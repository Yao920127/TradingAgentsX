"""PDF 孤頁測試：章節最後一頁只剩一點點內容時，應縮小行高讓它塞回前一頁。"""
import pytest

from backend.app.services.pdf_generator import PDFGenerator


@pytest.fixture(scope="module")
def gen():
    return PDFGenerator()


def _pages(gen, scale, body):
    gen._line_scale = scale
    try:
        pdf = gen._new_pdf()
        gen._render_analyst_section(pdf, "市場分析師", "NVDA", "2026-11-27", body)
        return pdf.page, pdf.get_y() - pdf.t_margin
    finally:
        gen._line_scale = 1.0


def _body_with_overflow(gen, extra_lines):
    return "\n".join(f"- 第 {i} 行內容，用來撐滿一整頁的篇幅。" for i in range(extra_lines))


def _find_overflowing_body(gen):
    """找出在 scale=1.0 時恰好多出一頁、且尾頁很短的內容。"""
    for n in range(20, 80):
        body = _body_with_overflow(gen, n)
        pages, tail = _pages(gen, 1.0, body)
        if pages == 2 and tail < 30:
            return body
    pytest.skip("找不到剛好溢出的內容長度")


def test_tiny_tail_is_compacted_into_one_page(gen):
    body = _find_overflowing_body(gen)
    scale = gen._pick_line_scale("市場分析師", "NVDA", "2026-11-27", body)
    assert scale < 1.0
    pages, _ = _pages(gen, scale, body)
    assert pages == 1


def test_normal_report_keeps_default_scale(gen):
    body = "- 一行短內容。"
    assert gen._pick_line_scale("市場分析師", "NVDA", "2026-11-27", body) == 1.0


def test_section_build_restores_scale(gen):
    body = _find_overflowing_body(gen)
    pdf = gen._new_pdf()
    gen._build_analyst_section(pdf, "市場分析師", "NVDA", "2026-11-27", body)
    assert gen._line_scale == 1.0


TABLE = (
    "| 動作 | 價位或事件 | 倉位 |\n|---|---|---|\n"
    + "\n".join(f"| 項目{i} | 收盤站上 {100 + i} | 約 {i}% |" for i in range(6))
)


def _table_page_spans(gen, body, scale=1.0):
    """回傳每張表格 (起始頁, 結束頁)。"""
    spans = []
    original = gen._add_table
    main = {}

    def recording(pdf, data):
        start = pdf.page
        original(pdf, data)
        if pdf is main.get("pdf"):  # 略過量測用的暫存 PDF
            spans.append((start, pdf.page))

    gen._add_table = recording
    gen._line_scale = scale
    try:
        pdf = gen._new_pdf()
        main["pdf"] = pdf
        gen._render_analyst_section(pdf, "激進分析師", "NVDA", "2026-11-27", body)
    finally:
        del gen._add_table
        gen._line_scale = 1.0
    return spans


def test_table_that_fits_one_page_is_never_split(gen):
    splits = []
    for n in range(10, 45):
        body = _body_with_overflow(gen, n) + "\n\n" + TABLE
        for start, end in _table_page_spans(gen, body):
            if start != end:
                splits.append(n)
    assert splits == []


def test_table_moves_to_next_page_when_it_would_split(gen):
    """至少有一種填充長度，表格會被整張推到第二頁（證明確實有搬動）。"""
    moved = False
    for n in range(10, 45):
        body = _body_with_overflow(gen, n) + "\n\n" + TABLE
        spans = _table_page_spans(gen, body)
        if spans and spans[0][0] == 2:
            moved = True
            break
    assert moved


def test_table_tail_orphan_is_compacted_when_small_overflow(gen):
    """表格剛好多出一點時，縮小行高後整份應回到一頁。"""
    for n in range(10, 45):
        body = _body_with_overflow(gen, n) + "\n\n" + TABLE
        if _pages(gen, 1.0, body)[0] == 2:
            scale = gen._pick_line_scale("激進分析師", "NVDA", "2026-11-27", body)
            pages_after, _ = _pages(gen, scale, body)
            pages_before = 2
            assert pages_after <= pages_before
            if pages_after == 1:
                return
    pytest.skip("找不到可壓回一頁的長度")
