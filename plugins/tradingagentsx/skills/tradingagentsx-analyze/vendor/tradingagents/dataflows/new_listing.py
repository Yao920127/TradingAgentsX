"""
新上市（剛 IPO）股票的資料補強。

剛上市的股票只有寥寥幾根日 K，50/200 日均線、MACD、RSI 等日線指標都算不出來，
stockstats 卻會用不足的資料硬算出 MACD=0、RSI=50 之類「看起來像中性」的假值。
本模組負責：

1. 判斷是否為新上市股票（日 K 根數不足）。
2. 改抓盤中 K 線（5 分 / 30 分 / 60 分），讓分析師與價格圖仍有價量資料可用。
3. 產生上市以來的摘要（首日開收、區間高低、各交易日 VWAP 等）。
4. 提供每個指標所需的最少 K 棒數，讓呼叫端把資料不足的值標為 N/A，而非回傳假值。
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)

# 日 K 少於這個數量就視為新上市股票（約一個月的交易日，也是布林通道所需的 20 根）
NEW_LISTING_MAX_DAILY_BARS = 20

# 給 LLM 的盤中 K 線最多幾根，避免塞爆上下文
MAX_INTRADAY_ROWS_FOR_LLM = 200

# Yahoo 盤中資料的保留期限：5 分 / 30 分約 60 天，60 分約 730 天
_INTRADAY_LOOKBACK_LIMIT_DAYS = {"5m": 59, "30m": 59, "60m": 729}

# 指標最少需要的 K 棒數（不足時 stockstats 的計算結果沒有意義）
_INDICATOR_MIN_BARS = {
    "macd": 26,
    "macds": 34,
    "macdh": 34,
    "rsi": 15,
    "boll": 20,
    "boll_ub": 20,
    "boll_lb": 20,
    "atr": 15,
    "vwma": 14,
    "mfi": 15,
}
_WINDOWED_INDICATOR = re.compile(r"^[a-z]+_(\d+)_[a-z]+$")


@dataclass(frozen=True)
class IntradayBars:
    """盤中 K 線。frame 欄位：Date（交易所當地時間，datetime）、Open、High、Low、Close、Volume。"""

    interval: str
    frame: pd.DataFrame


def indicator_min_bars(indicator: str) -> int:
    """回傳指標至少需要幾根 K 棒；未知指標回傳 1（不額外遮蔽）。"""
    name = indicator.lower()
    if name in _INDICATOR_MIN_BARS:
        return _INDICATOR_MIN_BARS[name]
    match = _WINDOWED_INDICATOR.match(name)
    return int(match.group(1)) if match else 1


def is_new_listing(daily_bar_count: int) -> bool:
    """日 K 根數不足（但至少有 1 根）即視為新上市。"""
    return 0 < daily_bar_count < NEW_LISTING_MAX_DAILY_BARS


def pick_intraday_interval(daily_bar_count: int) -> str:
    """依上市天數挑選盤中週期，讓 K 棒數維持在百根上下。"""
    if daily_bar_count <= 2:
        return "5m"
    if daily_bar_count <= 10:
        return "30m"
    return "60m"


def fetch_intraday_bars(
    symbol: str,
    start_date: str,
    end_date: str,
    interval: str,
) -> IntradayBars | None:
    """
    下載 [start_date, end_date] 的盤中 K 線（含 end_date 當天）。

    零成交量的 K 棒（例如 IPO 開盤前的占位報價）會被排除。
    超出 Yahoo 盤中資料保留期限、或查無資料時回傳 None，不拋出例外。
    """
    limit_days = _INTRADAY_LOOKBACK_LIMIT_DAYS.get(interval)
    if limit_days is None:
        raise ValueError(f"不支援的盤中週期：{interval}")

    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    earliest_allowed = datetime.now() - timedelta(days=limit_days)
    if end_dt < earliest_allowed:
        logger.info(f"{symbol} 的 {interval} 盤中資料已超出 Yahoo 保留期限，略過")
        return None
    start_dt = max(start_dt, earliest_allowed)

    try:
        # 用 Ticker.history 而非 yf.download：新股的 validRanges 受限時，
        # 部分 yfinance 版本的 yf.download 會誤判為無效區間而回傳空結果
        raw = yf.Ticker(symbol).history(
            start=start_dt.strftime("%Y-%m-%d"),
            end=end_dt.strftime("%Y-%m-%d"),
            interval=interval,
            auto_adjust=False,
            timeout=30,
        )
    except Exception as e:  # 網路或 Yahoo 端錯誤時，讓呼叫端退回日線
        logger.warning(f"下載 {symbol} 的 {interval} 盤中資料失敗：{e}")
        return None

    if raw is None or raw.empty:
        return None

    frame = raw.copy()
    if frame.index.tz is not None:
        # 保留交易所當地時間（例如美東 09:30），只拿掉時區標記
        frame.index = frame.index.tz_localize(None)
    frame = frame.reset_index().rename(columns={frame.index.name or "index": "Date"})
    if "Datetime" in frame.columns:
        frame = frame.rename(columns={"Datetime": "Date"})

    columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    if any(col not in frame.columns for col in columns):
        logger.warning(f"{symbol} 盤中資料欄位不完整：{list(frame.columns)}")
        return None

    frame = frame[columns].dropna(subset=["Open", "High", "Low", "Close"])
    frame = frame[frame["Volume"] > 0].reset_index(drop=True)
    if frame.empty:
        return None
    return IntradayBars(interval=interval, frame=frame)


# 新股的 Yahoo validRanges 可能只開放 1d/5d，長區間 start/end 查詢會被拒絕，
# 這時改用短 period 抓近期日 K（實測 1mo 仍可用）
_RECENT_DAILY_PERIODS = ("1mo", "5d")
_HISTORY_EXTRA_COLUMNS = ("Dividends", "Stock Splits", "Capital Gains")


def _fetch_recent_daily(symbol: str) -> pd.DataFrame:
    ticker = yf.Ticker(symbol)
    for period in _RECENT_DAILY_PERIODS:
        try:
            hist = ticker.history(period=period, auto_adjust=False)
        except Exception as e:
            logger.info(f"{symbol} 以 period={period} 抓日 K 失敗：{e}")
            continue
        if hist is not None and not hist.empty:
            hist = hist.drop(columns=[c for c in _HISTORY_EXTRA_COLUMNS if c in hist.columns])
            if hist.index.tz is not None:
                hist.index = hist.index.tz_localize(None)
            hist.index = hist.index.normalize()
            hist.index.name = "Date"
            return hist
    return pd.DataFrame()


def download_daily(symbol: str, start: str, end: str, timeout: int = 30) -> pd.DataFrame:
    """
    下載 [start, end) 的日 K，格式同 yf.download(multi_level_index=False, auto_adjust=False)。

    長區間查詢對新上市股票可能回傳空結果，此時改抓近期日 K 再裁切到查詢區間。
    """
    data = yf.download(
        symbol,
        start=start,
        end=end,
        multi_level_index=False,
        progress=False,
        auto_adjust=False,
        timeout=timeout,
    )
    if data is not None and not data.empty:
        return data

    recent = _fetch_recent_daily(symbol)
    if recent.empty:
        return pd.DataFrame() if data is None else data
    logger.info(f"{symbol} 長區間日 K 查無資料，改用近期日 K（{len(recent)} 根）")
    in_range = (recent.index >= pd.Timestamp(start)) & (recent.index < pd.Timestamp(end))
    return recent.loc[in_range]


def _session_vwaps(intraday: IntradayBars) -> list[tuple[str, float]]:
    """以盤中 K 線的典型價計算每個交易日的 VWAP。"""
    frame = intraday.frame
    typical = (frame["High"] + frame["Low"] + frame["Close"]) / 3
    by_day = pd.DataFrame(
        {
            "day": frame["Date"].dt.strftime("%Y-%m-%d"),
            "pv": typical * frame["Volume"],
            "volume": frame["Volume"],
        }
    ).groupby("day", sort=True)[["pv", "volume"]].sum()
    return [
        (day, float(row.pv / row.volume))
        for day, row in by_day.iterrows()
        if row.volume > 0
    ]


def summarize_new_listing(
    daily: pd.DataFrame,
    intraday: IntradayBars | None,
) -> str:
    """
    產生上市以來的摘要（Markdown）。

    daily 需含 Open、High、Low、Close、Volume 欄位，索引或 Date 欄為日期，依時間排序。
    """
    frame = daily.reset_index() if "Date" not in daily.columns else daily
    frame = frame.sort_values("Date").reset_index(drop=True)
    first, last = frame.iloc[0], frame.iloc[-1]
    first_day = pd.Timestamp(first["Date"]).strftime("%Y-%m-%d")
    last_day = pd.Timestamp(last["Date"]).strftime("%Y-%m-%d")
    first_open = float(first["Open"])
    first_close = float(first["Close"])
    last_close = float(last["Close"])

    lines = [
        f"## ⚠️ 新上市股票：自 {first_day} 起僅 {len(frame)} 個交易日",
        "日 K 不足以計算 50/200 日均線、MACD、RSI、布林通道等日線指標；"
        "這些指標若顯示 0、50 或等於收盤價，都是資料不足造成，不具訊號意義。",
        "",
        "### 上市以來摘要（由上方日 K 計算）",
        f"- 首個交易日：{first_day}（首日開盤 {first_open:.2f}，收盤 {first_close:.2f}，"
        f"開收變化 {(first_close / first_open - 1) * 100:+.2f}%）",
        f"- 上市以來最高 {float(frame['High'].max()):.2f}，最低 {float(frame['Low'].min()):.2f}",
        f"- 最新收盤 {last_close:.2f}（{last_day}），相對首日開盤 "
        f"{(last_close / first_open - 1) * 100:+.2f}%",
        f"- 平均日成交量 {int(frame['Volume'].mean()):,}",
        "- 注意：首日開盤價不等於 IPO 承銷價，承銷價請以公司公告或新聞查證。",
    ]

    if intraday is not None:
        vwaps = _session_vwaps(intraday)
        if vwaps:
            lines.append("")
            lines.append(f"### 各交易日 VWAP（由 {intraday.interval} 盤中 K 線計算）")
            lines.extend(f"- {day}：{vwap:.2f}" for day, vwap in vwaps)
    return "\n".join(lines)


def format_intraday_csv(intraday: IntradayBars) -> str:
    """把盤中 K 線轉成給 LLM 的 CSV（最多 MAX_INTRADAY_ROWS_FOR_LLM 根，取最新的）。"""
    frame = intraday.frame.tail(MAX_INTRADAY_ROWS_FOR_LLM).copy()
    frame["Date"] = frame["Date"].dt.strftime("%Y-%m-%d %H:%M")
    for col in ("Open", "High", "Low", "Close"):
        frame[col] = frame[col].round(2)
    frame["Volume"] = frame["Volume"].astype("int64")
    header = (
        f"### 盤中 K 線（{intraday.interval}，交易所當地時間，已排除零成交量報價）"
        f"共 {len(intraday.frame)} 根"
    )
    if len(intraday.frame) > len(frame):
        header += f"，以下僅列最新 {len(frame)} 根"
    return header + "\n" + frame.to_csv(index=False)


def build_new_listing_report(
    symbol: str,
    daily: pd.DataFrame,
    end_date: str,
) -> str:
    """
    新上市股票的補充段落：上市摘要 + 盤中 K 線。daily 為日 K（已依日期排序）。
    """
    frame = daily.reset_index() if "Date" not in daily.columns else daily
    first_day = pd.Timestamp(frame["Date"].min()).strftime("%Y-%m-%d")
    interval = pick_intraday_interval(len(frame))
    intraday = fetch_intraday_bars(symbol, first_day, end_date, interval)

    sections = [summarize_new_listing(frame, intraday)]
    if intraday is not None:
        sections.append(format_intraday_csv(intraday))
    else:
        sections.append(
            "### 盤中 K 線：無法取得（可能超出 Yahoo 盤中資料保留期限），請以日 K 為準並標示資料缺口。"
        )
    return "\n\n".join(sections)
