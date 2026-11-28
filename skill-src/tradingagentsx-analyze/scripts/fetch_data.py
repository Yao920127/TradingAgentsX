#!/usr/bin/env python3
"""腳本模式的資料蒐集：用 TradingAgentsX 的 dataflows 抓四類分析所需的資料。

用法：
  python fetch_data.py --ticker NVDA --date 2026-11-26 --market us --workdir <資料夾>
  python fetch_data.py --ticker 2330 --date 2026-11-26 --market twse --workdir <資料夾>

寫出（<workdir>/data/）：
  price.csv         日線 OHLCV（交給 indicators.py）
  fundamentals.md   基本面＋資產負債表＋現金流量表＋損益表（季）
  news.md           個股新聞（近 7 天）＋全球新聞
  social.md         社群情緒＋個股新聞

單一類別失敗只會在檔案內標示「資料缺口」並列入摘要的 gaps；價格取不到才算失敗。
stdout 只輸出一份 JSON 摘要；進度與錯誤走 stderr。

結束碼：0 成功（可能含資料缺口）；3 找不到 dataflows；6 參數不合法；
        8 網路被擋（例如 Claude app 容器），請改走網頁工具模式；9 取不到價格資料。
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Optional, Sequence

SKILL_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SKILL_DIR.parent.parent

MARKETS = ("us", "twse", "tpex")
PRICE_WINDOW_DAYS = 365  # 與 app 的 get_stock_data 最低區間一致
NEWS_WINDOW_DAYS = 7
GLOBAL_NEWS_LIMIT = 5
SOCIAL_LOOKBACK_DAYS = 7
PROBE_TIMEOUT_SECONDS = 8
PROBE_URLS = {
    "us": "https://query1.finance.yahoo.com/v8/finance/chart/AAPL?range=1d",
    "twse": "https://api.finmindtrade.com/api/v4/data",
    "tpex": "https://api.finmindtrade.com/api/v4/data",
}
PRICE_HEADER = ("Date", "Open", "High", "Low", "Close", "Volume")
# 供應商有時把錯誤當成一般字串回傳；以開頭判斷為資料缺口
_ERROR_PREFIX = re.compile(
    r"^\s*(error|錯誤|找不到|無法|獲取.{0,20}(失敗|出錯)|no data|rate limit)", re.IGNORECASE
)
# 結構化回傳但內容為空（例如 FinMind 的 `items: 0`／`feed: []`）也算缺口
_EMPTY_PAYLOAD = re.compile(r"^\s*(items:\s*0\s*$|feed:\s*\[\s*\]\s*$)", re.MULTILINE)


class FetchError(Exception):
    """可預期的失敗；code 即命令列的結束碼。"""

    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code


Call = Callable[..., Any]  # call(method, *args) -> str，簽名同 route_to_vendor


# ---------- 設定 ----------

def vendor_config(market: str) -> dict[str, Any]:
    """與 backend/app/services/trading_service.py 相同的供應商設定；美股沿用預設。"""
    if market not in ("twse", "tpex"):
        return {}
    return {
        "data_vendors": {
            "core_stock_apis": "finmind",
            "technical_indicators": "finmind",
            "fundamental_data": "finmind",
            "news_data": "finmind,aggregator",
            "social_data": "aggregator",
        },
        "tool_vendors": {
            "get_stock_data": "finmind",
            "get_indicators": "finmind",
            "get_fundamentals": "finmind",
            "get_balance_sheet": "finmind",
            "get_cashflow": "finmind",
            "get_income_statement": "finmind",
            "get_news": "finmind,aggregator",
            "get_global_news": "finmind,aggregator",
            "get_insider_sentiment": "finmind",
            "get_insider_transactions": "finmind",
        },
        "market_type": market,
    }


def normalize_ticker(ticker: str, market: str) -> str:
    cleaned = ticker.strip().upper()
    if market in ("twse", "tpex"):
        cleaned = re.sub(r"\.(TWO?|TPEX)$", "", cleaned)
    return cleaned


# ---------- 價格解析 ----------

def _to_number(text: str) -> Optional[float]:
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def parse_price_csv(text: str) -> list[dict[str, Any]]:
    """解析 yfinance／FinMind 的價格 CSV；忽略 # 註解、空行之後的補充段落與缺值列。"""
    lines = [ln for ln in text.splitlines() if not ln.lstrip().startswith("#")]
    header_at = next((i for i, ln in enumerate(lines) if ln.lower().startswith("date,")), None)
    if header_at is None:
        return []
    block: list[str] = []
    for line in lines[header_at:]:
        if not line.strip():
            break  # 空行之後是新上市摘要等補充文字
        block.append(line)
    reader = csv.DictReader(io.StringIO("\n".join(block)))
    rows: list[dict[str, Any]] = []
    for record in reader:
        lowered = {(k or "").strip().lower(): v for k, v in record.items()}
        values = [_to_number(lowered.get(c.lower(), "")) for c in PRICE_HEADER[1:]]
        date = (lowered.get("date") or "").strip()[:10]
        if not date or any(v is None for v in values):
            continue
        rows.append({"Date": date, **dict(zip(PRICE_HEADER[1:], values))})
    return rows


