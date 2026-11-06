"""即時股價服務與 /api/price/live 接口的單元測試（不打外部 API）。"""
from datetime import datetime, timezone

import pandas as pd
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.services import live_price_service as lps


def _intraday_frame(start_epoch: int, closes: list[float]) -> pd.DataFrame:
    index = pd.to_datetime(
        [start_epoch + 60 * i for i in range(len(closes))], unit="s", utc=True
    ).tz_convert("America/New_York")
    return pd.DataFrame(
        {
            "Open": [c - 1 for c in closes],
            "High": [c + 2 for c in closes],
            "Low": [c - 2 for c in closes],
            "Close": closes,
            "Volume": [1000 * (i + 1) for i in range(len(closes))],
        },
        index=index,
    )


@pytest.fixture(autouse=True)
def _clear_cache():
    lps.clear_cache()
    yield
    lps.clear_cache()


# ── resolve_live_symbol ─────────────────────────────────────────────────────

@pytest.mark.parametrize(
    "ticker, market_type, expected",
    [
        ("nvda", "us", "NVDA"),
        ("BRK-B", "us", "BRK-B"),
        ("2330", "twse", "2330.TW"),
        ("6488", "tpex", "6488.TWO"),
        ("2330.TW", "twse", "2330.TW"),
    ],
)
def test_resolve_live_symbol_maps_market_to_yahoo_suffix(ticker, market_type, expected):
    assert lps.resolve_live_symbol(ticker, market_type) == expected


@pytest.mark.parametrize("ticker", ["", "AAPL;rm -rf", "../etc", "A" * 20])
def test_resolve_live_symbol_rejects_invalid_ticker(ticker):
    with pytest.raises(lps.InvalidTickerError):
        lps.resolve_live_symbol(ticker, "us")


def test_resolve_live_symbol_rejects_unknown_market():
    with pytest.raises(lps.InvalidTickerError):
        lps.resolve_live_symbol("NVDA", "crypto")


# ── build_live_quote ────────────────────────────────────────────────────────

def test_build_live_quote_returns_points_candles_volumes_and_change():
    start = 1_793_900_000
    frame = _intraday_frame(start, [100.0, 101.0, 103.0])

    quote = lps.build_live_quote(
        symbol="NVDA",
        frame=frame,
        last_price=104.0,
        previous_close=100.0,
        currency="USD",
        now=start + 150,
    )

    assert quote["symbol"] == "NVDA"
    assert quote["currency"] == "USD"
    assert quote["price"] == 104.0
    assert quote["previous_close"] == 100.0
    assert quote["change"] == pytest.approx(4.0)
    assert quote["change_percent"] == pytest.approx(4.0)
    assert quote["points"] == [
        {"time": start, "value": 100.0},
        {"time": start + 60, "value": 101.0},
        {"time": start + 120, "value": 103.0},
    ]
    assert quote["candles"][0] == {
        "time": start, "open": 99.0, "high": 102.0, "low": 98.0, "close": 100.0,
    }
    assert quote["volumes"][-1] == {"time": start + 120, "volume": 3000}
    assert quote["as_of"] == start + 120
    assert quote["market_open"] is True


def test_build_live_quote_marks_market_closed_when_last_bar_is_stale():
    start = 1_793_900_000
    frame = _intraday_frame(start, [100.0, 101.0])

    quote = lps.build_live_quote(
        symbol="NVDA", frame=frame, last_price=None, previous_close=99.0,
        currency="USD", now=start + 60 + lps.MARKET_OPEN_STALENESS_SECONDS + 1,
    )

    assert quote["market_open"] is False
    # 沒有 last_price 時退回最後一根收盤價
    assert quote["price"] == 101.0


def test_build_live_quote_skips_rows_with_missing_prices():
    start = 1_793_900_000
    frame = _intraday_frame(start, [100.0, 101.0, 102.0])
    frame.iloc[1, frame.columns.get_loc("Close")] = float("nan")

    quote = lps.build_live_quote(
        symbol="NVDA", frame=frame, last_price=102.0, previous_close=None,
        currency=None, now=start + 120,
    )

    assert [p["time"] for p in quote["points"]] == [start, start + 120]
    assert quote["change"] is None
    assert quote["change_percent"] is None


