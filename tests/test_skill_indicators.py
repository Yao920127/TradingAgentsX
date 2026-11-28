"""skill-src/tradingagentsx-analyze/scripts/indicators.py 的測試。

驗證：
  - OHLCV 讀取（JSON／CSV）與驗證（欄位、日期、順序、重複、高低價矛盾）
  - 筆數／收盤價總和核對（防範 Claude 轉寫資料出錯）
  - 指標數值與手算結果一致（SMA、EMA、RSI、MACD、布林、ATR、VWMA、MFI）
  - 資料不足時指標為 None 而非亂填
  - CLI 寫出 price_data.json 與 indicators.json，並以結束碼回報錯誤
"""
import csv
import importlib.util
import json
import math
from datetime import date, timedelta
from pathlib import Path

import pytest

SCRIPT = (
    Path(__file__).resolve().parent.parent
    / "skill-src" / "tradingagentsx-analyze" / "scripts" / "indicators.py"
)


@pytest.fixture(scope="module")
def ind():
    spec = importlib.util.spec_from_file_location("ta_indicators", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_rows(n: int = 60):
    rows = []
    first_day = date(2025, 1, 1)
    for i in range(n):
        base = 100 + i
        rows.append({
            "Date": (first_day + timedelta(days=i)).isoformat(),
            "Open": float(base), "High": float(base + 2), "Low": float(base - 2),
            "Close": float(base + 1), "Volume": 1000 + i,
        })
    return rows


def write_json(path: Path, rows) -> Path:
    path.write_text(json.dumps({"price_data": rows}), encoding="utf-8")
    return path


def write_csv(path: Path, rows) -> Path:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["Date", "Open", "High", "Low", "Close", "Volume"])
        writer.writeheader()
        writer.writerows(rows)
    return path


# ---------- 讀取與驗證 ----------

def test_load_json_and_csv_give_same_rows(ind, tmp_path):
    rows = make_rows(10)
    from_json = ind.load_ohlcv(write_json(tmp_path / "a.json", rows))
    from_csv = ind.load_ohlcv(write_csv(tmp_path / "a.csv", rows))
    assert from_json == from_csv
    assert from_json[0]["Close"] == 101.0
    assert len(from_json) == 10


def test_load_accepts_bare_list_json(ind, tmp_path):
    path = tmp_path / "bare.json"
    path.write_text(json.dumps(make_rows(5)), encoding="utf-8")
    assert len(ind.load_ohlcv(path)) == 5


def test_missing_file_is_data_error(ind, tmp_path):
    with pytest.raises(ind.IndicatorError) as exc:
        ind.load_ohlcv(tmp_path / "nope.json")
    assert exc.value.code == 5


def test_missing_column_is_data_error(ind, tmp_path):
    rows = [{k: v for k, v in r.items() if k != "High"} for r in make_rows(5)]
    with pytest.raises(ind.IndicatorError) as exc:
        ind.load_ohlcv(write_json(tmp_path / "a.json", rows))
    assert exc.value.code == 5
    assert "High" in str(exc.value)


def test_unsorted_dates_are_rejected(ind, tmp_path):
    rows = make_rows(5)
    rows[2], rows[3] = rows[3], rows[2]
    with pytest.raises(ind.IndicatorError) as exc:
        ind.load_ohlcv(write_json(tmp_path / "a.json", rows))
    assert exc.value.code == 5


def test_duplicate_dates_are_rejected(ind, tmp_path):
    rows = make_rows(5)
    rows[3]["Date"] = rows[2]["Date"]
    with pytest.raises(ind.IndicatorError) as exc:
        ind.load_ohlcv(write_json(tmp_path / "a.json", rows))
    assert exc.value.code == 5


def test_bad_date_format_is_rejected(ind, tmp_path):
    rows = make_rows(5)
    rows[1]["Date"] = "2025/01/02"
    with pytest.raises(ind.IndicatorError):
        ind.load_ohlcv(write_json(tmp_path / "a.json", rows))


