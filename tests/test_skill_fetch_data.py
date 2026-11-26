"""skills/tradingagentsx-analyze/scripts/fetch_data.py 的測試。

以注入的假取資料函式驗證（不連網）：
  - 價格 CSV 解析（yfinance 帶註解標頭與補充段落、FinMind 小寫欄位）
  - 各市場的資料供應商設定與 app 一致
  - 依序呼叫 app 的工具並寫出 price.csv／fundamentals.md／news.md／social.md
  - 單一資料類型失敗只標示資料缺口；價格取不到才算失敗
  - 網路被擋（Claude app 容器）時回傳專用結束碼 8
"""
import importlib.util
import io
import json
import urllib.error
from pathlib import Path

import pytest

SCRIPT = (
    Path(__file__).resolve().parent.parent
    / "skills" / "tradingagentsx-analyze" / "scripts" / "fetch_data.py"
)

YF_TEXT = (
    "# NVDA 從 2025-11-26 到 2026-11-26 的股票數據\n"
    "# 總記錄數：3\n"
    "# 數據檢索時間：2026-11-26 10:00:00\n\n"
    "Date,Open,High,Low,Close,Adj Close,Volume,Dividends,Stock Splits\n"
    "2026-11-23 00:00:00,150.0,152.0,148.0,151.0,151.0,1000,0.0,0.0\n"
    "2026-11-24 00:00:00,151.0,153.0,149.5,152.5,152.5,1100,0.0,0.0\n"
    "2026-11-25 00:00:00,152.5,154.0,150.0,153.0,153.0,1200,0.0,0.0\n"
    "\n\n## 新上市摘要\n第一日開盤 1\n"
)

FM_TEXT = (
    "date,open,high,low,close,volume\n"
    "2026-11-24,1000,1010,990,1005,50000\n"
    "2026-11-25,1005,1020,1000,1015,60000\n"
)