def test_build_live_quote_raises_when_no_usable_data():
    empty = _intraday_frame(1_793_900_000, [])
    with pytest.raises(lps.LiveDataUnavailableError):
        lps.build_live_quote(
            symbol="ZZZZ", frame=empty, last_price=None, previous_close=None,
            currency=None, now=1_793_900_000,
        )


# ── get_live_quote caching ──────────────────────────────────────────────────

def test_get_live_quote_reuses_cached_result_within_ttl():
    calls = []
    clock = {"now": 1_000.0}

    def fake_fetch(symbol):
        calls.append(symbol)
        return {"symbol": symbol, "n": len(calls)}

    first = lps.get_live_quote("NVDA", "us", fetch=fake_fetch, clock=lambda: clock["now"])
    clock["now"] += lps.CACHE_TTL_SECONDS - 1
    second = lps.get_live_quote("nvda", "us", fetch=fake_fetch, clock=lambda: clock["now"])
    clock["now"] += 2
    third = lps.get_live_quote("NVDA", "us", fetch=fake_fetch, clock=lambda: clock["now"])

    assert first == second == {"symbol": "NVDA", "n": 1}
    assert third == {"symbol": "NVDA", "n": 2}
    assert calls == ["NVDA", "NVDA"]


# ── route ───────────────────────────────────────────────────────────────────

@pytest.fixture
def client(monkeypatch):
    from backend.app.api.price import router

    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_live_price_route_returns_quote(client, monkeypatch):
    sample = {
        "symbol": "2330.TW", "currency": "TWD", "price": 1000.0, "previous_close": 990.0,
        "change": 10.0, "change_percent": 1.01, "market_open": True, "as_of": 1,
        "points": [{"time": 1, "value": 1000.0}],
        "candles": [{"time": 1, "open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0}],
        "volumes": [{"time": 1, "volume": 5}],
    }
    seen = {}

    def fake_get(ticker, market_type):
        seen["args"] = (ticker, market_type)
        return sample

    monkeypatch.setattr("backend.app.api.price.get_live_quote", fake_get)

    res = client.get("/api/price/live", params={"ticker": "2330", "market_type": "twse"})

    assert res.status_code == 200
    assert res.json()["symbol"] == "2330.TW"
    assert seen["args"] == ("2330", "twse")


@pytest.mark.parametrize(
    "error, status",
    [
        (lps.InvalidTickerError("bad"), 400),
        (lps.LiveDataUnavailableError("none"), 404),
        (RuntimeError("yahoo down"), 502),
    ],
)
def test_live_price_route_maps_errors_to_status(client, monkeypatch, error, status):
    def boom(ticker, market_type):
        raise error

    monkeypatch.setattr("backend.app.api.price.get_live_quote", boom)

    res = client.get("/api/price/live", params={"ticker": "NVDA", "market_type": "us"})

    assert res.status_code == status
    assert "yahoo down" not in res.text


# ── fetch_live_quote (yfinance stubbed) ─────────────────────────────────────

class _FakeTicker:
    def __init__(self, frame, info_error=False):
        self._frame = frame
        self._info_error = info_error

    def history(self, **_kwargs):
        return self._frame

    @property
    def fast_info(self):
        if self._info_error:
            raise KeyError("currentTradingPeriod")
        return {"lastPrice": 101.0, "previousClose": 100.0, "currency": "USD"}


def _patch_yf(monkeypatch, ticker):
    import yfinance

    monkeypatch.setattr(yfinance, "Ticker", lambda symbol: ticker)


def test_fetch_live_quote_reports_unknown_ticker_as_unavailable(monkeypatch):
    _patch_yf(monkeypatch, _FakeTicker(_intraday_frame(0, []), info_error=True))

    with pytest.raises(lps.LiveDataUnavailableError):
        lps.fetch_live_quote("ZZZZZZQ")


def test_fetch_live_quote_survives_missing_quote_summary(monkeypatch):
    frame = _intraday_frame(1_793_900_000, [100.0, 102.0])
    _patch_yf(monkeypatch, _FakeTicker(frame, info_error=True))

    quote = lps.fetch_live_quote("NVDA")

    assert quote["price"] == 102.0
    assert quote["previous_close"] is None
