#!/usr/bin/env python3
"""把各 agent 的 Markdown 報告合併成 PDF，沿用 TradingAgentsX 網頁版的版面。

用法：
  python render_pdf.py --workdir <資料夾> --ticker 2330 --date 2026-11-26 \
      [--lang zh-TW|en] [--company 公司名稱] [--model Claude] [--output 路徑] \
      [--depth 1-5]

--depth 有給時，會先驗證辯論檔的發言標記：debate_investment.md 必須恰有
2×depth 個、debate_risk.md 必須恰有 3×depth 個 `<!-- 第 N 次 / 共 M 次 -->`，
且編號為 1..總數；不符就以結束碼 7 結束，不產出 PDF。

工作資料夾結構：
  reports/<key>.md   各 agent 報告；key 見 REPORTS（缺少或空白的會略過）
  debate_investment.md / debate_risk.md
                     辯論全文；只有給 --depth 時才會檢查
  price_data.json    選用。{"price_data": [{Date,Open,High,Low,Close,Volume}, ...],
                     "price_stats": {...}}；price_stats 缺少時自動計算

stdout 只輸出一份 JSON 摘要；訊息與錯誤都走 stderr。
結束碼：0 成功；2 沒有任何報告；3 找不到 pdf_generator；4 繁中缺字型；
        5 價格資料格式錯誤；6 參數不合法；7 辯論發言次數與 --depth 不符。
"""
from __future__ import annotations

import argparse
import base64
import contextlib
import hashlib
import importlib.util
import json
import os
import re
import sys
import tempfile
import zlib
from datetime import datetime
from pathlib import Path
from types import ModuleType
from typing import Any, Optional, Sequence

SKILL_DIR = Path(__file__).resolve().parent.parent
REPO_GENERATOR = SKILL_DIR.parent.parent / "backend" / "app" / "services" / "pdf_generator.py"
FONT_FILE = "NotoSerifTC-Regular.ttf"
LANGUAGES = ("zh-TW", "en")
REQUIRED_PRICE_COLUMNS = ("Date", "Open", "High", "Low", "Close")
MIN_CHART_ROWS = 5  # 與 pdf_generator 的繪圖門檻一致
DEPTH_RANGE = range(1, 6)
# (檔名, 每個深度的發言次數)；與 SKILL.md 的辯論規則一致
DEBATE_FILES = (("debate_investment.md", 2), ("debate_risk.md", 3))
_DEBATE_MARKER = re.compile(r"<!--\s*第\s*(\d+)\s*次\s*/\s*共\s*\d+\s*次\s*-->")

# (報告檔名 key, pdf_generator 的標籤鍵)；順序即 PDF 內的章節順序
REPORTS = (
    ("market", "market_analyst"),
    ("social", "social_analyst"),
    ("news", "news_analyst"),
    ("fundamentals", "fundamentals_analyst"),
    ("bull", "bull_researcher"),
    ("bear", "bear_researcher"),
    ("research_manager", "research_manager"),
    ("trader", "trader"),
    ("aggressive", "aggressive_analyst"),
    ("conservative", "conservative_analyst"),
    ("neutral", "neutral_analyst"),
    ("risk_manager", "risk_manager"),
)

_generator_modules: dict[Path, ModuleType] = {}


class RenderError(Exception):
    """可預期的失敗；code 即命令列的結束碼。"""

    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code


_TAIWAN_TICKER = re.compile(r"^\d{4,6}[A-Za-z]?(\.(TW|TWO))?$", re.IGNORECASE)


def currency_for(ticker: str) -> str:
    """台股（純數字代號，可帶 .TW/.TWO）用 NT$，其餘用 $。"""
    return "NT$" if _TAIWAN_TICKER.match(ticker.strip()) else "$"


def _validate_args(ticker: str, date: str, lang: str) -> None:
    if lang not in LANGUAGES:
        raise RenderError(6, f"--lang 只能是 {' 或 '.join(LANGUAGES)}，收到：{lang!r}")
    if not ticker.strip():
        raise RenderError(6, "--ticker 不可為空")
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError as exc:
        raise RenderError(6, f"--date 必須是 YYYY-MM-DD，收到：{date!r}") from exc