def _write_price_csv(path: Path, rows: Sequence[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(PRICE_HEADER)
        for r in rows:
            volume = r["Volume"]
            writer.writerow([r["Date"], r["Open"], r["High"], r["Low"], r["Close"],
                             int(volume) if float(volume).is_integer() else volume])


# ---------- 蒐集 ----------

def _validate(ticker: str, date: str, market: str) -> datetime:
    if market not in MARKETS:
        raise FetchError(6, f"--market 只能是 {'、'.join(MARKETS)}，收到：{market!r}")
    if not ticker.strip():
        raise FetchError(6, "--ticker 不可為空")
    try:
        return datetime.strptime(date, "%Y-%m-%d")
    except ValueError as exc:
        raise FetchError(6, f"--date 必須是 YYYY-MM-DD，收到：{date!r}") from exc


def _fetch_text(call: Call, name: str, method: str, *args: Any) -> tuple[Optional[str], Optional[str]]:
    """回傳 (文字, 缺口原因)；兩者必有一個為 None。"""
    try:
        text = call(method, *args)
    except Exception as exc:  # 供應商例外種類繁多，一律視為該類別缺口
        print(f"[fetch_data] {name} 失敗：{type(exc).__name__}: {exc}", file=sys.stderr)
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(text, str) or not text.strip():
        return None, "供應商回傳空結果"
    if _ERROR_PREFIX.match(text):
        return None, text.strip().splitlines()[0][:200]
    if _EMPTY_PAYLOAD.search(text):
        return None, "供應商回傳空內容（items: 0）"
    return text, None


def _section(title: str, text: Optional[str], reason: Optional[str]) -> str:
    body = text if text is not None else f"資料缺口 / Data gap：{title} 無法取得（{reason}）"
    return f"## {title}\n\n{body.strip()}\n"


def _write_md(path: Path, heading: str, sections: Sequence[str]) -> None:
    path.write_text(f"# {heading}\n\n" + "\n".join(sections), encoding="utf-8")


def collect(workdir: Path, ticker: str, date: str, market: str, call: Call,
            price_days: int = PRICE_WINDOW_DAYS) -> dict[str, Any]:
    """蒐集資料並寫入 <workdir>/data/；價格失敗拋 FetchError(9)。"""
    end = _validate(ticker, date, market)
    symbol = normalize_ticker(ticker, market)
    data_dir = Path(workdir) / "data"

    price_start = (end - timedelta(days=price_days)).strftime("%Y-%m-%d")
    price_text, price_reason = _fetch_text(call, "price", "get_stock_data", symbol, price_start, date)
    rows = parse_price_csv(price_text) if price_text else []
    if not rows:
        hint = ""
        if market in ("twse", "tpex") and not (os.environ.get("FINMIND_API_TOKEN") or os.environ.get("FINMIND_API_KEY")):
            hint = "；未設定環境變數 FINMIND_API_TOKEN（FinMind 需要 Token，請至 finmindtrade.com 申請）"
        raise FetchError(9, f"取不到 {symbol} 的價格資料（{price_reason or '解析後沒有任何有效列'}）{hint}")

    news_start = (end - timedelta(days=NEWS_WINDOW_DAYS)).strftime("%Y-%m-%d")
    fetched = {
        "fundamentals": _fetch_text(call, "fundamentals", "get_fundamentals", symbol, date),
        "balance_sheet": _fetch_text(call, "balance_sheet", "get_balance_sheet", symbol, "quarterly", date),
        "cashflow": _fetch_text(call, "cashflow", "get_cashflow", symbol, "quarterly", date),
        "income_statement": _fetch_text(call, "income_statement", "get_income_statement", symbol, "quarterly", date),
        "news": _fetch_text(call, "news", "get_news", symbol, news_start, date),
        "global_news": _fetch_text(call, "global_news", "get_global_news", date, NEWS_WINDOW_DAYS, GLOBAL_NEWS_LIMIT),
        "social_sentiment": _fetch_text(call, "social_sentiment", "get_social_sentiment",
                                        symbol, date, SOCIAL_LOOKBACK_DAYS),
    }

    data_dir.mkdir(parents=True, exist_ok=True)
    _write_price_csv(data_dir / "price.csv", rows)
    section = lambda key, title: _section(title, *fetched[key])  # noqa: E731
    _write_md(data_dir / "fundamentals.md", f"{symbol} 基本面資料 / Fundamentals ({date})", [
        section("fundamentals", "公司基本面 Company fundamentals"),
        section("balance_sheet", "資產負債表（季）Balance sheet"),
        section("cashflow", "現金流量表（季）Cash flow"),
        section("income_statement", "損益表（季）Income statement"),
    ])
    _write_md(data_dir / "news.md", f"{symbol} 新聞資料 / News ({news_start} ~ {date})", [
        section("news", "個股新聞 Company news"),
        section("global_news", "全球新聞 Global news"),
    ])
    _write_md(data_dir / "social.md", f"{symbol} 社群情緒 / Social sentiment ({date})", [
        section("social_sentiment", "社群情緒 Social sentiment"),
        section("news", "個股新聞 Company news"),
    ])

    return {
        "ticker": symbol,
        "market": market,
        "date": date,
        "price_rows": len(rows),
        "price_start": rows[0]["Date"],
        "price_end": rows[-1]["Date"],
        "gaps": [key for key, (_, reason) in fetched.items() if reason is not None],
        "gap_reasons": {key: reason for key, (_, reason) in fetched.items() if reason is not None},
        "files": {name: str(data_dir / f"{name}.{ext}") for name, ext in
                  (("price", "csv"), ("fundamentals", "md"), ("news", "md"), ("social", "md"))},
    }


# ---------- 網路偵測與實際呼叫 ----------

def network_blocked(market: str, opener: Optional[Callable[..., Any]] = None) -> bool:
    """連不上，或被 agent proxy 以 403 擋下，都視為被擋。其他 HTTP 回應都算可連線。"""
    open_url = opener or (lambda url, timeout: urllib.request.urlopen(url, timeout=timeout))
    try:
        response = open_url(PROBE_URLS[market], timeout=PROBE_TIMEOUT_SECONDS)
        response.close()
        return False
    except urllib.error.HTTPError as exc:
        body = exc.read()[:200] if hasattr(exc, "read") else b""
        return exc.code == 403 and b"agent proxy" in body.lower()
    except (urllib.error.URLError, OSError):
        return True


def make_vendor_call(market: str) -> Call:
    """載入 dataflows 並套用市場設定，回傳 route_to_vendor。"""
    for candidate in (SKILL_DIR / "vendor", REPO_ROOT):
        if (candidate / "tradingagents").is_dir():
            sys.path.insert(0, str(candidate))
            break
    else:
        raise FetchError(3, f"找不到 tradingagents 套件（已找過 {SKILL_DIR / 'vendor'} 與 {REPO_ROOT}）")
    try:
        from tradingagents.dataflows.config import set_config
        from tradingagents.dataflows.interface import route_to_vendor
    except ImportError as exc:
        raise FetchError(3, f"載入 dataflows 失敗：{exc}") from exc
    config = vendor_config(market)
    if config:
        set_config(config)
    return route_to_vendor


class _Parser(argparse.ArgumentParser):
    def error(self, message: str):  # type: ignore[override]
        raise FetchError(6, message)


def main(argv: Optional[Sequence[str]] = None, call: Optional[Call] = None,
         probe: Optional[Callable[[str], bool]] = None) -> int:
    parser = _Parser(description="蒐集股票分析所需資料")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--date", required=True, help="分析日期 YYYY-MM-DD")
    parser.add_argument("--market", default="us", help="us、twse（上市）或 tpex（上櫃/興櫃）")
    parser.add_argument("--workdir", required=True, type=Path)
    parser.add_argument("--price-days", type=int, default=PRICE_WINDOW_DAYS)
    try:
        args = parser.parse_args(argv)
        _validate(args.ticker, args.date, args.market)
        if (probe or network_blocked)(args.market):
            raise FetchError(8, "連不到資料來源（網路被擋）。請改用網頁工具模式，由 Claude 自行蒐集資料")
        with contextlib.redirect_stdout(sys.stderr):  # dataflows 會大量 print 除錯訊息
            vendor_call = call or make_vendor_call(args.market)
            result = collect(args.workdir, args.ticker, args.date, args.market, vendor_call,
                             price_days=args.price_days)
    except FetchError as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return exc.code
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
