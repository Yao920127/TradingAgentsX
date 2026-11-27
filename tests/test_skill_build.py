"""scripts/build_skill.py 的測試。

驗證建置流程：
  - 產出資料夾與 zip（頂層資料夾＝skill 名稱），zip 內容可重現（逐位元組一致）
  - 提示詞 references 由 tradingagents.agents.prompts 產生：12 個 agent × 2 語言＋共用＋摘要
  - vendor 的 pdf_generator 與 dataflows 子集可脫離 repo 匯入
  - 附帶 Noto Serif TC 字型；SKILL.md 缺少或 frontmatter 錯誤時明確失敗
  - 不會清掉不是自己建置出來的資料夾
"""
import importlib.util
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "build_skill.py"
SKILL_NAME = "tradingagentsx-analyze"

AGENTS = [
    "market_analyst", "social_analyst", "news_analyst", "fundamentals_analyst",
    "bull_researcher", "bear_researcher", "research_manager", "trader",
    "aggressive_debator", "conservative_debator", "neutral_debator", "risk_manager",
]
SUMMARY_SECTIONS = ["market", "sentiment", "news", "fundamentals"]


@pytest.fixture(scope="module")
def bs():
    spec = importlib.util.spec_from_file_location("ta_build_skill", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_source(root: Path, name: str = SKILL_NAME, description: str = "測試用 skill") -> Path:
    src = root / "src" / name
    (src / "scripts").mkdir(parents=True)
    (src / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n# 內容\n", encoding="utf-8")
    (src / "scripts" / "tool.py").write_text("print('hi')\n", encoding="utf-8")
    (src / "scripts" / "__pycache__").mkdir()
    (src / "scripts" / "__pycache__" / "tool.cpython-313.pyc").write_bytes(b"x")
    return src


@pytest.fixture(scope="module")
def built(bs, tmp_path_factory):
    root = tmp_path_factory.mktemp("build")
    src = make_source(root)
    result = bs.build(src, root / "dist")
    return result, root / "dist"


# ---------- 產物結構 ----------

def test_outputs_folder_and_zip(built):
    result, dist = built
    assert (dist / SKILL_NAME / "SKILL.md").is_file()
    assert Path(result["zip"]) == dist / f"{SKILL_NAME}.zip"
    assert zipfile.is_zipfile(result["zip"])


def test_zip_has_single_top_level_folder(built):
    result, _ = built
    with zipfile.ZipFile(result["zip"]) as zf:
        tops = {name.split("/")[0] for name in zf.namelist()}
    assert tops == {SKILL_NAME}


def test_zip_contains_expected_files(built):
    result, _ = built
    with zipfile.ZipFile(result["zip"]) as zf:
        names = set(zf.namelist())
    expected = [
        "SKILL.md", "scripts/tool.py", "requirements.txt",
        "assets/NotoSerifTC-Regular.b64.txt", "assets/NotoSerifTC-Bold.b64.txt",
        "vendor/pdf_generator.py",
        "vendor/tradingagents/default_config.py",
        "vendor/tradingagents/utils/toon_converter.py",
        "vendor/tradingagents/dataflows/interface.py",
        "vendor/tradingagents/dataflows/config.py",
        "references/prompts/zh-TW/_common.md",
        "references/prompts/en/_common.md",
    ]
    for rel in expected:
        assert f"{SKILL_NAME}/{rel}" in names, rel


def test_zip_excludes_caches_and_build_marker(built):
    result, _ = built
    with zipfile.ZipFile(result["zip"]) as zf:
        names = zf.namelist()
    assert not [n for n in names if "__pycache__" in n or n.endswith(".pyc") or ".DS_Store" in n]
    assert not [n for n in names if n.endswith(("skill-build.txt", ".skill-build"))]


def test_zip_is_reproducible(bs, tmp_path):
    src = make_source(tmp_path)
    first = Path(bs.build(src, tmp_path / "a")["zip"]).read_bytes()
    second = Path(bs.build(src, tmp_path / "b")["zip"]).read_bytes()
    assert first == second


def test_rebuild_into_same_output_works(bs, tmp_path):
    src = make_source(tmp_path)
    bs.build(src, tmp_path / "dist")
    (src / "scripts" / "tool.py").write_text("print('changed')\n", encoding="utf-8")
    result = bs.build(src, tmp_path / "dist")
    with zipfile.ZipFile(result["zip"]) as zf:
        assert b"changed" in zf.read(f"{SKILL_NAME}/scripts/tool.py")


# ---------- 提示詞 ----------

@pytest.mark.parametrize("lang", ["zh-TW", "en"])
def test_prompts_generated_for_all_agents(built, lang):
    _, dist = built
    folder = dist / SKILL_NAME / "references" / "prompts" / lang
    for agent in AGENTS:
        text = (folder / f"{agent}.md").read_text(encoding="utf-8")
        assert len(text) > 200, agent
    for section in SUMMARY_SECTIONS:
        assert (folder / f"_summarizer_{section}.md").is_file()


def test_prompt_files_match_source_functions(built):
    from tradingagents.agents.prompts import get_market_analyst_prompt, get_risk_manager_prompt
    _, dist = built
    base = dist / SKILL_NAME / "references" / "prompts"
    assert get_market_analyst_prompt("en") in (base / "en" / "market_analyst.md").read_text(encoding="utf-8")
    assert get_risk_manager_prompt("zh-TW") in (base / "zh-TW" / "risk_manager.md").read_text(encoding="utf-8")


def test_common_file_has_role_and_context_templates(built):
    _, dist = built
    text = (dist / SKILL_NAME / "references" / "prompts" / "zh-TW" / "_common.md").read_text(encoding="utf-8")
    assert "{date}" in text and "{company}" in text and "{ticker}" in text


# ---------- vendor 可脫離 repo 使用 ----------

def test_vendored_dataflows_import_without_repo(built, tmp_path):
    """vendor 優先於（editable 安裝的）repo；所有 tradingagents.* 模組都必須來自 vendor。"""
    _, dist = built
    vendor = dist / SKILL_NAME / "vendor"
    code = (
        "import sys; "
        f"sys.path.insert(0, {str(vendor)!r}); "
        "import tradingagents.dataflows.interface; "
        "files = {n: getattr(m, '__file__', None) for n, m in sys.modules.items() "
        "if n.startswith('tradingagents') and getattr(m, '__file__', None)}; "
        "import json; print(json.dumps(files))"
    )
    proc = subprocess.run([sys.executable, "-I", "-c", code], cwd=tmp_path,
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    files = json.loads(proc.stdout.strip().splitlines()[-1])
    assert files, "沒有載入任何 tradingagents 模組"
    outside = {n: f for n, f in files.items() if not f.startswith(str(vendor))}
    assert not outside, f"這些模組沒有被 vendor，退回使用 repo：{outside}"


def test_vendored_pdf_generator_is_identical_to_backend(built):
    _, dist = built
    vendored = (dist / SKILL_NAME / "vendor" / "pdf_generator.py").read_bytes()
    assert vendored == (REPO / "backend/app/services/pdf_generator.py").read_bytes()


# ---------- 來源與安全檢查 ----------

def test_missing_skill_md_fails(bs, tmp_path):
    src = make_source(tmp_path)
    (src / "SKILL.md").unlink()
    with pytest.raises(bs.BuildError) as exc:
        bs.build(src, tmp_path / "dist")
    assert exc.value.code == 2


@pytest.mark.parametrize("front", [
    "name: wrong-name\ndescription: x\n",
    "name: tradingagentsx-analyze\n",
    "description: x\n",
    "name: Bad_Name\ndescription: x\n",
])
def test_bad_frontmatter_fails(bs, tmp_path, front):
    src = make_source(tmp_path)
    (src / "SKILL.md").write_text(f"---\n{front}---\n\nbody\n", encoding="utf-8")
    with pytest.raises(bs.BuildError) as exc:
        bs.build(src, tmp_path / "dist")
    assert exc.value.code == 2


def test_refuses_to_overwrite_foreign_directory(bs, tmp_path):
    src = make_source(tmp_path)
    foreign = tmp_path / "dist" / SKILL_NAME
    foreign.mkdir(parents=True)
    (foreign / "precious.txt").write_text("keep me", encoding="utf-8")
    with pytest.raises(bs.BuildError) as exc:
        bs.build(src, tmp_path / "dist")
    assert exc.value.code == 3
    assert (foreign / "precious.txt").read_text(encoding="utf-8") == "keep me"


def test_no_fonts_option_skips_fonts(bs, tmp_path):
    src = make_source(tmp_path)
    result = bs.build(src, tmp_path / "dist", include_fonts=False)
    with zipfile.ZipFile(result["zip"]) as zf:
        assert not [n for n in zf.namelist() if "NotoSerifTC" in n]


def test_missing_font_source_fails(bs, tmp_path):
    src = make_source(tmp_path)
    with pytest.raises(bs.BuildError) as exc:
        bs.build(src, tmp_path / "dist", font_dir=tmp_path / "no_fonts")
    assert exc.value.code == 4


# ---------- 命令列 ----------

def test_cli_prints_json_summary(bs, tmp_path, capsys):
    src = make_source(tmp_path)
    code = bs.main(["--source", str(src), "--out", str(tmp_path / "dist")])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert out["name"] == SKILL_NAME
    assert out["files"] > 50
    assert out["zip_bytes"] > 1_000_000


def test_cli_bad_source_returns_2(bs, tmp_path, capsys):
    code = bs.main(["--source", str(tmp_path / "nope"), "--out", str(tmp_path / "dist")])
    assert code == 2
    assert capsys.readouterr().out == ""


# ---------- 真實 skill 來源 ----------

@pytest.fixture(scope="module")
def real_build(bs, tmp_path_factory):
    out = tmp_path_factory.mktemp("real")
    return bs.build(bs.DEFAULT_SOURCE, out), out


def test_real_skill_builds_with_valid_frontmatter(bs, real_build):
    result, out = real_build
    fields = bs.read_frontmatter(out / SKILL_NAME / "SKILL.md")
    assert fields["name"] == SKILL_NAME
    assert 50 < len(fields["description"]) <= 1024


GEMINI_SUFFIXES = {".pdf", ".csv", ".py", ".txt", ".md"}  # Gemini 技能上傳只收這些副檔名


def test_built_folder_only_has_gemini_supported_file_types(real_build):
    """Gemini 上傳技能資料夾時，含其他副檔名（ttf、無副檔名的標記檔…）會被整個拒絕。"""
    _, out = real_build
    root = out / SKILL_NAME
    unsupported = sorted(
        str(p.relative_to(root)) for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() not in GEMINI_SUFFIXES
    )
    assert not unsupported, unsupported


def test_packed_fonts_restore_to_loadable_ttf(real_build, tmp_path):
    """壓縮文字檔還原後必須是可用的 TTF，且仍含常用繁中字。"""
    import base64
    import zlib
    from fontTools.ttLib import TTFont
    _, out = real_build
    for style in ("Regular", "Bold"):
        pack = (out / SKILL_NAME / "assets" / f"NotoSerifTC-{style}.b64.txt").read_text(encoding="ascii")
        ttf = tmp_path / f"{style}.ttf"
        ttf.write_bytes(zlib.decompress(base64.b64decode(pack)))
        cmap = TTFont(str(ttf)).getBestCmap()
        for char in "台積電買入賣出持有風險鑫穎，。：％":
            assert ord(char) in cmap, (style, char)


def test_built_skill_renders_zh_pdf_from_packed_fonts(real_build, tmp_path):
    """建置產物（只有 .txt 字型）在乾淨環境執行 render_pdf.py，要能產出繁中 PDF。"""
    import subprocess
    _, out = real_build
    work = tmp_path / "work"
    (work / "reports").mkdir(parents=True)
    (work / "reports" / "market.md").write_text("## 技術面\n\n台積電買入，風險可控。\n", encoding="utf-8")
    env = {**os.environ, "TMPDIR": str(tmp_path / "tmp")}
    (tmp_path / "tmp").mkdir()
    proc = subprocess.run(
        [sys.executable, "-I", str(out / SKILL_NAME / "scripts" / "render_pdf.py"),
         "--workdir", str(work), "--ticker", "2330", "--date", "2026-11-26", "--lang", "zh-TW"],
        capture_output=True, text=True, env=env, timeout=180,
    )
    assert proc.returncode == 0, proc.stderr[-800:]
    pdfs = list(work.glob("*.pdf"))
    assert len(pdfs) == 1 and pdfs[0].read_bytes().startswith(b"%PDF")


def test_skill_md_mentions_only_existing_files(real_build):
    """SKILL.md 與 web-mode.md 內提到的 scripts/references 路徑，產物裡都要存在。"""
    import re
    _, out = real_build
    root = out / SKILL_NAME
    mentioned = set()
    for doc in (root / "SKILL.md", root / "references" / "web-mode.md"):
        text = doc.read_text(encoding="utf-8")
        mentioned |= set(re.findall(r"(?:scripts/\w+\.py|references/web-mode\.md|assets/[\w.-]+\.txt)", text))
    assert {"scripts/fetch_data.py", "scripts/indicators.py", "scripts/render_pdf.py",
            "references/web-mode.md"} <= mentioned
    missing = [m for m in sorted(mentioned) if not (root / m).exists()]
    assert not missing, missing


def test_skill_md_prompt_files_exist_for_both_languages(real_build):
    import re
    _, out = real_build
    text = (out / SKILL_NAME / "SKILL.md").read_text(encoding="utf-8")
    names = set(re.findall(r"`(\w+\.md)`", text)) - {"SKILL.md"}
    prompt_names = {n for n in names if n.split(".")[0] in AGENTS}
    assert prompt_names == {f"{a}.md" for a in AGENTS}
    for lang in ("zh-TW", "en"):
        for name in prompt_names:
            assert (out / SKILL_NAME / "references" / "prompts" / lang / name).is_file(), (lang, name)


# ---------- Claude Code plugin（/plugin marketplace add / install） ----------

PLUGIN_NAME = "tradingagentsx"
COMMITTED_PLUGIN = REPO / "plugins" / PLUGIN_NAME
MARKETPLACE_JSON = REPO / ".claude-plugin" / "marketplace.json"


def test_build_plugin_layout(bs, tmp_path):
    src = make_source(tmp_path)
    plugin_dir = tmp_path / "plugins" / PLUGIN_NAME
    result = bs.build_plugin(src, plugin_dir)

    manifest = json.loads((plugin_dir / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["name"] == PLUGIN_NAME
    assert manifest["version"] and manifest["description"]
    skill = plugin_dir / "skills" / SKILL_NAME
    assert (skill / "SKILL.md").is_file()
    assert (skill / "assets" / "NotoSerifTC-Regular.b64.txt").is_file()
    assert (skill / "references" / "prompts" / "en" / "risk_manager.md").is_file()
    assert (skill / "vendor" / "pdf_generator.py").is_file()
    assert not list(plugin_dir.glob("*.zip"))
    assert result["plugin_dir"] == str(plugin_dir)


def test_build_plugin_is_reproducible(bs, tmp_path):
    src = make_source(tmp_path)
    bs.build_plugin(src, tmp_path / "a")
    bs.build_plugin(src, tmp_path / "b")
    def snapshot(root):
        return {str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}
    assert snapshot(tmp_path / "a") == snapshot(tmp_path / "b")


def test_build_plugin_refuses_foreign_directory(bs, tmp_path):
    src = make_source(tmp_path)
    foreign = tmp_path / "plugins" / PLUGIN_NAME
    foreign.mkdir(parents=True)
    (foreign / "mine.txt").write_text("keep", encoding="utf-8")
    with pytest.raises(bs.BuildError) as exc:
        bs.build_plugin(src, foreign)
    assert exc.value.code == 3
    assert (foreign / "mine.txt").exists()


def test_cli_plugin_mode(bs, tmp_path, capsys):
    src = make_source(tmp_path)
    code = bs.main(["--source", str(src), "--plugin", "--plugin-dir", str(tmp_path / "p")])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert (tmp_path / "p" / ".claude-plugin" / "plugin.json").is_file()
    assert out["plugin_dir"] == str(tmp_path / "p")


def test_marketplace_manifest_points_to_committed_plugin():
    data = json.loads(MARKETPLACE_JSON.read_text(encoding="utf-8"))
    assert data["name"] == PLUGIN_NAME
    assert data["owner"]["name"]
    entries = {p["name"]: p for p in data["plugins"]}
    assert PLUGIN_NAME in entries
    source = entries[PLUGIN_NAME]["source"]
    assert source == f"./plugins/{PLUGIN_NAME}"
    plugin_root = REPO / source
    manifest = json.loads((plugin_root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["name"] == PLUGIN_NAME
    assert (plugin_root / "skills" / SKILL_NAME / "SKILL.md").is_file()


def test_committed_plugin_matches_current_sources(bs, tmp_path):
    """原始碼、提示詞、pdf_generator 或 dataflows 改動後必須重建：
    python scripts/build_skill.py --plugin"""
    fresh = tmp_path / PLUGIN_NAME
    bs.build_plugin(bs.DEFAULT_SOURCE, fresh)

    def snapshot(root):
        return {str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}

    expected, committed = snapshot(fresh), snapshot(COMMITTED_PLUGIN)
    assert set(expected) == set(committed), (
        f"檔案清單不同：缺少 {sorted(set(expected) - set(committed))[:5]}，"
        f"多出 {sorted(set(committed) - set(expected))[:5]}；請執行 python scripts/build_skill.py --plugin")
    stale = [name for name in expected if expected[name] != committed[name]]
    assert not stale, f"這些檔案已過期：{stale[:5]}；請執行 python scripts/build_skill.py --plugin"
