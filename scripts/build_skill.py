#!/usr/bin/env python3
"""把 skill-src/<name>/ 組裝成可上傳的 skill 資料夾與 zip。

用法：
  python scripts/build_skill.py [--source skill-src/tradingagentsx-analyze] [--out dist]
                                [--font-dir <字型資料夾>] [--no-fonts]
  python scripts/build_skill.py --plugin [--plugin-dir plugins/tradingagentsx]

組裝內容（單一來源，不手改產物）：
  <source>/**                       原始碼：SKILL.md、scripts/、手寫 references/
  references/prompts/<lang>/*.md    由 tradingagents.agents.prompts 產生（12 個 agent＋共用＋摘要）
  vendor/pdf_generator.py           backend/app/services/pdf_generator.py 原樣複製
  vendor/tradingagents/             dataflows 與其內部相依（default_config、utils/toon_converter）
  assets/NotoSerifTC-{Regular,Bold}.ttf   繁中 PDF 字型（容器沒有可用的 CJK 字型）
  requirements.txt                  Claude Code 腳本模式的 pip 相依

--plugin 改為產生 Claude Code plugin（plugins/tradingagentsx/，需提交進 git，
供 /plugin marketplace add 與 /plugin install 使用），不產生 zip；測試會檢查提交的
產物與目前原始碼是否一致。

zip 內容可重現（固定時間戳、排序）。stdout 只輸出一份 JSON 摘要。
結束碼：0 成功；2 來源或 SKILL.md 不合法；3 輸出資料夾不是先前建置的產物；
        4 repo 內缺少必要檔案（字型、pdf_generator…）；6 參數不合法。
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Any, Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = REPO_ROOT / "skill-src" / "tradingagentsx-analyze"
DEFAULT_OUT = REPO_ROOT / "dist"
DEFAULT_FONT_DIR = REPO_ROOT / "Cactus_Classical_Serif,Noto_Serif_TC" / "Noto_Serif_TC" / "static"
PDF_GENERATOR = REPO_ROOT / "backend" / "app" / "services" / "pdf_generator.py"
FONT_FILES = ("NotoSerifTC-Regular.ttf", "NotoSerifTC-Bold.ttf")
BUILD_MARKER = ".skill-build"
DEFAULT_PLUGIN_DIR = REPO_ROOT / "plugins" / "tradingagentsx"
PLUGIN_NAME = "tradingagentsx"
PLUGIN_VERSION = "0.2.3"
PLUGIN_MANIFEST = {
    "name": PLUGIN_NAME,
    "description": "TradingAgentsX 12 位 AI 分析師股票分析流程（美股／台股）：分析、辯論、最終決策與 PDF 報告。"
                   "Multi-agent stock analysis with bull/bear and risk debates, bilingual zh-TW/en, PDF report.",
    "version": PLUGIN_VERSION,
    "author": {"name": "Yao920127"},
    "homepage": "https://github.com/Yao920127/TradingAgentsX",
    "repository": "https://github.com/Yao920127/TradingAgentsX",
    "license": "Apache-2.0",
    "keywords": ["stocks", "trading", "analysis", "multi-agent", "taiwan", "pdf"],
}
LANGUAGES = ("zh-TW", "en")
ZIP_TIMESTAMP = (2020, 1, 1, 0, 0, 0)
IGNORED = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")

# 與 tradingagents.agents.prompts 的 agent 一一對應
AGENT_PROMPTS = (
    "market_analyst", "social_analyst", "news_analyst", "fundamentals_analyst",
    "bull_researcher", "bear_researcher", "research_manager", "trader",
    "aggressive_debator", "conservative_debator", "neutral_debator", "risk_manager",
)
SUMMARY_SECTIONS = ("market", "sentiment", "news", "fundamentals")

# dataflows 的內部相依（以 AST 掃描 import 得出）：default_config 與 utils/toon_converter
VENDOR_TRADINGAGENTS_FILES = ("default_config.py", "utils/toon_converter.py")

REQUIREMENTS = """\
# tradingagentsx-analyze 腳本模式（fetch_data.py）需要的套件；Claude app 容器不需要
requests
pandas
numpy
polars
yfinance
stockstats
tenacity
beautifulsoup4
python-dateutil
tqdm
openai
praw
git+https://github.com/toon-format/toon-python.git
"""


class BuildError(Exception):
    """可預期的失敗；code 即命令列的結束碼。"""

    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code


# ---------- 來源檢查 ----------

def read_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise BuildError(2, f"{skill_md} 缺少 YAML frontmatter（開頭的 --- 區塊）")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields


def validate_source(source: Path) -> str:
    """回傳 skill 名稱；來源不合法時拋 BuildError(2)。"""
    if not source.is_dir():
        raise BuildError(2, f"找不到 skill 來源資料夾：{source}")
    skill_md = source / "SKILL.md"
    if not skill_md.is_file():
        raise BuildError(2, f"{source} 內沒有 SKILL.md")
    fields = read_frontmatter(skill_md)
    name = fields.get("name", "")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        raise BuildError(2, f"SKILL.md 的 name 必須是小寫英數與連字號，收到：{name!r}")
    if name != source.name:
        raise BuildError(2, f"SKILL.md 的 name（{name}）必須與資料夾名稱（{source.name}）一致")
    if not fields.get("description"):
        raise BuildError(2, "SKILL.md 缺少 description")
    return name


def _require(path: Path, what: str) -> Path:
    if not path.is_file():
        raise BuildError(4, f"找不到{what}：{path}")
    return path


# ---------- 組裝各部分 ----------

def _prepare_output(target: Path) -> None:
    """只清除先前建置留下的資料夾，避免誤刪使用者的檔案。"""
    if target.exists():
        if not (target / BUILD_MARKER).is_file():
            raise BuildError(3, f"{target} 已存在且不是先前建置的產物（缺少 {BUILD_MARKER}），不會覆寫")
        shutil.rmtree(target)
    target.mkdir(parents=True)
    (target / BUILD_MARKER).write_text("generated by scripts/build_skill.py\n", encoding="utf-8")


def _load_prompts_module():
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    import tradingagents.agents.prompts as prompts  # noqa: PLC0415
    return prompts


def write_prompt_references(target: Path) -> int:
    prompts = _load_prompts_module()
    count = 0
    for lang in LANGUAGES:
        folder = target / "references" / "prompts" / lang
        folder.mkdir(parents=True, exist_ok=True)
        for agent in AGENT_PROMPTS:
            text = getattr(prompts, f"get_{agent}_prompt")(lang)
            (folder / f"{agent}.md").write_text(f"{text.strip()}\n", encoding="utf-8")
            count += 1
        common = "\n\n".join([
            f"# 共用指令 / Common instructions ({lang})",
            f"## 角色指令 Role instruction\n\n{prompts.get_agent_role_instruction(lang).strip()}",
            "## 情境訊息範本 Context message template\n\n"
            + prompts.get_context_message(lang, "{date}", "{company}", "{ticker}").strip(),
            f"## 語言指令 Language instruction\n\n{prompts.get_language_instruction(lang).strip()}",
            f"## 語言結尾指令 Language closing\n\n{prompts.get_language_closing_instruction(lang).strip()}",
        ])
        (folder / "_common.md").write_text(f"{common}\n", encoding="utf-8")
        count += 1
        for section in SUMMARY_SECTIONS:
            text = prompts.get_section_summarizer_prompt(section, lang)
            (folder / f"_summarizer_{section}.md").write_text(f"{text.strip()}\n", encoding="utf-8")
            count += 1
    return count


def copy_vendor(target: Path) -> None:
    vendor = target / "vendor"
    vendor.mkdir(exist_ok=True)
    shutil.copy2(_require(PDF_GENERATOR, "pdf_generator.py"), vendor / "pdf_generator.py")
    package = REPO_ROOT / "tradingagents"
    shutil.copytree(_require(package / "dataflows" / "interface.py", "dataflows").parent,
                    vendor / "tradingagents" / "dataflows", ignore=IGNORED)
    for rel in VENDOR_TRADINGAGENTS_FILES:
        destination = vendor / "tradingagents" / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(_require(package / rel, f"tradingagents/{rel}"), destination)


def copy_fonts(target: Path, font_dir: Path) -> None:
    assets = target / "assets"
    assets.mkdir(exist_ok=True)
    for name in FONT_FILES:
        shutil.copy2(_require(Path(font_dir) / name, f"字型 {name}"), assets / name)


def make_zip(folder: Path, zip_path: Path) -> int:
    """可重現的 zip：排序、固定時間戳；回傳檔案數。"""
    root = folder.name
    files = sorted(p for p in folder.rglob("*") if p.is_file() and p.name != BUILD_MARKER)
    dirs = sorted({d for p in files for d in p.relative_to(folder).parents if str(d) != "."})
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for rel in [Path()] + dirs:
            info = zipfile.ZipInfo(f"{root}/{rel.as_posix()}/".replace("/./", "/"), ZIP_TIMESTAMP)
            info.external_attr = (0o40755 << 16) | 0x10
            zf.writestr(info, b"")
        for path in files:
            rel = path.relative_to(folder)
            info = zipfile.ZipInfo(f"{root}/{rel.as_posix()}", ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if rel.parts[0] == "scripts" else 0o644) << 16
            zf.writestr(info, path.read_bytes())
    return len(files)


def _check_fonts(include_fonts: bool, font_dir: Optional[Path]) -> Path:
    fonts = Path(font_dir) if font_dir else DEFAULT_FONT_DIR
    if include_fonts:  # 先檢查再動手，失敗時不會留下半成品
        for font in FONT_FILES:
            _require(fonts / font, f"字型 {font}")
    return fonts


def assemble_skill(source: Path, target: Path, include_fonts: bool, fonts: Path) -> int:
    """把 skill 完整內容組裝到 target，回傳提示詞檔案數。"""
    shutil.copytree(source, target, ignore=IGNORED, dirs_exist_ok=True)
    prompt_files = write_prompt_references(target)
    copy_vendor(target)
    if include_fonts:
        copy_fonts(target, fonts)
    (target / "requirements.txt").write_text(REQUIREMENTS, encoding="utf-8")
    return prompt_files


def build(source: Path, out_dir: Path, include_fonts: bool = True,
          font_dir: Optional[Path] = None) -> dict[str, Any]:
    """組裝並打包，回傳摘要；失敗拋 BuildError。"""
    source, out_dir = Path(source), Path(out_dir)
    name = validate_source(source)
    fonts = _check_fonts(include_fonts, font_dir)
    target = out_dir / name
    _prepare_output(target)
    prompt_files = assemble_skill(source, target, include_fonts, fonts)

    zip_path = out_dir / f"{name}.zip"
    file_count = make_zip(target, zip_path)
    return {
        "name": name,
        "folder": str(target),
        "zip": str(zip_path),
        "zip_bytes": zip_path.stat().st_size,
        "files": file_count,
        "prompt_files": prompt_files,
        "fonts": include_fonts,
    }


def build_plugin(source: Path, plugin_dir: Path, include_fonts: bool = True,
                 font_dir: Optional[Path] = None) -> dict[str, Any]:
    """產生 Claude Code plugin（.claude-plugin/plugin.json＋skills/<name>/）；失敗拋 BuildError。"""
    source, plugin_dir = Path(source), Path(plugin_dir)
    name = validate_source(source)
    fonts = _check_fonts(include_fonts, font_dir)
    _prepare_output(plugin_dir)
    manifest_dir = plugin_dir / ".claude-plugin"
    manifest_dir.mkdir()
    (manifest_dir / "plugin.json").write_text(
        json.dumps(PLUGIN_MANIFEST, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prompt_files = assemble_skill(source, plugin_dir / "skills" / name, include_fonts, fonts)
    return {
        "name": PLUGIN_NAME,
        "skill": name,
        "plugin_dir": str(plugin_dir),
        "files": sum(1 for p in plugin_dir.rglob("*") if p.is_file()),
        "prompt_files": prompt_files,
        "fonts": include_fonts,
    }


class _Parser(argparse.ArgumentParser):
    def error(self, message: str):  # type: ignore[override]
        raise BuildError(6, message)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _Parser(description="組裝並打包 skill")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--font-dir", type=Path, default=None)
    parser.add_argument("--plugin", action="store_true",
                        help="產生 Claude Code plugin 而不是 zip（需提交進 git）")
    parser.add_argument("--plugin-dir", type=Path, default=DEFAULT_PLUGIN_DIR)
    parser.add_argument("--no-fonts", action="store_true", help="略過字型（開發用，繁中 PDF 會失敗）")
    try:
        args = parser.parse_args(argv)
        if args.plugin:
            summary = build_plugin(args.source, args.plugin_dir, include_fonts=not args.no_fonts,
                                   font_dir=args.font_dir)
        else:
            summary = build(args.source, args.out, include_fonts=not args.no_fonts, font_dir=args.font_dir)
    except BuildError as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return exc.code
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
