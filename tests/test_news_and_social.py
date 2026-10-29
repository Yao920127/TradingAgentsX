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


def _recording_paid_sources(calls):
    def paid(label):
        def impl(*args):
            calls.append(label)
            return f"{label}：1 則", f"## {label} 資料"
        return impl
    return {
        "stocktwits_messages": paid("StockTwits"),
        "x_posts": paid("X"),
        "lunarcrush_topic": paid("LunarCrush"),
        "jina_social_search": paid("Jina 搜尋"),
    }


def test_paid_social_sources_skipped_when_free_sources_have_data(monkeypatch):
    calls = []
    _stub_social(monkeypatch, hacker_news=lambda *a: ("Hacker News：2 則", "## HN 討論"),
                 **_recording_paid_sources(calls))

    report = social_sentiment.get_social_sentiment("SKHY", "2026-10-30")

    assert calls == []
    assert "StockTwits：未啟用（免費來源已有資料" in report


def test_paid_social_sources_used_when_free_sources_are_empty(monkeypatch):
    calls = []
    _stub_social(monkeypatch, **_recording_paid_sources(calls))

    report = social_sentiment.get_social_sentiment("SKHY", "2026-10-30")

    assert sorted(calls) == sorted(["StockTwits", "X", "LunarCrush", "Jina 搜尋"])
    assert "## StockTwits 資料" in report
    assert "【社群資料不足】" not in report


def test_google_news_fallback_adds_jina_content_to_top_three(monkeypatch):
    from tradingagents.dataflows import google

    items = [
        {"link": f"https://news.example/{i}", "title": f"Story {i}", "snippet": "s", "date": "", "source": "src"}
        for i in range(4)
    ]
    monkeypatch.setattr(google, "getNewsData", lambda *a: items)
    monkeypatch.setattr(google, "read_article", lambda url: f"BODY {url[-1]}")

    report = google.get_google_company_news("SKHY", "2026-10-16", "2026-10-30")

    assert "全文摘錄：BODY 0" in report and "全文摘錄：BODY 2" in report
    assert "BODY 3" not in report


# ---------------------------------------------------------------- Jina 共用工具與各來源

def test_extract_urls_dedupes_strips_punctuation_and_excludes_domains():
    from tradingagents.dataflows.jina_reader import extract_urls

    text = "見 https://a.com/x。另見 (https://b.com/y), 重複 https://a.com/x 與 https://x.com/user/status/1"

    assert extract_urls(text, 5, exclude_domains=("x.com/",)) == ["https://a.com/x", "https://b.com/y"]


def test_attach_content_reads_top_n_with_urls_without_mutating(monkeypatch):
    from tradingagents.dataflows import jina_reader

    monkeypatch.setattr(jina_reader, "read_article", lambda url: f"BODY {url}")
    items = [{"url": ""}, {"url": "u1"}, {"url": "u2"}, {"url": "u3"}]

    result = jina_reader.attach_content(items, "url", 2)

    assert [r.get("content") for r in result] == [None, "BODY u1", "BODY u2", None]
    assert "content" not in items[1]


def test_append_linked_content_adds_excerpt_section(monkeypatch):
    from tradingagents.dataflows import jina_reader

    monkeypatch.setattr(jina_reader, "read_article", lambda url: "full text")

    result = jina_reader.append_linked_content("Summary citing https://news.example/a", 3)

    assert result.startswith("Summary citing")
    assert "## 引用文章全文摘錄" in result and "full text" in result


def test_alpha_vantage_news_feed_gets_jina_content(monkeypatch):
    from tradingagents.dataflows import alpha_vantage_news

    feed = {"feed": [{"title": f"t{i}", "url": f"https://av.example/{i}", "summary": "s"} for i in range(4)]}
    monkeypatch.setattr(alpha_vantage_news, "_make_api_request", lambda *a: json.dumps(feed))
    monkeypatch.setattr(alpha_vantage_news, "attach_content",
                        lambda items, key, n: [{**it, "content": "BODY"} if i < n else it for i, it in enumerate(items)])

    result = alpha_vantage_news.get_news("SKHY", "2026-10-16", "2026-10-30", use_toon=False)

    contents = [item.get("content") for item in json.loads(result)["feed"]]
    assert contents == ["BODY", "BODY", "BODY", None]


