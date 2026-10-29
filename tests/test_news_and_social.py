"""新聞聚合、社群情緒、Alpha Vantage 錯誤處理與簡轉繁的單元測試（不打外部 API）。"""
import json

import pytest

from tradingagents.dataflows import alpha_vantage_common, interface, news_aggregator, social_sentiment
from tradingagents.dataflows.news_models import Article, NewsProviderError, dedupe_articles, search_name
from tradingagents.utils.zh_convert import localize_for, to_traditional


def _article(title, url, published="2026-10-28T00:00:00Z", provider="test"):
    return Article(title=title, url=url, source="src", published_at=published, provider=provider)


# ---------------------------------------------------------------- news_models

def test_dedupe_removes_same_url_and_same_title():
    articles = [
        _article("SK Hynix sold out", "https://a.com/x?utm=1"),
        _article("SK Hynix sold out!", "https://b.com/other"),  # 同標題（忽略標點）
        _article("Different story", "https://a.com/x"),  # 同 URL（忽略 query）
        _article("Unique", "https://c.com/u"),
    ]

    result = dedupe_articles(articles)

    assert [a.title for a in result] == ["SK Hynix sold out", "Unique"]


def test_search_name_strips_corporate_suffix():
    assert search_name("SK hynix Inc.") == "SK hynix"
    assert search_name("Taiwan Semiconductor Manufacturing Company Limited") == "Taiwan Semiconductor Manufacturing"


# ---------------------------------------------------------------- news_aggregator

@pytest.fixture
def stub_company(monkeypatch):
    monkeypatch.setattr(news_aggregator, "resolve_company_name", lambda symbol: "SK hynix Inc.")
    monkeypatch.setattr(news_aggregator, "enrich_with_content", lambda articles, top_n: articles)


def test_get_news_merges_providers_and_reports_status(monkeypatch, stub_company):
    monkeypatch.setattr(news_aggregator.providers, "finnhub_company_news",
                        lambda *a: [_article("Old news", "https://f.com/1", "2026-10-20T00:00:00Z")])
    monkeypatch.setattr(news_aggregator.providers, "marketaux_news",
                        lambda *a, **k: (_ for _ in ()).throw(NewsProviderError("未設定 Marketaux API 金鑰")))
    monkeypatch.setattr(news_aggregator.providers, "newsapi_everything",
                        lambda *a: [_article("Newest", "https://n.com/1", "2026-10-29T00:00:00Z")])
    monkeypatch.setattr(news_aggregator, "_throttled_gdelt",
                        lambda *a: [_article("Old news", "https://g.com/dup", "2026-10-20T00:00:00Z")])

    report = news_aggregator.get_news("skhy", "2026-10-16", "2026-10-30")

    assert report.index("Newest") < report.index("Old news")  # 依時間新到舊
    assert report.count("Old news") == 1  # 跨來源去重
    assert "Marketaux：無法使用" in report
    assert "SK hynix Inc.（SKHY）" in report


def test_get_news_raises_when_every_provider_is_empty(monkeypatch, stub_company):
    for name in ("finnhub_company_news", "newsapi_everything"):
        monkeypatch.setattr(news_aggregator.providers, name, lambda *a: [])
    monkeypatch.setattr(news_aggregator.providers, "marketaux_news", lambda *a, **k: [])
    monkeypatch.setattr(news_aggregator, "_throttled_gdelt", lambda *a: [])

    with pytest.raises(NewsProviderError):
        news_aggregator.get_news("SKHY", "2026-10-16", "2026-10-30")


def test_global_news_drops_articles_after_analysis_date(monkeypatch, stub_company):
    monkeypatch.setattr(news_aggregator.providers, "finnhub_general_news",
                        lambda limit: [_article("Future", "https://f.com/fut", "2026-11-05T00:00:00Z"),
                                       _article("Past", "https://f.com/past", "2026-10-25T00:00:00Z")])
    monkeypatch.setattr(news_aggregator.providers, "newsapi_business_headlines", lambda limit: [])
    monkeypatch.setattr(news_aggregator.providers, "marketaux_news", lambda *a, **k: [])
    monkeypatch.setattr(news_aggregator, "_throttled_gdelt", lambda *a: [])

    report = news_aggregator.get_global_news("2026-10-30", 7, 10)

    assert "Past" in report
    assert "Future" not in report


# ---------------------------------------------------------------- social_sentiment