def _check_debate_markers(workdir: Path, depth: int) -> None:
    """辯論檔的發言標記必須恰為 1..(每深度次數 × depth)；否則視為辯論沒跑完。"""
    for name, per_depth in DEBATE_FILES:
        expected = per_depth * depth
        path = workdir / name
        if not path.is_file():
            raise RenderError(7, f"找不到 {path}；depth={depth} 需要 {expected} 次發言")
        numbers = [int(n) for n in _DEBATE_MARKER.findall(path.read_text(encoding="utf-8"))]
        if sorted(numbers) != list(range(1, expected + 1)):
            raise RenderError(
                7,
                f"{name} 的發言標記不符：depth={depth} 應為第 1–{expected} 次各一個，"
                f"實際找到 {len(numbers)} 個（{numbers or '無'}）；請繼續辯論補足後再產生 PDF",
            )


def _find_generator_path() -> Path:
    candidates = []
    from_env = os.environ.get("TA_PDF_GENERATOR")
    if from_env:
        candidates.append(Path(from_env))
    candidates.extend([SKILL_DIR / "vendor" / "pdf_generator.py", REPO_GENERATOR])
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    searched = "、".join(str(c) for c in candidates)
    raise RenderError(3, f"找不到 pdf_generator.py，已找過：{searched}")