def test_non_numeric_value_is_rejected(ind, tmp_path):
    rows = make_rows(5)
    rows[1]["Close"] = "abc"
    with pytest.raises(ind.IndicatorError) as exc:
        ind.load_ohlcv(write_json(tmp_path / "a.json", rows))
    assert exc.value.code == 5


def test_high_below_low_is_rejected(ind, tmp_path):
    rows = make_rows(5)
    rows[2]["High"], rows[2]["Low"] = 90.0, 110.0
    with pytest.raises(ind.IndicatorError) as exc:
        ind.load_ohlcv(write_json(tmp_path / "a.json", rows))
    assert exc.value.code == 5


def test_close_outside_high_low_is_rejected(ind, tmp_path):
    rows = make_rows(5)
    rows[2]["Close"] = rows[2]["High"] + 50
    with pytest.raises(ind.IndicatorError):
        ind.load_ohlcv(write_json(tmp_path / "a.json", rows))


def test_empty_data_is_rejected(ind, tmp_path):
    with pytest.raises(ind.IndicatorError) as exc:
        ind.load_ohlcv(write_json(tmp_path / "a.json", []))
    assert exc.value.code == 5


def test_expected_row_count_mismatch(ind):
    rows = ind.validate_rows(make_rows(10))
    ind.check_expectations(rows, expect_rows=10)
    with pytest.raises(ind.IndicatorError) as exc:
        ind.check_expectations(rows, expect_rows=11)
    assert exc.value.code == 7


def test_expected_close_sum_mismatch(ind):
    rows = ind.validate_rows(make_rows(10))
    total = sum(r["Close"] for r in rows)
    ind.check_expectations(rows, expect_close_sum=total)
    ind.check_expectations(rows, expect_close_sum=total + 0.004)  # 容許四捨五入誤差
    with pytest.raises(ind.IndicatorError) as exc:
        ind.check_expectations(rows, expect_close_sum=total + 5)
    assert exc.value.code == 7


# ---------- 指標數值 ----------

def test_sma_matches_manual(ind):
    table = ind.compute_indicators(ind.validate_rows(make_rows(60)))
    closes = [101 + i for i in range(60)]
    assert table["close_50_sma"][49] == pytest.approx(sum(closes[:50]) / 50)
    assert table["close_50_sma"][48] is None
    assert table["close_200_sma"][-1] is None  # 只有 60 筆，不夠 200


def test_ema10_matches_manual(ind):
    table = ind.compute_indicators(ind.validate_rows(make_rows(30)))
    closes = [101 + i for i in range(30)]
    alpha = 2 / 11
    ema = closes[0]
    for value in closes[1:]:
        ema = alpha * value + (1 - alpha) * ema
    assert table["close_10_ema"][-1] == pytest.approx(ema)


def test_rsi_is_100_on_monotonic_rise_and_0_on_fall(ind):
    up = ind.compute_indicators(ind.validate_rows(make_rows(40)))
    assert up["rsi"][-1] == pytest.approx(100.0)
    falling = make_rows(40)
    for i, r in enumerate(falling):
        base = 200 - i
        r.update(Open=float(base), High=float(base + 2), Low=float(base - 2), Close=float(base - 1))
    down = ind.compute_indicators(ind.validate_rows(falling))
    assert down["rsi"][-1] == pytest.approx(0.0)
    assert up["rsi"][13] is None  # 前 14 筆差分不足


def test_rsi_flat_series_is_none_not_nan(ind):
    rows = make_rows(30)
    for r in rows:
        r.update(Open=100.0, High=100.0, Low=100.0, Close=100.0)
    table = ind.compute_indicators(ind.validate_rows(rows))
    assert table["rsi"][-1] is None


def test_macd_components_consistent(ind):
    table = ind.compute_indicators(ind.validate_rows(make_rows(80)))
    macd, macds, macdh = table["macd"][-1], table["macds"][-1], table["macdh"][-1]
    assert macdh == pytest.approx(macd - macds)
    assert macd > 0  # 持續上漲，快線在慢線之上
    assert table["macd"][24] is None  # 慢線 26 期未滿


