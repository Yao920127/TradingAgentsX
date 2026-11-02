"""
Download Service for Analyst Reports
Generates combined PDF reports with all analyst analyses
"""
import io
import logging
from typing import List, Dict, Optional
from datetime import datetime

from backend.app.services.pdf_generator import PDFGenerator
from tradingagents.dataflows.news_models import resolve_company_name
from tradingagents.dataflows.finmind_common import _make_api_request, get_yfinance_ticker, normalize_stock_id

logger = logging.getLogger(__name__)


# 分析師中英文名稱對照表
ANALYST_NAME_MAPPING = {
    # 分析師組
    "市場分析師": "Market_Analyst",
    "基本面分析師": "Fundamentals_Analyst",
    "社群媒體分析師": "Social_Media_Analyst",
    "新聞分析師": "News_Analyst",
    
    # 研究員組
    "看漲研究員": "Bull_Researcher",
    "看跌研究員": "Bear_Researcher",
    
    # 風險辯論者組
    "激進分析師": "Aggressive_Debator",
    "保守分析師": "Conservative_Debator",
    "中立分析師": "Neutral_Debator",
    
    # 經理組
    "研究經理": "Research_Manager",
    "風險經理": "Risk_Manager",
    
    # 交易員
    "交易員": "Trader",
}


def _is_taiwan_ticker(ticker: str) -> bool:
    return bool(ticker) and ticker.strip()[0].isdigit()


_finmind_name_cache: Dict[str, str] = {}


def _finmind_stock_name(ticker: str) -> str:
    """以 FinMind TaiwanStockInfo 取得台股中文簡稱（如 2379 → 瑞昱），失敗回傳空字串（不快取失敗）。"""
    if ticker in _finmind_name_cache:
        return _finmind_name_cache[ticker]
    try:
        stock_id = normalize_stock_id(ticker)
        response = _make_api_request(dataset="TaiwanStockInfo", data_id=stock_id)
        for item in response.get("data") or []:
            if item.get("stock_id") == stock_id and item.get("stock_name"):
                _finmind_name_cache[ticker] = item["stock_name"]
                return item["stock_name"]
    except Exception as e:
        logger.warning("FinMind 取得 %s 公司名稱失敗：%s", ticker, e)
    return ""


def resolve_cover_company_name(ticker: str) -> str:
    """解析封面公司全名：一律優先英文名（yfinance），台股查不到時退回 FinMind 中文名，再不行回傳 ticker。"""
    if not _is_taiwan_ticker(ticker):
        return resolve_company_name(ticker)

    yf_name = ""
    try:
        primary = get_yfinance_ticker(ticker)
        base = primary.split(".")[0]
        # 市場類型不明時 get_yfinance_ticker 預設 .TW，上櫃股需再試 .TWO
        for candidate in dict.fromkeys((primary, f"{base}.TW", f"{base}.TWO")):
            name = resolve_company_name(candidate)
            if name != candidate:
                yf_name = name
                break
    except Exception as e:
        logger.warning("yfinance 取得 %s 公司名稱失敗：%s", ticker, e)

    return yf_name or _finmind_stock_name(ticker) or ticker


class DownloadService:
    """Service for handling analyst report downloads"""
    
    def __init__(self):
        """Initialize download service"""
        self.pdf_generator = PDFGenerator()
    
    def create_combined_pdf(
        self,
        ticker: str,
        analysis_date: str,
        reports: List[Dict[str, str]],
        price_data: list = None, # type: ignore
        price_stats: dict = None, # type: ignore
        language: str = "zh-TW",
        deep_think_llm: str = None, # type: ignore
        quick_think_llm: str = None, # type: ignore
    ) -> tuple[bytes, str]:
        """
        Create a single combined PDF containing all analyst reports
        
        Features:
        - Cover page with ticker and analysis date
        - Table of contents with price chart and analyst list
        - All analyst reports as separate sections
        
        Args:
            ticker: Stock ticker symbol
            analysis_date: Date of analysis (YYYY-MM-DD)
            reports: List of dicts with keys 'analyst_name' and 'report_content'
            price_data: Optional list of price data for chart
            price_stats: Optional price statistics for TOC
            language: Language for PDF labels ('en' or 'zh-TW')
            
        Returns:
            Tuple of (PDF bytes, filename)
        """
        # Define the preferred order for analysts (based on language)
        if language == "en":
            analyst_order = [
                'Market Analyst',
                'Fundamentals Analyst', 
                'Social Media Analyst',
                'News Analyst',
                'Bull Researcher',
                'Bear Researcher',
                'Aggressive Analyst',
                'Conservative Analyst',
                'Neutral Analyst',
                'Research Manager',
                'Risk Manager',
                'Trader',
            ]
        else:
            analyst_order = [
                '市場分析師',
                '基本面分析師', 
                '社群媒體分析師',
                '新聞分析師',
                '看漲研究員',
                '看跌研究員',
                '激進分析師',
                '保守分析師',
                '中立分析師',
                '研究經理',
                '風險經理',
                '交易員',
            ]
        
        # Sort reports by preferred order
        def get_order(report):
            analyst_name = report.get('analyst_name', '')
            try:
                return analyst_order.index(analyst_name)
            except ValueError:
                return len(analyst_order)  # Unknown analysts go to the end
        
        sorted_reports = sorted(reports, key=get_order)
        
        # Resolve company full name for the cover page (falls back to ticker)
        company_name = resolve_cover_company_name(ticker)

        # Generate combined PDF
        pdf_bytes = self.pdf_generator.generate_combined_report_pdf(
            ticker=ticker,
            analysis_date=analysis_date,
            reports=sorted_reports,
            price_data=price_data,
            price_stats=price_stats,
            language=language,
            deep_think_llm=deep_think_llm,
            quick_think_llm=quick_think_llm,
            company_name=company_name,
        )
        
        # Generate filename: TICKER_Combined_Report_DATE.pdf
        filename = f"{ticker}_Report_{analysis_date}.pdf"
        
        return pdf_bytes, filename


# Singleton instance
download_service = DownloadService()
