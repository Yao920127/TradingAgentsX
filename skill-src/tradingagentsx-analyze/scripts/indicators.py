#!/usr/bin/env python3
"""離線技術指標＋日線資料驗證（純 Python，不需連網、不需 pandas）。

用途：Claude 用自己的網頁工具取得日線後，先存成 CSV／JSON，再用本腳本
  1. 驗證資料（欄位、日期、排序、高低價是否矛盾）
  2. 以 --expect-rows／--expect-close-sum 核對「抄寫」是否漏列或抄錯
  3. 計算與網頁版市場分析師相同的指標組合
  4. 寫出 <workdir>/price_data.json（給 render_pdf.py 畫走勢圖）與 indicators.json

用法：
  python indicators.py --input ohlcv.csv|json --workdir <資料夾> \
      [--expect-rows N] [--expect-close-sum S] [--lookback 30]

輸入欄位：Date(YYYY-MM-DD), Open, High, Low, Close, Volume；日期須由舊到新且不重複。
stdout 只輸出一份 JSON 摘要；錯誤訊息走 stderr。
結束碼：0 成功；5 資料格式或內容錯誤；6 參數不合法；7 與預期筆數／總和不符。
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Sequence

REQUIRED_COLUMNS = ("Date", "Open", "High", "Low", "Close", "Volume")
INDICATORS = (
    "close_50_sma", "close_200_sma", "close_10_ema",
    "macd", "macds", "macdh",
    "rsi", "boll", "boll_ub", "boll_lb",
    "atr", "vwma", "mfi",
)
SUM_TOLERANCE = 0.005  # 收盤價總和的容許誤差（四捨五入）
PRICE_TOLERANCE = 1e-6  # 高低價包含收盤／開盤時的相對容許誤差
RSI_PERIOD = 14
ATR_PERIOD = 14
MFI_PERIOD = 14
BOLL_PERIOD = 20
BOLL_WIDTH = 2.0
VWMA_PERIOD = 14  # 與 stockstats 預設一致


class IndicatorError(Exception):
    """可預期的失敗；code 即命令列的結束碼。"""

    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code


# ---------- 讀取與驗證 ----------

def load_ohlcv(path: Path) -> list[dict[str, Any]]:
    """讀取 CSV 或 JSON 並驗證，回傳正規化後的列。"""
    path = Path(path)
    if not path.is_file():
        raise IndicatorError(5, f"找不到輸入檔：{path}")
    try:
        if path.suffix.lower() == ".csv":
            with path.open(newline="", encoding="utf-8-sig") as fh:
                raw = list(csv.DictReader(fh))
        else:
            payload = json.loads(path.read_text(encoding="utf-8"))
            raw = payload.get("price_data") if isinstance(payload, dict) else payload
    except (json.JSONDecodeError, UnicodeDecodeError, csv.Error) as exc:
        raise IndicatorError(5, f"無法解析 {path.name}：{exc}") from exc
    return validate_rows(raw)


def _to_float(value: Any, column: str, index: int) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise IndicatorError(5, f"第 {index} 列 {column} 不是數字：{value!r}") from exc
    if not math.isfinite(number):
        raise IndicatorError(5, f"第 {index} 列 {column} 不是有限數字：{value!r}")
    return number


def _validate_row(index: int, row: Any) -> dict[str, Any]:
    if not isinstance(row, dict):
        raise IndicatorError(5, f"第 {index} 列不是物件")
    absent = [c for c in REQUIRED_COLUMNS if c not in row or row[c] in (None, "")]
    if absent:
        raise IndicatorError(5, f"第 {index} 列缺少欄位：{', '.join(absent)}")
    date = str(row["Date"]).strip()
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError as exc:
        raise IndicatorError(5, f"第 {index} 列日期必須是 YYYY-MM-DD：{date!r}") from exc

    open_, high, low, close, volume = (
        _to_float(row[c], c, index) for c in ("Open", "High", "Low", "Close", "Volume")
    )
    if min(open_, high, low, close) <= 0:
        raise IndicatorError(5, f"第 {index} 列（{date}）價格必須大於 0")
    if volume < 0:
        raise IndicatorError(5, f"第 {index} 列（{date}）成交量不可為負")
    slack = high * PRICE_TOLERANCE
    if high + slack < low:
        raise IndicatorError(5, f"第 {index} 列（{date}）最高價 {high} 低於最低價 {low}")
    for name, price in (("Open", open_), ("Close", close)):
        if price > high + slack or price < low - slack:
            raise IndicatorError(5, f"第 {index} 列（{date}）{name} {price} 超出最高／最低價範圍")
    return {"Date": date, "Open": open_, "High": high, "Low": low, "Close": close, "Volume": volume}


def validate_rows(raw: Any) -> list[dict[str, Any]]:
    """驗證並回傳新列表；不修改輸入。"""
    if not isinstance(raw, list) or not raw:
        raise IndicatorError(5, "沒有任何日線資料（需要非空的陣列）")
    rows = [_validate_row(i, r) for i, r in enumerate(raw)]
    for prev, cur in zip(rows, rows[1:]):
        if cur["Date"] == prev["Date"]:
            raise IndicatorError(5, f"日期重複：{cur['Date']}")
        if cur["Date"] < prev["Date"]:
            raise IndicatorError(5, f"日期未由舊到新排序：{prev['Date']} 之後是 {cur['Date']}")
    return rows


def check_expectations(
    rows: Sequence[dict[str, Any]],
    expect_rows: Optional[int] = None,
    expect_close_sum: Optional[float] = None,
) -> None:
    """與來源回報的筆數／收盤價總和核對，抓出轉寫漏列或抄錯。"""
    if expect_rows is not None and len(rows) != expect_rows:
        raise IndicatorError(7, f"筆數不符：預期 {expect_rows}，實際 {len(rows)}")
    if expect_close_sum is not None:
        actual = math.fsum(r["Close"] for r in rows)
        if abs(actual - expect_close_sum) > SUM_TOLERANCE:
            raise IndicatorError(
                7, f"收盤價總和不符：預期 {expect_close_sum}，實際 {actual:.4f}（可能有漏列或抄錯）"
            )


# ---------- 指標（皆回傳與輸入等長的 list，資料不足處為 None） ----------

def _sma(values: Sequence[float], period: int) -> list[Optional[float]]:
    out: list[Optional[float]] = [None] * len(values)
    for i in range(period - 1, len(values)):
        out[i] = math.fsum(values[i - period + 1: i + 1]) / period
    return out


def _ema(values: Sequence[float], period: int) -> list[float]:
    alpha = 2 / (period + 1)
    out: list[float] = []
    for value in values:
        out.append(value if not out else alpha * value + (1 - alpha) * out[-1])
    return out


def _mask_before(values: Sequence[float], first_valid: int) -> list[Optional[float]]:
    return [v if i >= first_valid else None for i, v in enumerate(values)]


def _wilder(values: Sequence[float], period: int, first: int) -> list[Optional[float]]:
    """Wilder 平滑：values[first : first+period] 的平均為起點。"""
    out: list[Optional[float]] = [None] * len(values)
    start = first + period - 1
    if start >= len(values):
        return out
    out[start] = math.fsum(values[first: first + period]) / period
    for i in range(start + 1, len(values)):
        out[i] = (out[i - 1] * (period - 1) + values[i]) / period  # type: ignore[operator]
    return out


def _rsi(closes: Sequence[float]) -> list[Optional[float]]:
    diffs = [0.0] + [b - a for a, b in zip(closes, closes[1:])]
    gains = [max(d, 0.0) for d in diffs]
    losses = [max(-d, 0.0) for d in diffs]
    avg_gain = _wilder(gains, RSI_PERIOD, 1)
    avg_loss = _wilder(losses, RSI_PERIOD, 1)
    out: list[Optional[float]] = []
    for gain, loss in zip(avg_gain, avg_loss):
        if gain is None or loss is None or (gain == 0 and loss == 0):
            out.append(None)
        elif loss == 0:
            out.append(100.0)
        else:
            out.append(100 - 100 / (1 + gain / loss))
    return out


def _macd(closes: Sequence[float]) -> tuple[list, list, list]:
    fast, slow = _ema(closes, 12), _ema(closes, 26)
    line = [f - s for f, s in zip(fast, slow)]
    macd_valid = 26 - 1
    signal = _ema(line[macd_valid:], 9)
    macds: list[Optional[float]] = [None] * len(closes)
    macdh: list[Optional[float]] = [None] * len(closes)
    macd = _mask_before(line, macd_valid)
    signal_valid = macd_valid + 9 - 1
    for offset, value in enumerate(signal):
        i = macd_valid + offset
        if i >= signal_valid and i < len(closes):
            macds[i] = value
            macdh[i] = line[i] - value
    return macd, macds, macdh


def _bollinger(closes: Sequence[float]) -> tuple[list, list, list]:
    middle: list[Optional[float]] = [None] * len(closes)
    upper: list[Optional[float]] = [None] * len(closes)
    lower: list[Optional[float]] = [None] * len(closes)
    for i in range(BOLL_PERIOD - 1, len(closes)):
        window = closes[i - BOLL_PERIOD + 1: i + 1]
        mean = math.fsum(window) / BOLL_PERIOD
        std = math.sqrt(math.fsum((c - mean) ** 2 for c in window) / BOLL_PERIOD)  # 母體標準差，與 stockstats 一致
        middle[i], upper[i], lower[i] = mean, mean + BOLL_WIDTH * std, mean - BOLL_WIDTH * std
    return middle, upper, lower


def _atr(rows: Sequence[dict[str, Any]]) -> list[Optional[float]]:
    ranges = [rows[0]["High"] - rows[0]["Low"]]
    for prev, cur in zip(rows, rows[1:]):
        ranges.append(max(
            cur["High"] - cur["Low"],
            abs(cur["High"] - prev["Close"]),
            abs(cur["Low"] - prev["Close"]),
        ))
    return _wilder(ranges, ATR_PERIOD, 0)


def _typical(row: dict[str, Any]) -> float:
    return (row["High"] + row["Low"] + row["Close"]) / 3


def _vwma(rows: Sequence[dict[str, Any]]) -> list[Optional[float]]:
    out: list[Optional[float]] = [None] * len(rows)
    for i in range(VWMA_PERIOD - 1, len(rows)):
        window = rows[i - VWMA_PERIOD + 1: i + 1]
        volume = math.fsum(r["Volume"] for r in window)
        if volume > 0:
            out[i] = math.fsum(_typical(r) * r["Volume"] for r in window) / volume  # 典型價格加權，同 stockstats
    return out


def _mfi(rows: Sequence[dict[str, Any]]) -> list[Optional[float]]:
    typical = [(r["High"] + r["Low"] + r["Close"]) / 3 for r in rows]
    flow = [t * r["Volume"] for t, r in zip(typical, rows)]
    out: list[Optional[float]] = [None] * len(rows)
    for i in range(MFI_PERIOD, len(rows)):
        positive = negative = 0.0
        for j in range(i - MFI_PERIOD + 1, i + 1):
            if typical[j] > typical[j - 1]:
                positive += flow[j]
            elif typical[j] < typical[j - 1]:
                negative += flow[j]
        if positive == 0 and negative == 0:
            continue
        out[i] = 100.0 if negative == 0 else 100 - 100 / (1 + positive / negative)
    return out


def compute_indicators(rows: Sequence[dict[str, Any]]) -> dict[str, list[Optional[float]]]:
    """計算網頁版市場分析師使用的指標組合。"""
    closes = [r["Close"] for r in rows]
    macd, macds, macdh = _macd(closes)
    boll, boll_ub, boll_lb = _bollinger(closes)
    return {
        "close_50_sma": _sma(closes, 50),
        "close_200_sma": _sma(closes, 200),
        "close_10_ema": _mask_before(_ema(closes, 10), 10 - 1),
        "macd": macd, "macds": macds, "macdh": macdh,
        "rsi": _rsi(closes),
        "boll": boll, "boll_ub": boll_ub, "boll_lb": boll_lb,
        "atr": _atr(rows),
        "vwma": _vwma(rows),
        "mfi": _mfi(rows),
    }


# ---------- 摘要與輸出 ----------

def _round(value: Optional[float]) -> Optional[float]:
    return None if value is None else round(value, 4)


def summarize(
    rows: Sequence[dict[str, Any]],
    table: dict[str, list[Optional[float]]],
    lookback: int = 30,
) -> dict[str, Any]:
    start = max(len(rows) - max(lookback, 1), 0)
    recent = [
        {"Date": rows[i]["Date"], "Close": rows[i]["Close"],
         **{name: _round(table[name][i]) for name in INDICATORS}}
        for i in range(start, len(rows))
    ]
    return {
        "rows": len(rows),
        "start_date": rows[0]["Date"],
        "latest_date": rows[-1]["Date"],
        "latest_close": rows[-1]["Close"],
        "close_sum": round(math.fsum(r["Close"] for r in rows), 4),
        "latest": recent[-1],
        "recent": recent,
    }


def price_stats(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    first, last = rows[0], rows[-1]
    start, end = first["Close"], last["Close"]
    duration = (
        datetime.strptime(last["Date"], "%Y-%m-%d") - datetime.strptime(first["Date"], "%Y-%m-%d")
    ).days
    return {
        "growth_rate": (end - start) / start * 100,
        "duration_days": duration,
        "start_date": first["Date"],
        "end_date": last["Date"],
        "start_price": start,
        "end_price": end,
    }


def _clean_number(value: float) -> Any:
    return int(value) if float(value).is_integer() else value


def write_outputs(
    workdir: Path,
    rows: Sequence[dict[str, Any]],
    table: dict[str, list[Optional[float]]],
) -> tuple[Path, Path]:
    workdir.mkdir(parents=True, exist_ok=True)
    price_rows = [{**r, "Volume": _clean_number(r["Volume"])} for r in rows]
    price_path = workdir / "price_data.json"
    price_path.write_text(
        json.dumps({"price_data": price_rows, "price_stats": price_stats(rows)}, ensure_ascii=False),
        encoding="utf-8",
    )
    indicator_path = workdir / "indicators.json"
    indicator_path.write_text(
        json.dumps(
            {"dates": [r["Date"] for r in rows],
             "indicators": {k: [_round(v) for v in series] for k, series in table.items()}},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return price_path, indicator_path


class _Parser(argparse.ArgumentParser):
    def error(self, message: str):  # type: ignore[override]
        raise IndicatorError(6, message)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _Parser(description="驗證日線資料並計算技術指標")
    parser.add_argument("--input", required=True, type=Path, help="OHLCV 的 CSV 或 JSON")
    parser.add_argument("--workdir", required=True, type=Path)
    parser.add_argument("--expect-rows", type=int, default=None, help="來源回報的筆數")
    parser.add_argument("--expect-close-sum", type=float, default=None, help="來源收盤價總和")
    parser.add_argument("--lookback", type=int, default=30, help="摘要中保留最近幾筆")
    try:
        args = parser.parse_args(argv)
        rows = load_ohlcv(args.input)
        check_expectations(rows, args.expect_rows, args.expect_close_sum)
        table = compute_indicators(rows)
        price_path, indicator_path = write_outputs(args.workdir, rows, table)
        summary = {
            **summarize(rows, table, args.lookback),
            "price_data": str(price_path),
            "indicators": str(indicator_path),
        }
    except IndicatorError as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return exc.code
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