def test_bollinger_matches_manual(ind):
    table = ind.compute_indicators(ind.validate_rows(make_rows(40)))
    closes = [101 + i for i in range(40)][-20:]
    mean = sum(closes) / 20
    std = math.sqrt(sum((c - mean) ** 2 for c in closes) / 20)  # 母體標準差，與 stockstats 一致
    assert table["boll"][-1] == pytest.approx(mean)
    assert table["boll_ub"][-1] == pytest.approx(mean + 2 * std)
    assert table["boll_lb"][-1] == pytest.approx(mean - 2 * std)
    assert table["boll"][18] is None


def test_atr_bounds(ind):
    # 每日高低差 4，上漲 1 點 → 真實波幅 5（第一筆為 4）
    table = ind.compute_indicators(ind.validate_rows(make_rows(40)))
    assert 4.0 <= table["atr"][-1] <= 5.0
    assert table["atr"][12] is None


def test_vwma_matches_manual(ind):
    rows = ind.validate_rows(make_rows(40))
    table = ind.compute_indicators(rows)
    tail = rows[-14:]  # stockstats 預設視窗 14
    expected = sum((r["High"] + r["Low"] + r["Close"]) / 3 * r["Volume"] for r in tail) / sum(r["Volume"] for r in tail)
    assert table["vwma"][-1] == pytest.approx(expected)


def test_mfi_is_100_on_monotonic_rise(ind):
    table = ind.compute_indicators(ind.validate_rows(make_rows(40)))
    assert table["mfi"][-1] == pytest.approx(100.0)
    assert table["mfi"][12] is None


def test_table_has_one_value_per_row_and_no_nan(ind):
    rows = ind.validate_rows(make_rows(45))
    table = ind.compute_indicators(rows)
    assert set(table) == set(ind.INDICATORS)
    for name, series in table.items():
        assert len(series) == 45, name
        assert all(v is None or math.isfinite(v) for v in series), name


# ---------- 摘要與 CLI ----------

def test_summarize_reports_latest_values_and_dates(ind):
    rows = ind.validate_rows(make_rows(60))
    summary = ind.summarize(rows, ind.compute_indicators(rows), lookback=5)
    assert summary["latest_date"] == rows[-1]["Date"]
    assert summary["latest_close"] == rows[-1]["Close"]
    assert len(summary["recent"]) == 5
    assert summary["recent"][-1]["Date"] == rows[-1]["Date"]
    assert "rsi" in summary["recent"][-1]
    assert summary["rows"] == 60


def test_cli_writes_price_data_and_indicators(ind, tmp_path, capsys):
    src = write_csv(tmp_path / "in.csv", make_rows(60))
    work = tmp_path / "work"
    code = ind.main(["--input", str(src), "--workdir", str(work)])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    price = json.loads((work / "price_data.json").read_text(encoding="utf-8"))
    assert len(price["price_data"]) == 60
    assert price["price_stats"]["start_price"] == 101.0
    assert price["price_stats"]["end_price"] == 160.0
    assert (work / "indicators.json").is_file()
    assert out["rows"] == 60


def test_cli_validation_mismatch_returns_7_and_writes_nothing(ind, tmp_path, capsys):
    src = write_json(tmp_path / "in.json", make_rows(20))
    work = tmp_path / "work"
    code = ind.main(["--input", str(src), "--workdir", str(work), "--expect-rows", "21"])
    captured = capsys.readouterr()
    assert code == 7
    assert captured.out == ""
    assert not (work / "price_data.json").exists()


def test_cli_bad_input_returns_5(ind, tmp_path, capsys):
    code = ind.main(["--input", str(tmp_path / "missing.json"), "--workdir", str(tmp_path / "w")])
    assert code == 5
    assert capsys.readouterr().out == ""


def test_cli_bad_args_returns_6(ind, capsys):
    assert ind.main(["--workdir", "x"]) == 6
