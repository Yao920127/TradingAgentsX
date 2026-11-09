import logging
import threading
import time
import pandas as pd
import polars as pl
import yfinance as yf
from stockstats import wrap
from typing import Annotated, Callable
import os
from .config import get_config, DATA_DIR

logger = logging.getLogger(__name__)


_cache_locks: dict[str, threading.Lock] = {}
_cache_locks_guard = threading.Lock()


def _lock_for(path: str) -> threading.Lock:
    """每個快取檔案一把鎖，避免平行工具呼叫同時讀寫同一個 CSV。"""
    with _cache_locks_guard:
        return _cache_locks.setdefault(path, threading.Lock())


def load_price_csv_cached(
    data_file: str,
    download: Callable[[], pd.DataFrame],
    max_age_hours: float | None = None,
) -> pd.DataFrame:
    """
    讀取（或下載並寫入）價格快取，回傳 pandas DataFrame（Date 為 datetime）。

    - 以檔案鎖序列化平行呼叫，避免讀到寫到一半的檔案。
    - 以暫存檔 + os.replace 原子寫入。
    - 快取損壞（解析失敗）時刪除並重新下載。
    """
    with _lock_for(data_file):
        if os.path.exists(data_file):
            fresh = (
                max_age_hours is None
                or (time.time() - os.path.getmtime(data_file)) / 3600 < max_age_hours
            )
            if fresh:
                try:
                    df = pd.read_csv(data_file)
                    df["Date"] = pd.to_datetime(df["Date"])
                    return df
                except Exception as e:
                    logger.warning(f"價格快取損壞，將刪除並重新下載 {data_file}: {e}")
                    os.remove(data_file)

        df = download().reset_index(drop=True)
        if "Date" not in df.columns:
            df = df.reset_index()
        tmp_file = f"{data_file}.{os.getpid()}.{threading.get_ident()}.tmp"
        df.to_csv(tmp_file, index=False)
        os.replace(tmp_file, data_file)
        df["Date"] = pd.to_datetime(df["Date"])
        return df


class StockstatsUtils:
    """
    一個提供股票統計功能的工具類別。
    注意: stockstats 函式庫需要 pandas DataFrame，所以需要進行 pandas/polars 轉換。
    """
    @staticmethod
    def get_stock_stats(
        symbol: Annotated[str, "公司的股票代碼"],
        indicator: Annotated[
            str, "基於公司股票數據的量化指標"
        ],
        curr_date: Annotated[
            str, "用於檢索股價數據的當前日期，格式為 YYYY-mm-dd"
        ],
    ):
        """
        獲取指定股票和指標的統計數據。

        Args:
            symbol (str): 公司的股票代碼。
            indicator (str): 要計算的量化指標。
            curr_date (str): 當前日期。

        Returns:
            float or str: 指標值或錯誤訊息。
        """
        from datetime import datetime, timedelta
        
        # 獲取設定並設定數據目錄路徑
        config = get_config()
        online = config["data_vendors"]["technical_indicators"] != "local"

        df = None
        data = None

        if not online:
            try:
                data = pl.read_csv(
                    os.path.join(
                        DATA_DIR, # type: ignore
                        f"{symbol}-YFin-data-2015-01-01-2025-03-25.csv",
                    ) # type: ignore
                )
                # stockstats 需要 pandas DataFrame
                data_pd = data.to_pandas()
                df = wrap(data_pd)
            except FileNotFoundError:
                raise Exception("Stockstats 失敗：尚未獲取 Yahoo Finance 數據！")
        else:
            # 獲取今天的日期 (YYYY-mm-dd) 以添加到快取
            today_date = datetime.now()
            curr_date_dt = datetime.strptime(curr_date, "%Y-%m-%d")

            end_date = today_date
            start_date = today_date - timedelta(days=365*15)
            start_date_str = start_date.strftime("%Y-%m-%d")
            end_date_str = end_date.strftime("%Y-%m-%d")

            # 獲取設定並確保快取目錄存在
            os.makedirs(config["data_cache_dir"], exist_ok=True)

            data_file = os.path.join(
                config["data_cache_dir"],
                f"{symbol}-YFin-data-{start_date_str}-{end_date_str}.csv",
            )

            def _download() -> pd.DataFrame:
                return yf.download(
                    symbol,
                    start=start_date_str,
                    end=end_date_str,
                    multi_level_index=False,
                    progress=False,
                    auto_adjust=False,
                ).reset_index()  # type: ignore

            data_pd = load_price_csv_cached(data_file, _download)
            df = wrap(data_pd)
            df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
            curr_date = curr_date_dt.strftime("%Y-%m-%d")

        df[indicator]  # 觸發 stockstats 計算指標
        matching_rows = df[df["Date"].str.startswith(curr_date)]

        if not matching_rows.empty:
            indicator_value = matching_rows[indicator].values[0]
            return indicator_value
        else:
            # 區分「真的是週末」與「平日卻無值」（假日、尚未上市或資料不足），
            # 避免把平日交易日誤標為週末假日。
            try:
                is_weekend = datetime.strptime(curr_date, "%Y-%m-%d").weekday() >= 5
            except Exception:
                is_weekend = False
            if is_weekend:
                return "N/A：非交易日 (週末)"
            return "N/A：無資料 (假日、個股尚未上市，或歷史資料不足以計算此指標)"