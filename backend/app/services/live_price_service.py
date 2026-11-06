"""
即時股價服務：從 Yahoo Finance 取得當日每分鐘的價格與成交量。

給結果頁的「即時」模式使用。同一支股票在 CACHE_TTL_SECONDS 內的重複請求
共用同一份結果，避免多位使用者同時輪詢時一直打 Yahoo。
Yahoo 的報價可能有延遲（依交易所而定，最多約 15 分鐘）。
"""
from __future__ import annotations

import logging
import math
import re
import threading
import time
from typing import Any, Callable, Optional

import pandas as pd  # type: ignore

logger = logging.getLogger(__name__)

CACHE_TTL_SECONDS = 5
# 最後一根 K 棒距今超過這個秒數，就視為休市（盤中 Yahoo 約每分鐘更新）
MARKET_OPEN_STALENESS_SECONDS = 5 * 60

_TICKER_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9.\-]{0,14}$")
_MARKET_SUFFIX = {"us": "", "twse": ".TW", "tpex": ".TWO"}


class InvalidTickerError(ValueError):
    """股票代號或市場類型不合法。"""


class LiveDataUnavailableError(LookupError):
    """Yahoo 沒有這支股票的當日資料。"""


def resolve_live_symbol(ticker: str, market_type: Optional[str]) -> str:
    """把使用者輸入的代號與市場類型轉成 Yahoo Finance 代號（例如 2330 + twse → 2330.TW）。"""
    symbol = (ticker or "").strip().upper()
    if not _TICKER_PATTERN.match(symbol):
        raise InvalidTickerError(f"Invalid ticker: {ticker!r}")

    market = (market_type or "us").lower()
    if market not in _MARKET_SUFFIX:
        raise InvalidTickerError(f"Invalid market_type: {market_type!r}")

    suffix = _MARKET_SUFFIX[market]
    if suffix and "." not in symbol:
        return f"{symbol}{suffix}"
    return symbol


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not math.isnan(value)


def _round(value: float) -> float:
    return round(float(value), 4)


def build_live_quote(
    *,
    symbol: str,
    frame: pd.DataFrame,
    last_price: Optional[float],
    previous_close: Optional[float],
    currency: Optional[str],
    now: float,
) -> dict[str, Any]:
    """把 Yahoo 的每分鐘資料整理成前端需要的格式（時間一律為 Unix 秒）。"""
    rows = frame.dropna(subset=["Open", "High", "Low", "Close"])
    if rows.empty:
        raise LiveDataUnavailableError(f"No intraday data for {symbol}")

    times = [int(ts.timestamp()) for ts in rows.index]
    opens, highs, lows, closes = (rows[col].tolist() for col in ("Open", "High", "Low", "Close"))
    volumes = rows["Volume"].fillna(0).tolist()

    points = [{"time": t, "value": _round(c)} for t, c in zip(times, closes)]
    candles = [
        {"time": t, "open": _round(o), "high": _round(h), "low": _round(lo), "close": _round(c)}
        for t, o, h, lo, c in zip(times, opens, highs, lows, closes)
    ]
    volume_bars = [{"time": t, "volume": int(v)} for t, v in zip(times, volumes)]

    price = _round(last_price) if _is_number(last_price) else points[-1]["value"]
    prev = _round(previous_close) if _is_number(previous_close) else None
    change = _round(price - prev) if prev else None
    change_percent = _round((price - prev) / prev * 100) if prev else None
    as_of = times[-1]

    return {
        "symbol": symbol,
        "currency": currency,
        "price": price,
        "previous_close": prev,
        "change": change,
        "change_percent": change_percent,
        "market_open": now - as_of <= MARKET_OPEN_STALENESS_SECONDS,
        "as_of": as_of,
        "points": points,
        "candles": candles,
        "volumes": volume_bars,
    }


def fetch_live_quote(symbol: str) -> dict[str, Any]:
    """向 Yahoo Finance 取當日（休市時為最近交易日）每分鐘資料。"""
    import yfinance as yf  # type: ignore

    ticker = yf.Ticker(symbol)
    frame = ticker.history(period="1d", interval="1m", prepost=False)
    if frame is None or frame.empty:
        raise LiveDataUnavailableError(f"No intraday data for {symbol}")

    # 報價摘要偶爾缺欄位；拿不到時仍用每分鐘資料顯示，只是少了昨收與漲跌
    try:
        info = ticker.fast_info
        last_price = info.get("lastPrice")
        previous_close = info.get("previousClose")
        currency = info.get("currency")
    except Exception as e:
        logger.warning("Yahoo quote summary unavailable for %s: %s", symbol, e)
        last_price = previous_close = currency = None

    return build_live_quote(
        symbol=symbol,
        frame=frame,
        last_price=last_price,
        previous_close=previous_close,
        currency=currency,
        now=time.time(),
    )


_cache: dict[str, tuple[float, dict[str, Any]]] = {}
_cache_lock = threading.Lock()


def clear_cache() -> None:
    with _cache_lock:
        _cache.clear()


def get_live_quote(
    ticker: str,
    market_type: Optional[str],
    *,
    fetch: Callable[[str], dict[str, Any]] = fetch_live_quote,
    clock: Callable[[], float] = time.monotonic,
) -> dict[str, Any]:
    """取得即時報價；同一代號在 CACHE_TTL_SECONDS 內直接回傳快取。"""
    symbol = resolve_live_symbol(ticker, market_type)
    now = clock()

    with _cache_lock:
        cached = _cache.get(symbol)
        if cached and now - cached[0] < CACHE_TTL_SECONDS:
            return cached[1]

    quote = fetch(symbol)

    with _cache_lock:
        _cache[symbol] = (now, quote)
    return quote