def _stub_social(monkeypatch, **overrides):
    defaults = {
        "stocktwits_messages": lambda ticker: ("StockTwits：無法使用（未設定）", ""),
        "x_posts": lambda *a: ("X：無法使用（未設定）", ""),
        "lunarcrush_topic": lambda *a: ("LunarCrush：無法使用（未設定）", ""),
        "apewisdom_rank": lambda ticker: (social_sentiment.APEWISDOM_UNRANKED, "## 未上榜說明"),
        "hacker_news": lambda *a: ("Hacker News：0 則", ""),
        "ptt_stock": lambda *a: ("PTT：不適用", ""),
        "reddit_posts": lambda *a: ("Reddit：無法使用（未設定）", ""),
        "jina_social_search": lambda keyword: ("Jina 搜尋：無法使用（未設定）", ""),
    }
    defaults.update(overrides)
    for name, fn in defaults.items():
        monkeypatch.setattr(social_sentiment, name, fn)
    monkeypatch.setattr(social_sentiment, "resolve_company_name", lambda symbol: "SK hynix Inc.")


def test_social_sentiment_flags_no_data_even_if_apewisdom_unranked(monkeypatch):
    _stub_social(monkeypatch)

    report = social_sentiment.get_social_sentiment("SKHY", "2026-10-30")

    assert "【社群資料不足】" in report
    assert "## 資料來源狀態" in report


def test_social_sentiment_uses_real_data_without_notice(monkeypatch):
    _stub_social(monkeypatch, hacker_news=lambda *a: ("Hacker News：2 則", "## HN 討論"))

    report = social_sentiment.get_social_sentiment("SKHY", "2026-10-30")

    assert "【社群資料不足】" not in report
    assert "## HN 討論" in report


def test_ptt_date_infers_previous_year_for_later_month():
    assert social_sentiment._ptt_date("10/26", "2026-10-30") == "2026-10-26"
    assert social_sentiment._ptt_date("12/31", "2026-01-05") == "2025-12-31"


# ---------------------------------------------------------------- Alpha Vantage 錯誤不可當成資料

class _FakeResponse:
    def __init__(self, payload):
        self.text = json.dumps(payload)

    def raise_for_status(self):
        return None


@pytest.mark.parametrize(
    "payload, expected",
    [
        ({"Information": "This is a premium endpoint. Subscribe to unlock."}, alpha_vantage_common.AlphaVantageAPIError),
        ({"Note": "Our standard API rate limit is 25 requests per day."}, alpha_vantage_common.AlphaVantageRateLimitError),
        ({"Error Message": "Invalid API call."}, alpha_vantage_common.AlphaVantageAPIError),
    ],
)
def test_alpha_vantage_error_payloads_raise(monkeypatch, payload, expected):
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test")
    monkeypatch.setattr(alpha_vantage_common.requests, "get", lambda *a, **k: _FakeResponse(payload))

    with pytest.raises(expected):
        alpha_vantage_common._make_api_request("NEWS_SENTIMENT", {})


# ---------------------------------------------------------------- route_to_vendor

def test_multi_vendor_stops_before_fallback_vendors(monkeypatch):
    calls = []

    def vendor(name, result=None):
        def impl(*args):
            calls.append(name)
            if result is None:
                raise RuntimeError("no data")
            return result
        return impl

    monkeypatch.setitem(interface.VENDOR_METHODS, "get_news", {
        "finmind": vendor("finmind", "tw news"),
        "aggregator": vendor("aggregator", "global news"),
        "google": vendor("google", "should not run"),
    })
    monkeypatch.setattr(interface, "get_config", lambda: {"tool_vendors": {"get_news": "finmind,aggregator"}})

    result = interface.route_to_vendor("get_news", "2330", "2026-10-01", "2026-10-30")

    assert calls == ["finmind", "aggregator"]
    assert "tw news" in result and "global news" in result


# ---------------------------------------------------------------- 簡轉繁

def test_to_traditional_converts_nested_reports_without_mutating():
    reports = {"fundamentals_report": "财务分析：资料中心", "debate": {"history": ["营收成长"]}, "count": 1}

    converted = to_traditional(reports)

    assert converted == {"fundamentals_report": "財務分析：資料中心", "debate": {"history": ["營收成長"]}, "count": 1}
    assert reports["fundamentals_report"] == "财务分析：资料中心"


def test_localize_for_leaves_english_and_traditional_untouched():
    assert localize_for("en", "资料") == "资料"
    assert localize_for("zh-TW", "最終交易提案：持有，股價自高點回落") == "最終交易提案：持有，股價自高點回落"


def test_empty_vendor_result_falls_back_to_next_vendor(monkeypatch):
    monkeypatch.setitem(interface.VENDOR_METHODS, "get_news", {
        "local": lambda *a: "   ",  # 本地資料目錄不存在時回傳空字串
        "google": lambda *a: "google news",
    })
    monkeypatch.setattr(interface, "get_config", lambda: {"tool_vendors": {"get_news": "local"}})

    assert interface.route_to_vendor("get_news", "SKHY", "2026-10-16", "2026-10-30") == "google news"
