from typing import Annotated
from datetime import datetime
from dateutil.relativedelta import relativedelta
from concurrent.futures import ThreadPoolExecutor

from .googlenews_utils import getNewsData
from .jina_reader import read_article

# 前幾則新聞用 Jina Reader 抓全文（Google 搜尋結果只有標題與一句摘要）
JINA_TOP_N = 3


def get_google_news(
    query: Annotated[str, "用於搜索的查詢"],
    curr_date: Annotated[str, "當前日期，格式為 yyyy-mm-dd"],
    look_back_days: Annotated[int, "回溯天數"],
) -> str:
    """
    使用 Google News 檢索新聞文章。

    Args:
        query (str): 用於搜索的查詢。
        curr_date (str): 當前日期，格式為 yyyy-mm-dd。
        look_back_days (int): 回溯天數。

    Returns:
        str: 包含新聞報導的格式化字串。
    """
    query = query.replace(" ", "+")

    start_date = datetime.strptime(curr_date, "%Y-%m-%d")
    before = start_date - relativedelta(days=look_back_days)
    before = before.strftime("%Y-%m-%d")

    news_results = getNewsData(query, before, curr_date)

    if len(news_results) == 0:
        return ""

    top = news_results[:JINA_TOP_N]
    with ThreadPoolExecutor(max_workers=len(top)) as pool:
        contents = list(pool.map(lambda n: read_article(n["link"]) if n.get("link") else "", top))

    news_str = ""

    for i, news in enumerate(news_results):
        news_str += (
            f"### {news['title']} (來源: {news['source']}) \n\n{news['snippet']}\n\n"
        )
        if i < len(contents) and contents[i]:
            news_str += f"> 全文摘錄：{contents[i]}\n\n"

    return f"## {query} Google 新聞，從 {before} 到 {curr_date}：\n\n{news_str}"


def get_global_news_google(
    curr_date: Annotated[str, "當前日期，格式為 yyyy-mm-dd"],
    look_back_days: Annotated[int, "回溯天數"] = 7,
    limit: Annotated[int, "返回的最大文章數（此實作未使用，僅為供應商路由簽名一致）"] = 5,
) -> str:
    """
    全球宏觀 / 市場新聞（透過 Google News，免 API 金鑰）。

    get_global_news 供應商鏈原本只有 openai（需 OpenAI web search）與 finmind（台股），
    對使用非 OpenAI 供應商的使用者不可用。本函式以固定的總經查詢字串取代個股查詢，
    讓任何人都有一個免金鑰的全球新聞來源。
    """
    return get_google_news("stock market economy finance macro", curr_date, look_back_days)

def get_google_company_news(
    ticker: Annotated[str, "股票代碼"],
    start_date: Annotated[str, "開始日期，格式為 yyyy-mm-dd"],
    end_date: Annotated[str, "結束日期，格式為 yyyy-mm-dd"],
) -> str:
    """get_news 介面（代碼、起訖日期）的轉接：改以回溯天數呼叫 get_google_news。"""
    look_back_days = (
        datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")
    ).days
    return get_google_news(ticker, end_date, max(look_back_days, 1))