def test_stocktwits_reads_external_links_but_not_platform_links(monkeypatch):
    from tradingagents.dataflows import social_paid_sources

    messages = [
        {"body": "Earnings beat https://news.example/q3 $SKHY", "sentiment": "bullish", "likes": 5},
        {"body": "lol https://stocktwits.com/message/1", "sentiment": "bearish", "likes": 1},
    ]
    monkeypatch.setattr(social_paid_sources, "_run_apify_actor", lambda *a: messages)
    read = []
    monkeypatch.setattr(social_paid_sources, "read_urls", lambda urls: read.extend(urls) or ["Q3 article"] * len(urls))

    status, block = social_paid_sources.stocktwits_messages("SKHY")

    assert read == ["https://news.example/q3"]
    assert "看多 1 則、看空 1 則" in block and "Q3 article" in block


def test_gdelt_retries_once_after_rate_limit(monkeypatch):
    attempts = []

    def flaky(*args):
        attempts.append(1)
        if len(attempts) == 1:
            raise NewsProviderError("GDELT 超過速率限制（每 5 秒 1 次）")
        return [_article("Recovered", "https://g.com/ok")]

    monkeypatch.setattr(news_aggregator.providers, "gdelt_news", flaky)
    monkeypatch.setattr(news_aggregator, "GDELT_MIN_INTERVAL", 0)

    result = news_aggregator._throttled_gdelt("q", "2026-10-16", "2026-10-30", 10)

    assert len(attempts) == 2 and result[0].title == "Recovered"


# ---------------------------------------------------------------- 報告版面校正與截斷偵測

def test_normalize_report_markdown_unifies_heading_styles():
    from tradingagents.utils.report_format import normalize_report_markdown

    text = "\n".join([
        "# SK hynix 基本面分析報告",
        "**一、市場概況**",
        "股價自高點 **195.37** 回檔。",
        "二、技術指標解讀",
        "**主要風險**",
        "**競爭地位**：在 DRAM 市場形成三強。",
        "| **項目** | 數值 |",
    ])

    lines = [line for line in normalize_report_markdown(text).splitlines() if line]

    assert lines == [
        "## SK hynix 基本面分析報告",
        "## 一、市場概況",
        "股價自高點 **195.37** 回檔。",  # 內文關鍵字粗體保留
        "## 二、技術指標解讀",
        "### 主要風險",
        "**競爭地位**：在 DRAM 市場形成三強。",  # 行內粗體不是標題
        "| **項目** | 數值 |",  # 表格不處理
    ]


def test_long_bold_sentence_is_not_turned_into_heading():
    from tradingagents.utils.report_format import normalize_report_markdown

    sentence = "**" + "這是一整句被加粗的長篇強調內文，超過小標題長度上限所以應該維持原樣不轉成標題。" + "**"

    assert normalize_report_markdown(sentence) == sentence


class _Response:
    def __init__(self, content, metadata):
        self.content = content
        self.response_metadata = metadata


@pytest.mark.parametrize("metadata", [{"stop_reason": "max_tokens"}, {"finish_reason": "length"}, {"finish_reason": "MAX_TOKENS"}])
def test_report_text_flags_truncated_output(metadata):
    from tradingagents.agents.utils.output_filter import report_text

    result = report_text(_Response([{"type": "text", "text": "| 項目 | FY2024 | Q1 2"}], metadata), "Fundamentals_Analyst")

    assert result.startswith("| 項目 | FY2024 | Q1 2")
    assert "被截斷" in result


def test_report_text_leaves_complete_output_untouched():
    from tradingagents.agents.utils.output_filter import report_text

    assert report_text(_Response("完整報告", {"stop_reason": "end_turn"}), "Market_Analyst") == "完整報告"


def test_to_traditional_keeps_traditional_vocabulary():
    # s2twp 會把「項目」改成「專案」、「數據」改成「資料」；s2tw 只轉字形
    assert to_traditional("项目 数据 項目 數據") == "項目 數據 項目 數據"
