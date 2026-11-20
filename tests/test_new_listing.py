"""新上市股票資料補強（tradingagents/dataflows/new_listing.py）的單元測試，不連網。"""

import pandas as pd
import pytest

from tradingagents.dataflows import new_listing
from tradingagents.dataflows.new_listing import (
    IntradayBars,
    download_daily,
    format_intraday_csv,
    indicator_min_bars,
    is_new_listing,
    pick_intraday_interval,
    summarize_new_listing,
)


def _daily_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Open": [111.5],
            "High": [115.1],
            "Low": [92.72],
            "Close": [97.17],
            "Adj Close": [97.17],
            "Volume": [853213200],
        },
        index=pd.DatetimeIndex(["2026-11-19"], name="Date"),
    )


def _intraday_bars() -> IntradayBars:
    frame = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2026-11-19 11:45", "2026-11-19 11:50"]),
            "Open": [111.5, 111.68],
            "High": [114.99, 113.31],
            "Low": [110.0, 106.0],
            "Close": [111.68, 111.51],
            "Volume": [100, 300],
        }
    )
    return IntradayBars(interval="5m", frame=frame)


@pytest.mark.parametrize(
    ("indicator", "expected"),
    [
        ("close_50_sma", 50),
        ("close_200_sma", 200),
        ("close_10_ema", 10),
        ("macd", 26),
        ("macds", 34),
        ("rsi", 15),
        ("boll_ub", 20),
        ("unknown", 1),
    ],
)
def test_indicator_min_bars(indicator, expected):
    assert indicator_min_bars(indicator) == expected


def test_is_new_listing_thresholds():
    assert not is_new_listing(0)
    assert is_new_listing(1)
    assert is_new_listing(19)
    assert not is_new_listing(20)


def test_pick_intraday_interval_scales_with_days_listed():
    assert pick_intraday_interval(1) == "5m"
    assert pick_intraday_interval(5) == "30m"
    assert pick_intraday_interval(15) == "60m"


def test_summary_reports_first_day_and_vwap():
    summary = summarize_new_listing(_daily_frame(), _intraday_bars())

    assert "自 2026-11-19 起僅 1 個交易日" in summary
    assert "首日開盤 111.50，收盤 97.17" in summary
    assert "-12.85%" in summary
    # VWAP = Σ(典型價 × 量) / Σ量
    typical = [(114.99 + 110.0 + 111.68) / 3, (113.31 + 106.0 + 111.51) / 3]
    vwap = (typical[0] * 100 + typical[1] * 300) / 400
    assert f"2026-11-19：{vwap:.2f}" in summary


def test_summary_without_intraday_has_no_vwap_section():
    assert "VWAP" not in summarize_new_listing(_daily_frame(), None)


def test_intraday_csv_uses_local_minutes():
    csv = format_intraday_csv(_intraday_bars())

    assert "共 2 根" in csv
    assert "2026-11-19 11:45,111.5,114.99,110.0,111.68,100" in csv


def test_download_daily_falls_back_to_recent_bars(monkeypatch):
    monkeypatch.setattr(new_listing.yf, "download", lambda *a, **k: pd.DataFrame())
    monkeypatch.setattr(new_listing, "_fetch_recent_daily", lambda symbol: _daily_frame())

    result = download_daily("ANT", "2025-11-20", "2026-11-20")

    assert len(result) == 1
    assert result.index[0] == pd.Timestamp("2026-11-19")


def test_download_daily_fallback_respects_requested_range(monkeypatch):
    monkeypatch.setattr(new_listing.yf, "download", lambda *a, **k: pd.DataFrame())
    monkeypatch.setattr(new_listing, "_fetch_recent_daily", lambda symbol: _daily_frame())

    assert download_daily("ANT", "2026-11-20", "2026-11-21").empty


def test_fetch_intraday_skips_data_beyond_yahoo_retention():
    assert new_listing.fetch_intraday_bars("ANT", "2020-01-01", "2020-01-02", "5m") is None