@pytest.fixture(scope="module")
def fd():
    spec = importlib.util.spec_from_file_location("ta_fetch_data", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeCalls:
    """記錄呼叫並依方法回傳預設字串；值為例外時拋出。"""

    def __init__(self, price_text=YF_TEXT, overrides=None):
        self.calls = []
        self.replies = {
            "get_stock_data": price_text,
            "get_fundamentals": "PE=25",
            "get_balance_sheet": "BALANCE",
            "get_cashflow": "CASHFLOW",
            "get_income_statement": "INCOME",
            "get_news": "NEWS-ITEMS",
            "get_global_news": "GLOBAL-NEWS",
            "get_social_sentiment": "SOCIAL-SENTIMENT",
        }
        self.replies.update(overrides or {})

    def __call__(self, method, *args):
        self.calls.append((method, args))
        reply = self.replies[method]
        if isinstance(reply, Exception):
            raise reply
        return reply


# ---------- 價格解析 ----------

def test_parse_yfinance_csv_with_header_comments_and_supplement(fd):
    rows = fd.parse_price_csv(YF_TEXT)
    assert [r["Date"] for r in rows] == ["2026-11-23", "2026-11-24", "2026-11-25"]
    assert rows[0] == {"Date": "2026-11-23", "Open": 150.0, "High": 152.0,
                       "Low": 148.0, "Close": 151.0, "Volume": 1000.0}


def test_parse_finmind_lowercase_csv(fd):
    rows = fd.parse_price_csv(FM_TEXT)
    assert len(rows) == 2
    assert rows[1]["Close"] == 1015.0 and rows[1]["Volume"] == 60000.0


def test_parse_empty_or_header_only_returns_empty(fd):
    assert fd.parse_price_csv("date,open,high,low,close,volume\n") == []
    assert fd.parse_price_csv("找不到 'XXXX' 在 a 和 b 之間的數據") == []
    assert fd.parse_price_csv("") == []


def test_parse_skips_rows_with_missing_values(fd):
    text = FM_TEXT + "2026-11-26,,,,,\n"
    assert len(fd.parse_price_csv(text)) == 2


# ---------- 供應商設定 ----------

def test_us_config_keeps_defaults(fd):
    assert fd.vendor_config("us") == {}


@pytest.mark.parametrize("market", ["twse", "tpex"])
def test_taiwan_config_uses_finmind(fd, market):
    cfg = fd.vendor_config(market)
    assert cfg["data_vendors"]["core_stock_apis"] == "finmind"
    assert cfg["data_vendors"]["news_data"] == "finmind,aggregator"
    assert cfg["tool_vendors"]["get_news"] == "finmind,aggregator"
    assert cfg["market_type"] == market


# ---------- 蒐集流程 ----------

def test_collect_writes_all_files_and_calls_app_tools(fd, tmp_path):
    call = FakeCalls()
    result = fd.collect(tmp_path, "nvda", "2026-11-26", "us", call)

    methods = [m for m, _ in call.calls]
    assert methods[0] == "get_stock_data"
    assert {"get_fundamentals", "get_balance_sheet", "get_cashflow", "get_income_statement",
            "get_news", "get_global_news", "get_social_sentiment"} <= set(methods)
    assert call.calls[0][1][0] == "NVDA"  # 美股代碼轉大寫
    data = tmp_path / "data"
    assert (data / "price.csv").read_text(encoding="utf-8").splitlines()[0] == \
        "Date,Open,High,Low,Close,Volume"
    fundamentals = (data / "fundamentals.md").read_text(encoding="utf-8")
    for token in ("PE=25", "BALANCE", "CASHFLOW", "INCOME"):
        assert token in fundamentals
    news = (data / "news.md").read_text(encoding="utf-8")
    assert "NEWS-ITEMS" in news and "GLOBAL-NEWS" in news
    social = (data / "social.md").read_text(encoding="utf-8")
    assert "SOCIAL-SENTIMENT" in social
    assert result["gaps"] == []
    assert result["price_rows"] == 3
    assert result["ticker"] == "NVDA"


def test_collect_price_window_is_at_least_one_year(fd, tmp_path):
    call = FakeCalls()
    fd.collect(tmp_path, "NVDA", "2026-11-26", "us", call)
    _, (_, start, end) = call.calls[0]
    assert end == "2026-11-26"
    assert start <= "2025-11-26"


def test_collect_news_window_is_seven_days(fd, tmp_path):
    call = FakeCalls()
    fd.collect(tmp_path, "NVDA", "2026-11-26", "us", call)
    news_call = next(args for m, args in call.calls if m == "get_news")
    assert news_call == ("NVDA", "2026-11-19", "2026-11-26")


def test_taiwan_ticker_keeps_digits_and_strips_suffix(fd, tmp_path):
    call = FakeCalls(price_text=FM_TEXT)
    result = fd.collect(tmp_path, "2330.TW", "2026-11-26", "twse", call)
    assert call.calls[0][1][0] == "2330"
    assert result["ticker"] == "2330"


def test_failed_category_becomes_gap_but_run_continues(fd, tmp_path):
    call = FakeCalls(overrides={"get_social_sentiment": RuntimeError("boom"),
                                "get_global_news": ""})
    result = fd.collect(tmp_path, "NVDA", "2026-11-26", "us", call)

    assert set(result["gaps"]) == {"social_sentiment", "global_news"}
    social = (tmp_path / "data" / "social.md").read_text(encoding="utf-8")
    assert "資料缺口" in social
    assert "NEWS-ITEMS" in social  # 社群分析仍附上個股新聞
    assert "資料缺口" in (tmp_path / "data" / "news.md").read_text(encoding="utf-8")


def test_error_text_returned_as_data_counts_as_gap(fd, tmp_path):
    call = FakeCalls(overrides={"get_fundamentals": "Error: rate limit exceeded"})
    result = fd.collect(tmp_path, "NVDA", "2026-11-26", "us", call)
    assert "fundamentals" in result["gaps"]


@pytest.mark.parametrize("empty_feed", [
    "market: Taiwan\nitems: 0\nnote: FinMind 不提供新聞 API\nfeed: []",
    "feed: []",
])
def test_empty_feed_payload_counts_as_gap(fd, tmp_path, empty_feed):
    call = FakeCalls(overrides={"get_global_news": empty_feed})
    result = fd.collect(tmp_path, "NVDA", "2026-11-26", "us", call)
    assert "global_news" in result["gaps"]
    assert "資料缺口" in (tmp_path / "data" / "news.md").read_text(encoding="utf-8")


def test_missing_price_raises_exit_code_9(fd, tmp_path):
    call = FakeCalls(price_text="date,open,high,low,close,volume\n")
    with pytest.raises(fd.FetchError) as exc:
        fd.collect(tmp_path, "NVDA", "2026-11-26", "us", call)
    assert exc.value.code == 9


def test_taiwan_price_failure_hints_missing_finmind_token(fd, tmp_path, monkeypatch):
    monkeypatch.delenv("FINMIND_API_TOKEN", raising=False)
    monkeypatch.delenv("FINMIND_API_KEY", raising=False)
    call = FakeCalls(price_text="date,open,high,low,close,volume\n")
    with pytest.raises(fd.FetchError) as exc:
        fd.collect(tmp_path, "2330", "2026-11-26", "twse", call)
    assert "FINMIND_API_TOKEN" in str(exc.value)


def test_price_exception_raises_exit_code_9(fd, tmp_path):
    call = FakeCalls(overrides={"get_stock_data": ConnectionError("down")})
    with pytest.raises(fd.FetchError) as exc:
        fd.collect(tmp_path, "NVDA", "2026-11-26", "us", call)
    assert exc.value.code == 9


@pytest.mark.parametrize("ticker,date,market", [
    ("", "2026-11-26", "us"),
    ("NVDA", "11/26/2026", "us"),
    ("NVDA", "2026-11-26", "hk"),
])
def test_invalid_arguments_raise_exit_code_6(fd, tmp_path, ticker, date, market):
    with pytest.raises(fd.FetchError) as exc:
        fd.collect(tmp_path, ticker, date, market, FakeCalls())
    assert exc.value.code == 6


# ---------- 網路偵測 ----------

def test_probe_detects_agent_proxy_block(fd):
    def blocked(url, timeout):
        raise urllib.error.HTTPError(
            url, 403, "Forbidden", {}, io.BytesIO(b"agent proxy: no rule allows this host"))
    assert fd.network_blocked("us", opener=blocked) is True


def test_probe_detects_connection_failure(fd):
    def down(url, timeout):
        raise urllib.error.URLError("no route")
    assert fd.network_blocked("twse", opener=down) is True


def test_probe_accepts_any_normal_http_response(fd):
    class Ok:
        status = 200

        def close(self):
            pass

    assert fd.network_blocked("us", opener=lambda url, timeout: Ok()) is False

    def not_found(url, timeout):
        raise urllib.error.HTTPError(url, 404, "nf", {}, io.BytesIO(b"x"))
    assert fd.network_blocked("us", opener=not_found) is False


# ---------- 命令列 ----------

def test_cli_blocked_network_returns_8_and_writes_nothing(fd, tmp_path, capsys):
    code = fd.main(["--ticker", "NVDA", "--date", "2026-11-26", "--market", "us",
                    "--workdir", str(tmp_path / "w")],
                   call=FakeCalls(), probe=lambda market: True)
    captured = capsys.readouterr()
    assert code == 8
    assert captured.out == ""
    assert not (tmp_path / "w" / "data").exists()


def test_cli_success_prints_json_summary(fd, tmp_path, capsys):
    code = fd.main(["--ticker", "NVDA", "--date", "2026-11-26", "--market", "us",
                    "--workdir", str(tmp_path / "w")],
                   call=FakeCalls(), probe=lambda market: False)
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert out["price_rows"] == 3
    assert out["files"]["price"].endswith("price.csv")


def test_cli_bad_args_returns_6(fd, capsys):
    assert fd.main(["--ticker", "NVDA"], call=FakeCalls(), probe=lambda m: False) == 6
