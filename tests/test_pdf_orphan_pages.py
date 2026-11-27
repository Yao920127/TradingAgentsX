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
