"""skills/tradingagentsx-analyze/scripts/render_pdf.py 的測試。

以合成的報告與價格資料實際產出 PDF，驗證：
  - 12 份報告、中英文兩種語言都能產出
  - 缺少的報告會被略過並列在結果裡；完全沒有報告會報錯
  - 有價格資料時多出一頁走勢圖；價格統計缺少時自動計算
  - 繁中報告缺字型時明確報錯，而不是產出亂碼
  - 壞掉的價格資料、不合法的日期明確報錯
"""
import importlib.util
import json
import re
from pathlib import Path

import pytest

SCRIPT = (
    Path(__file__).resolve().parent.parent
    / "skills" / "tradingagentsx-analyze" / "scripts" / "render_pdf.py"
)

REPORT_KEYS = [
    "market", "social", "news", "fundamentals",
    "bull", "bear", "research_manager",
    "trader", "aggressive", "conservative", "neutral", "risk_manager",
]

ZH_REPORT = """## 一、概況

- 趨勢：**上升**，RSI **61.2**
- 支撐 2150，壓力 2330

| 指標 | 最新值 | 解讀 |
|---|---|---|
| RSI | 61.2 | 中性偏強 |
| MACD | 12.3 | 多方動能 |

### 1. 風險

資料缺口：無法取得外資買賣超。
"""

EN_REPORT = """## 1. Overview

- Trend: **up**, RSI **61.2**
- Support 2150, resistance 2330

| Indicator | Latest | Reading |
|---|---|---|
| RSI | 61.2 | Neutral-strong |

### Risks

Data gap: foreign flow unavailable.
"""