def _load_generator_module(path: Path) -> ModuleType:
    cached = _generator_modules.get(path)
    if cached is not None:
        return cached
    spec = importlib.util.spec_from_file_location("ta_pdf_generator", path)
    if spec is None or spec.loader is None:
        raise RenderError(3, f"無法載入 {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _generator_modules[path] = module
    return module


FONT_PACK_SUFFIX = ".b64.txt"


def _unpack_fonts(assets: Path) -> Optional[Path]:
    """把 assets/NotoSerifTC-<樣式>.b64.partNN.txt（zlib＋base64 的字型，切成多份）還原成暫存資料夾的 .ttf。

    Gemini 技能上傳只收文字類副檔名，所以字型以文字檔附帶；沒有壓縮包就回傳 None。
    """
    parts: dict[str, list[Path]] = {}
    for pack in sorted(assets.glob(f"NotoSerifTC-*{FONT_PACK_SUFFIX[:-4]}.part*.txt")):
        parts.setdefault(pack.name.split(FONT_PACK_SUFFIX[:-4])[0], []).append(pack)
    if not parts:
        return None
    signature = "|".join(f"{p.name}:{p.stat().st_size}" for group in parts.values() for p in group)
    cache = Path(tempfile.gettempdir()) / f"tradingagentsx-fonts-{hashlib.sha1(signature.encode()).hexdigest()[:12]}"
    style = ""
    try:
        cache.mkdir(parents=True, exist_ok=True)
        for style, group in parts.items():
            target = cache / f"{style}.ttf"
            if target.is_file() and target.stat().st_size > 0:
                continue
            encoded = "".join(p.read_text(encoding="ascii") for p in group)
            data = zlib.decompress(base64.b64decode(encoded))
            partial = target.with_suffix(f".tmp{os.getpid()}")
            partial.write_bytes(data)
            os.replace(partial, target)
    except (OSError, ValueError, zlib.error) as exc:
        raise RenderError(4, f"字型壓縮檔 {style} 無法還原：{exc}") from exc
    return cache


def _resolve_font_dir(font_dir: Optional[Path]) -> Optional[Path]:
    """明確指定優先；否則用 skill 附帶的字型（ttf 或壓縮文字檔）；都沒有就交給 pdf_generator 的預設。"""
    if font_dir is not None:
        return font_dir
    bundled = SKILL_DIR / "assets"
    if (bundled / FONT_FILE).is_file():
        return bundled
    return _unpack_fonts(bundled)


def _collect_reports(workdir: Path, module: ModuleType, lang: str) -> tuple[list[dict], list[str]]:
    reports_dir = workdir / "reports"
    included: list[dict] = []
    missing: list[str] = []
    for key, label_key in REPORTS:
        path = reports_dir / f"{key}.md"
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        if text.strip():
            included.append({
                "analyst_name": module.get_pdf_label(label_key, lang),
                "report_content": text,
            })
        else:
            missing.append(key)
    return included, missing


def _compute_price_stats(rows: list[dict]) -> dict[str, Any]:
    first, last = rows[0], rows[-1]
    start, end = float(first["Close"]), float(last["Close"])
    growth = (end - start) / start * 100 if start else 0.0
    try:
        duration = (
            datetime.strptime(str(last["Date"])[:10], "%Y-%m-%d")
            - datetime.strptime(str(first["Date"])[:10], "%Y-%m-%d")
        ).days
    except ValueError:
        duration = len(rows) - 1
    return {
        "growth_rate": growth,
        "duration_days": duration,
        "start_date": str(first["Date"])[:10],
        "end_date": str(last["Date"])[:10],
        "start_price": start,
        "end_price": end,
    }


def _load_price(workdir: Path) -> tuple[Optional[list[dict]], Optional[dict]]:
    path = workdir / "price_data.json"
    if not path.is_file():
        return None, None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise RenderError(5, f"price_data.json 不是有效的 JSON：{exc}") from exc

    rows = payload.get("price_data") if isinstance(payload, dict) else payload
    stats = payload.get("price_stats") if isinstance(payload, dict) else None
    if not isinstance(rows, list):
        raise RenderError(5, "price_data.json 的 price_data 必須是陣列")
    if not rows:
        return None, None

    normalized: list[dict] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise RenderError(5, f"price_data 第 {index} 列不是物件")
        absent = [c for c in REQUIRED_PRICE_COLUMNS if c not in row]
        if absent:
            raise RenderError(5, f"price_data 第 {index} 列缺少欄位：{', '.join(absent)}")
        normalized.append({**row, "Volume": row.get("Volume", 0)})
    return normalized, stats or _compute_price_stats(normalized)


def render(
    workdir: Path,
    ticker: str,
    date: str,
    lang: str = "zh-TW",
    company: Optional[str] = None,
    model: str = "Claude",
    output: Optional[Path] = None,
    font_dir: Optional[Path] = None,
    depth: Optional[int] = None,
) -> dict[str, Any]:
    """產出 PDF 並回傳摘要；失敗時拋出 RenderError。"""
    workdir = Path(workdir)
    _validate_args(ticker, date, lang)
    if depth is not None:
        if depth not in DEPTH_RANGE:
            raise RenderError(6, f"--depth 必須是 1–5，收到：{depth!r}")
        _check_debate_markers(workdir, depth)

    generator_path = _find_generator_path()
    with contextlib.redirect_stdout(sys.stderr):  # 產生器會 print 訊息，不可污染 stdout 的 JSON
        module = _load_generator_module(generator_path)
    included, missing = _collect_reports(workdir, module, lang)
    if not included:
        keys = ", ".join(key for key, _ in REPORTS)
        raise RenderError(2, f"{workdir / 'reports'} 內找不到任何報告（可用檔名：{keys}，副檔名 .md）")
    price_data, price_stats = _load_price(workdir)

    resolved_font_dir = _resolve_font_dir(Path(font_dir) if font_dir else None)
    with contextlib.redirect_stdout(sys.stderr):
        generator = module.PDFGenerator(font_dir=str(resolved_font_dir) if resolved_font_dir else None)
        # 沒有 CJK 字型時產生器會退回 Helvetica，繁中內容會變成亂碼，所以直接報錯
        if lang == "zh-TW" and getattr(generator, "_font_name", "") == "Helvetica":
            raise RenderError(4, f"找不到中文字型 {FONT_FILE}（字型目錄：{resolved_font_dir or '預設路徑'}）")
        pdf_bytes = generator.generate_combined_report_pdf(
            ticker=ticker,
            analysis_date=date,
            reports=included,
            price_data=price_data,
            price_stats=price_stats,
            language=lang,
            deep_think_llm=model,
            quick_think_llm=model,
            company_name=company,
            currency=currency_for(ticker),
        )

    safe_ticker = re.sub(r"[^\w.\-]", "_", ticker.strip())
    pdf_path = Path(output) if output else workdir / f"{safe_ticker}_Report_{date}.pdf"
    pdf_path.write_bytes(pdf_bytes)
    return {
        "pdf": str(pdf_path),
        "language": lang,
        "included_reports": [r["analyst_name"] for r in included],
        "missing_reports": missing,
        "chart": bool(price_data and len(price_data) >= MIN_CHART_ROWS),
        "price_stats": price_stats,
    }


class _Parser(argparse.ArgumentParser):
    def error(self, message: str):  # type: ignore[override]
        raise RenderError(6, message)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _Parser(description="把各 agent 的 Markdown 報告合併成 PDF")
    parser.add_argument("--workdir", required=True, type=Path)
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--date", required=True, help="分析日期 YYYY-MM-DD")
    parser.add_argument("--lang", default="zh-TW")
    parser.add_argument("--company", default=None)
    parser.add_argument("--model", default="Claude")
    parser.add_argument("--output", default=None, type=Path)
    parser.add_argument("--font-dir", default=None, type=Path)
    parser.add_argument("--depth", default=None, type=int, help="研究深度 1–5；給了就驗證辯論發言標記")
    try:
        args = parser.parse_args(argv)
        result = render(
            args.workdir, args.ticker, args.date, lang=args.lang, company=args.company,
            model=args.model, output=args.output, font_dir=args.font_dir, depth=args.depth,
        )
    except RenderError as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return exc.code
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
