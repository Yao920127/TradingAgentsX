# -*- coding: utf-8 -*-
"""台股（FinMind）相關修正的回歸測試：新聞逐日抓取、公司名稱、財報期間標示、toon 轉換。"""
import json

import pytest

from tradingagents.dataflows import finmind_fundamentals, finmind_news
from tradingagents.graph import propagation


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def _news_item(day, link, source="CMoney"):
    return {"date": f"{day} 08:00:00", "title": f"新聞 {link}", "link": link, "source": source}


@pytest.fixture
def no_content(monkeypatch):
    monkeypatch.setattr(finmind_news, "attach_content", lambda items, key, n: items)


def test_news_fetches_each_day_backward_from_end_date(monkeypatch, no_content):
    # Arrange：FinMind TaiwanStockNews 只回傳 start_date 當天的新聞
    requested_days = []

    def fake_get(url, headers=None, params=None, timeout=None):
        day = params["start_date"]
        requested_days.append(day)
        return _FakeResponse({"data": [_news_item(day, f"https://x/{day}")]})

    monkeypatch.setattr(finmind_news.requests, "get", fake_get)

    # Act
    result = json.loads(finmind_news.get_news("2330", "2026-11-06", "2026-11-20", use_toon=False))

    # Assert：從 end_date 往回抓，最新的新聞排在最前面
    assert requested_days[0] == "2026-11-20"
    assert result["feed"][0]["date"] == "2026-11-20"
    assert len(requested_days) <= finmind_news.NEWS_LOOKBACK_DAYS


def test_news_never_requests_days_before_start_date(monkeypatch, no_content):
    requested_days = []

    def fake_get(url, headers=None, params=None, timeout=None):
        requested_days.append(params["start_date"])
        return _FakeResponse({"data": []})

    monkeypatch.setattr(finmind_news.requests, "get", fake_get)
    monkeypatch.setattr(finmind_news, "_make_api_request", lambda **kw: {"data": []})

    with pytest.raises(finmind_news.FinMindDataNotFoundError):
        finmind_news.get_news("2330", "2026-11-19", "2026-11-20", use_toon=False)

    assert requested_days == ["2026-11-20", "2026-11-19"]


def test_news_dedupes_same_link_from_different_sources(monkeypatch, no_content):
    def fake_get(url, headers=None, params=None, timeout=None):
        day = params["start_date"]
        return _FakeResponse({"data": [
            _news_item(day, "https://cmoney/1", "CMoney"),
            _news_item(day, "https://cmoney/1", "cmoney.tw"),
        ]})

    monkeypatch.setattr(finmind_news.requests, "get", fake_get)

    result = json.loads(finmind_news.get_news("2330", "2026-11-20", "2026-11-20", use_toon=False))

    assert [n["link"] for n in result["feed"]] == ["https://cmoney/1"]


def test_news_skips_failed_day_and_keeps_others(monkeypatch, no_content):
    def fake_get(url, headers=None, params=None, timeout=None):
        day = params["start_date"]
        if day == "2026-11-20":
            raise finmind_news.requests.RequestException("boom")
        return _FakeResponse({"data": [_news_item(day, f"https://x/{day}")]})

    monkeypatch.setattr(finmind_news.requests, "get", fake_get)

    result = json.loads(finmind_news.get_news("2330", "2026-11-19", "2026-11-20", use_toon=False))

    assert [n["date"] for n in result["feed"]] == ["2026-11-19"]


def test_taiwan_ticker_resolves_name_with_tw_suffix(monkeypatch):
    # Arrange：裸代碼 2330 在 yfinance 對應到東證的 For-side.com
    looked_up = []

    class FakeTicker:
        def __init__(self, symbol):
            looked_up.append(symbol)
            names = {"2330": "For-side.com Co Ltd", "2330.TW": "Taiwan Semiconductor Manufacturing Company Limited"}
            self.info = {"longName": names.get(symbol)}

    import yfinance
    monkeypatch.setattr(yfinance, "Ticker", FakeTicker)
    monkeypatch.setattr(propagation, "route_to_vendor", lambda *a, **k: "{}")
    monkeypatch.setattr(propagation, "get_yfinance_ticker", lambda t: f"{t}.TW")

    # Act
    state = propagation.Propagator().create_initial_state("2330", "2026-11-20")

    # Assert
    assert looked_up == ["2330.TW"]
    assert state["company_name"] == "Taiwan Semiconductor Manufacturing Company Limited"
    assert state["company_of_interest"] == "2330"


def test_us_ticker_resolves_name_without_suffix(monkeypatch):
    looked_up = []

    class FakeTicker:
        def __init__(self, symbol):
            looked_up.append(symbol)
            self.info = {"longName": "NVIDIA Corporation"}

    import yfinance
    monkeypatch.setattr(yfinance, "Ticker", FakeTicker)
    monkeypatch.setattr(propagation, "route_to_vendor", lambda *a, **k: "{}")

    state = propagation.Propagator().create_initial_state("nvda", "2026-11-20")

    assert looked_up == ["NVDA"]
    assert state["company_name"] == "NVIDIA Corporation"


def _statement_rows(dataset):
    return {"data": [
        {"date": "2026-09-30", "type": "Revenue", "value": 1.0, "stock_id": "2330"},
        {"date": "2026-06-30", "type": "Revenue", "value": 1.0, "stock_id": "2330"},
    ]}


def test_income_statement_is_labelled_single_quarter(monkeypatch):
    monkeypatch.setattr(finmind_fundamentals, "_make_api_request", lambda **kw: _statement_rows(kw["dataset"]))

    result = json.loads(finmind_fundamentals.get_income_statement("2330", curr_date="2026-11-20", use_toon=False))

    assert "單季" in result["period_basis"]


def test_cashflow_is_labelled_year_to_date(monkeypatch):
    monkeypatch.setattr(finmind_fundamentals, "_make_api_request", lambda **kw: _statement_rows(kw["dataset"]))

    result = json.loads(finmind_fundamentals.get_cashflow("2330", curr_date="2026-11-20", use_toon=False))

    assert "累計" in result["period_basis"]


def test_toon_converter_imports_and_encodes():
    from tradingagents.utils.toon_converter import convert_json_to_toon

    encoded = convert_json_to_toon({"stock_id": "2330", "rows": [{"a": 1}, {"a": 2}]})

    assert "2330" in encoded
    assert not encoded.lstrip().startswith("{")