@pytest.fixture(scope="module")
def render_pdf():
    spec = importlib.util.spec_from_file_location("ta_render_pdf", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_reports(workdir: Path, text: str, keys=REPORT_KEYS) -> None:
    reports = workdir / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    for key in keys:
        (reports / f"{key}.md").write_text(text, encoding="utf-8")


def _write_prices(workdir: Path, days: int = 30, with_stats: bool = True) -> None:
    rows = []
    for i in range(days):
        base = 2100 + i * 5
        rows.append({
            "Date": f"2026-10-{i + 1:02d}",
            "Open": base, "High": base + 20, "Low": base - 15,
            "Close": base + 8, "Volume": 40_000_000 + i * 10_000,
        })
    payload = {"price_data": rows}
    if with_stats:
        payload["price_stats"] = {
            "growth_rate": 6.9, "duration_days": days - 1,
            "start_date": rows[0]["Date"], "end_date": rows[-1]["Date"],
            "start_price": rows[0]["Close"], "end_price": rows[-1]["Close"],
        }
    (workdir / "price_data.json").write_text(json.dumps(payload), encoding="utf-8")


def _page_count(pdf_path: Path) -> int:
    return len(re.findall(rb"/Type\s*/Page(?![a-zA-Z])", pdf_path.read_bytes()))


def test_renders_zh_pdf_with_all_twelve_reports(render_pdf, tmp_path):
    _write_reports(tmp_path, ZH_REPORT)

    result = render_pdf.render(tmp_path, "2330", "2026-11-26", lang="zh-TW", company="台積電")

    pdf = Path(result["pdf"])
    assert pdf.name == "2330_Report_2026-11-26.pdf"
    assert pdf.read_bytes().startswith(b"%PDF")
    assert result["missing_reports"] == []
    assert len(result["included_reports"]) == 12
    # 封面 + 目錄 + 3 個團隊分隔頁 + 12 份報告，至少 17 頁
    assert _page_count(pdf) >= 17


def test_renders_english_pdf(render_pdf, tmp_path):
    _write_reports(tmp_path, EN_REPORT)

    result = render_pdf.render(tmp_path, "NVDA", "2026-11-26", lang="en")

    pdf = Path(result["pdf"])
    assert pdf.read_bytes().startswith(b"%PDF")
    assert "Market Analyst" in result["included_reports"]
    assert "Risk Manager" in result["included_reports"]


def test_missing_reports_are_skipped_and_listed(render_pdf, tmp_path):
    _write_reports(tmp_path, ZH_REPORT, keys=["market", "risk_manager"])

    result = render_pdf.render(tmp_path, "2330", "2026-11-26")

    assert result["included_reports"] == ["市場分析師", "風險經理"]
    assert "news" in result["missing_reports"]
    assert len(result["missing_reports"]) == 10


@pytest.mark.parametrize("selected", [
    ["market", "news"],
    ["social"],
    ["fundamentals", "market", "news"],
])
def test_renders_with_only_selected_analysts(render_pdf, tmp_path, selected):
    # 使用者只選部分分析師：辯論與決策 8 份報告齊全，沒選的分析師不寫
    downstream = [k for k in REPORT_KEYS if k not in ("market", "social", "news", "fundamentals")]
    _write_reports(tmp_path, ZH_REPORT, keys=selected + downstream)

    result = render_pdf.render(tmp_path, "NVDA", "2026-11-26", lang="zh-TW")

    unselected = [k for k in ("market", "social", "news", "fundamentals") if k not in selected]
    assert sorted(result["missing_reports"]) == sorted(unselected)
    assert len(result["included_reports"]) == len(selected) + len(downstream)
    pdf = Path(result["pdf"])
    assert pdf.read_bytes().startswith(b"%PDF")
    # 封面 + 目錄 + 3 個團隊分隔頁 + 已納入的報告
    assert _page_count(pdf) >= 5 + len(result["included_reports"])


def test_blank_report_file_counts_as_missing(render_pdf, tmp_path):
    _write_reports(tmp_path, ZH_REPORT, keys=["market"])
    (tmp_path / "reports" / "news.md").write_text("   \n", encoding="utf-8")

    result = render_pdf.render(tmp_path, "2330", "2026-11-26")

    assert "news" in result["missing_reports"]


def test_no_reports_raises_exit_code_2(render_pdf, tmp_path):
    with pytest.raises(render_pdf.RenderError) as exc:
        render_pdf.render(tmp_path, "2330", "2026-11-26")
    assert exc.value.code == 2


def test_price_chart_adds_a_page(render_pdf, tmp_path):
    without = tmp_path / "without"
    with_chart = tmp_path / "with"
    for d in (without, with_chart):
        _write_reports(d, ZH_REPORT, keys=["market", "risk_manager"])
    _write_prices(with_chart)

    plain = render_pdf.render(without, "2330", "2026-11-26")
    charted = render_pdf.render(with_chart, "2330", "2026-11-26")

    assert charted["chart"] is True
    assert plain["chart"] is False
    assert _page_count(Path(charted["pdf"])) == _page_count(Path(plain["pdf"])) + 1


def test_price_stats_are_computed_when_absent(render_pdf, tmp_path):
    _write_reports(tmp_path, ZH_REPORT, keys=["market"])
    _write_prices(tmp_path, with_stats=False)

    result = render_pdf.render(tmp_path, "2330", "2026-11-26")

    stats = result["price_stats"]
    assert stats["start_price"] == 2108
    assert stats["end_price"] == 2100 + 29 * 5 + 8
    assert stats["growth_rate"] == pytest.approx((2253 - 2108) / 2108 * 100)
    assert stats["duration_days"] == 29


def test_zh_without_cjk_font_fails_clearly(render_pdf, tmp_path):
    _write_reports(tmp_path, ZH_REPORT, keys=["market"])
    empty_font_dir = tmp_path / "no_fonts"
    empty_font_dir.mkdir()

    with pytest.raises(render_pdf.RenderError) as exc:
        render_pdf.render(tmp_path, "2330", "2026-11-26", lang="zh-TW", font_dir=empty_font_dir)
    assert exc.value.code == 4


def test_malformed_price_json_raises_exit_code_5(render_pdf, tmp_path):
    _write_reports(tmp_path, ZH_REPORT, keys=["market"])
    (tmp_path / "price_data.json").write_text("{not json", encoding="utf-8")

    with pytest.raises(render_pdf.RenderError) as exc:
        render_pdf.render(tmp_path, "2330", "2026-11-26")
    assert exc.value.code == 5


def test_price_rows_missing_columns_raise_exit_code_5(render_pdf, tmp_path):
    _write_reports(tmp_path, ZH_REPORT, keys=["market"])
    (tmp_path / "price_data.json").write_text(
        json.dumps({"price_data": [{"Date": "2026-11-01", "Close": 1.0}] * 6}), encoding="utf-8"
    )

    with pytest.raises(render_pdf.RenderError) as exc:
        render_pdf.render(tmp_path, "2330", "2026-11-26")
    assert exc.value.code == 5


@pytest.mark.parametrize("bad_date", ["2026/11/26", "11-26-2026", "today", ""])
def test_invalid_date_raises_exit_code_6(render_pdf, tmp_path, bad_date):
    _write_reports(tmp_path, ZH_REPORT, keys=["market"])
    with pytest.raises(render_pdf.RenderError) as exc:
        render_pdf.render(tmp_path, "2330", bad_date)
    assert exc.value.code == 6


def test_cli_prints_json_summary_and_returns_zero(render_pdf, tmp_path, capsys):
    _write_reports(tmp_path, ZH_REPORT, keys=["market"])

    code = render_pdf.main(["--workdir", str(tmp_path), "--ticker", "2330", "--date", "2026-11-26"])

    out = capsys.readouterr().out
    assert code == 0
    assert json.loads(out)["included_reports"] == ["市場分析師"]


def test_cli_returns_error_code_and_message(render_pdf, tmp_path, capsys):
    code = render_pdf.main(["--workdir", str(tmp_path), "--ticker", "2330", "--date", "2026-11-26"])

    captured = capsys.readouterr()
    assert code == 2
    assert captured.out == ""
    assert "reports" in captured.err


@pytest.mark.parametrize("ticker,expected", [
    ("2330", "NT$"), ("6488", "NT$"), ("00878", "NT$"), ("2330.TW", "NT$"),
    ("6488.TWO", "NT$"), ("NVDA", "$"), ("BRK.B", "$"), ("AAPL", "$"),
])
def test_currency_for_ticker(render_pdf, ticker, expected):
    assert render_pdf.currency_for(ticker) == expected


def _generator_module(render_pdf):
    return render_pdf._load_generator_module(render_pdf._find_generator_path())


def test_price_stats_use_currency_symbol(render_pdf, tmp_path, monkeypatch):
    module = _generator_module(render_pdf)
    seen = []
    original = module.PDFGenerator._add_table
    monkeypatch.setattr(
        module.PDFGenerator, "_add_table",
        lambda self, pdf, rows, *a, **k: (seen.append(rows), original(self, pdf, rows, *a, **k))[1],
    )
    _write_reports(tmp_path, ZH_REPORT, keys=["market"])
    _write_prices(tmp_path)

    render_pdf.render(tmp_path, "2330", "2026-11-26")

    prices = [r[1] for rows in seen for r in rows if r[0] in ("起始價格", "結束價格", "Start Price", "End Price")]
    assert prices and all(p.startswith("NT$") for p in prices)


def test_cover_merges_identical_models_into_one_column(render_pdf, tmp_path, monkeypatch):
    module = _generator_module(render_pdf)
    labels = []
    original = module.PDFGenerator._spaced_text
    monkeypatch.setattr(
        module.PDFGenerator, "_spaced_text",
        lambda self, pdf, x, y, w, text, *a, **k: (labels.append(text), original(self, pdf, x, y, w, text, *a, **k))[1],
    )
    _write_reports(tmp_path, ZH_REPORT, keys=["market"])

    render_pdf.render(tmp_path, "NVDA", "2026-11-26", model="Claude")

    assert "分析模型" in labels
    assert "深度思維模型" not in labels and "快速思維模型" not in labels
