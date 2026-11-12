"""
即時股價服務：從 Yahoo Finance 取得當日每分鐘的價格與成交量（含盤前、盤後）。

給結果頁的「即時」模式使用。同一支股票在 CACHE_TTL_SECONDS 內的重複請求
共用同一份結果，避免多位使用者同時輪詢時一直打 Yahoo。
Yahoo 的報價可能有延遲（依交易所而定，最多約 15 分鐘）。
Yahoo 不提供盤前、盤後的每分鐘成交量，這些時段的成交量幾乎都是 0。
"""
from __future__ import annotations

import logging
import math
import re
import threading
import time
from dataclasses import dataclass
from itertools import groupby
from typing import Any, Callable, Optional

import pandas as pd  # type: ignore

logger = logging.getLogger(__name__)

CACHE_TTL_SECONDS = 5
# 拿不到交易時段時的備援：最後一根 K 棒距今超過這個秒數，就視為休市
MARKET_OPEN_STALENESS_SECONDS = 5 * 60

SESSION_PRE = "pre"
SESSION_REGULAR = "regular"
SESSION_POST = "post"
SESSION_CLOSED = "closed"

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


@dataclass(frozen=True)
class TradingPeriods:
    """交易所當日的盤前開始、正常盤起訖、盤後結束（Unix 秒）。"""

    pre_start: int
    regular_start: int
    regular_end: int
    post_end: int

    @property
    def has_extended_hours(self) -> bool:
        return self.pre_start < self.regular_start or self.post_end > self.regular_end


def parse_trading_periods(metadata: Any) -> Optional[TradingPeriods]:
    """從 Yahoo 的 history metadata 取出交易時段；格式不對就回傳 None。"""
    try:
        current = metadata["currentTradingPeriod"]
        periods = TradingPeriods(
            pre_start=int(current["pre"]["start"]),
            regular_start=int(current["regular"]["start"]),
            regular_end=int(current["regular"]["end"]),
            post_end=int(current["post"]["end"]),
        )
    except (KeyError, TypeError, ValueError):
        return None
    if not periods.pre_start <= periods.regular_start < periods.regular_end <= periods.post_end:
        return None
    return periods


def _seconds_of_day(ts: pd.Timestamp) -> int:
    return ts.hour * 3600 + ts.minute * 60 + ts.second


def _bar_sessions(index: pd.DatetimeIndex, periods: Optional[TradingPeriods]) -> list[str]:
    """每根 K 棒屬於盤前、盤中或盤後。

    用交易所當地的「時:分」比對，所以休市時顯示的上一個交易日也能正確分段。
    沒有延長交易時段的市場（例如台股）全部算盤中。
    """
    if periods is None or not periods.has_extended_hours:
        return [SESSION_REGULAR] * len(index)

    def local_seconds(epoch: int) -> int:
        ts = pd.Timestamp(epoch, unit="s", tz="UTC")
        return _seconds_of_day(ts.tz_convert(index.tz) if index.tz is not None else ts)

    regular_start = local_seconds(periods.regular_start)
    regular_end = local_seconds(periods.regular_end)

    def session_of(ts: pd.Timestamp) -> str:
        seconds = _seconds_of_day(ts)
        if seconds < regular_start:
            return SESSION_PRE
        if seconds >= regular_end:
            return SESSION_POST
        return SESSION_REGULAR

    return [session_of(ts) for ts in index]


def _current_session(now: float, as_of: int, periods: Optional[TradingPeriods]) -> str:
    """市場現在的狀態：盤前、盤中、盤後或休市。"""
    if periods is None:
        is_fresh = now - as_of <= MARKET_OPEN_STALENESS_SECONDS
        return SESSION_REGULAR if is_fresh else SESSION_CLOSED
    # 最後一根 K 棒早於今天的時段，代表今天還沒有任何成交（假日或尚未開盤）
    if as_of < periods.pre_start or now < periods.pre_start:
        return SESSION_CLOSED
    if now < periods.regular_start:
        return SESSION_PRE
    if now < periods.regular_end:
        return SESSION_REGULAR
    if now < periods.post_end:
        return SESSION_POST
    return SESSION_CLOSED


def _session_ranges(times: list[int], sessions: list[str]) -> list[dict[str, Any]]:
    """把連續同一時段的 K 棒合併成 {session, start, end}。"""
    ranges = []
    for session, group in groupby(zip(times, sessions), key=lambda pair: pair[1]):
        group_times = [t for t, _ in group]
        ranges.append({"session": session, "start": group_times[0], "end": group_times[-1]})
    return ranges


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
    trading_periods: Optional[TradingPeriods] = None,
) -> dict[str, Any]:
    """把 Yahoo 的每分鐘資料整理成前端需要的格式（時間一律為 Unix 秒）。

    last_price 是正常盤的最新價（盤前、盤後時就是最近一次收盤價）。
    最後一根 K 棒在盤前或盤後時，price 改用那根 K 棒的價格，
    previous_close 則改為最近一次正常盤收盤價，漲跌以它為基準。
    """
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

    sessions = _bar_sessions(rows.index, trading_periods)
    price_session = sessions[-1]
    regular_price = _round(last_price) if _is_number(last_price) else None
    if price_session == SESSION_REGULAR:
        price = regular_price if regular_price is not None else points[-1]["value"]
        prev = _round(previous_close) if _is_number(previous_close) else None
    else:
        price = points[-1]["value"]
        regular_closes = [c for c, s in zip(closes, sessions) if s == SESSION_REGULAR]
        fallback = _round(regular_closes[-1]) if regular_closes else None
        prev = regular_price if regular_price is not None else fallback
    change = _round(price - prev) if prev else None
    change_percent = _round((price - prev) / prev * 100) if prev else None
    as_of = times[-1]
    session = _current_session(now, as_of, trading_periods)

    return {
        "symbol": symbol,
        "currency": currency,
        "price": price,
        "previous_close": prev,
        "change": change,
        "change_percent": change_percent,
        "market_open": session != SESSION_CLOSED,
        "session": session,
        "price_session": price_session,
        "sessions": _session_ranges(times, sessions),
        "as_of": as_of,
        "points": points,
        "candles": candles,
        "volumes": volume_bars,
    }


def fetch_live_quote(symbol: str) -> dict[str, Any]:
    """向 Yahoo Finance 取當日（休市時為最近交易日）每分鐘資料，含盤前與盤後。"""
    import yfinance as yf  # type: ignore

    ticker = yf.Ticker(symbol)
    frame = ticker.history(period="1d", interval="1m", prepost=True)
    if frame is None or frame.empty:
        raise LiveDataUnavailableError(f"No intraday data for {symbol}")

    # 報價摘要偶爾缺欄位；拿不到時仍用每分鐘資料顯示，只是少了昨收與漲跌
    try:
        info = ticker.fast_info
        last_price = info.get("lastPrice")
        # previousClose 會混入盤後價，優先用正常盤的昨收
        previous_close = info.get("regularMarketPreviousClose") or info.get("previousClose")
        currency = info.get("currency")
    except Exception as e:
        logger.warning("Yahoo quote summary unavailable for %s: %s", symbol, e)
        last_price = previous_close = currency = None

    try:
        trading_periods = parse_trading_periods(ticker.get_history_metadata())
    except Exception as e:
        logger.warning("Yahoo trading periods unavailable for %s: %s", symbol, e)
        trading_periods = None

    return build_live_quote(
        symbol=symbol,
        frame=frame,
        last_price=last_price,
        previous_close=previous_close,
        currency=currency,
        now=time.time(),
        trading_periods=trading_periods,
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
