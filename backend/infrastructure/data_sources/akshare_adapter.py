"""AkShare Data Adapter - A股数据获取"""
import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

import pandas as pd

logger = logging.getLogger(__name__)

# AkShare 导入可能失败（未安装），做 graceful 处理
try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    logger.warning("AkShare 未安装，实时数据功能不可用。运行 pip install akshare 安装。")


class AkShareAdapter:
    """AkShare 数据获取适配器"""

    @staticmethod
    def get_realtime_market() -> pd.DataFrame:
        """获取全市场实时行情"""
        if not AKSHARE_AVAILABLE:
            return pd.DataFrame()
        try:
            df = ak.stock_zh_a_spot_em()
            column_map = {
                "代码": "ticker",
                "名称": "name",
                "最新价": "latest_price",
                "涨跌幅": "change_pct",
                "成交量": "volume",
                "总市值": "market_cap",
                "换手率": "turnover",
            }
            df = df.rename(columns=column_map)
            keep_cols = ["ticker", "name", "latest_price", "change_pct", "volume", "market_cap", "turnover"]
            return df[[c for c in keep_cols if c in df.columns]]
        except Exception as e:
            logger.error(f"获取实时行情失败: {e}")
            return pd.DataFrame()

    @staticmethod
    def get_institutional_forecast(ticker: str) -> pd.DataFrame:
        """获取机构盈利预测"""
        if not AKSHARE_AVAILABLE:
            return pd.DataFrame()
        try:
            df = ak.stock_yjyg_em(symbol=ticker)
            column_map = {
                "代码": "ticker",
                "名称": "name",
                "研报数": "source_count",
                "机构预测每股收益": "eps_forecast_neutral",
                "机构预测净利润增幅": "net_profit_growth",
            }
            df = df.rename(columns=column_map)
            return df
        except Exception as e:
            logger.error(f"获取 {ticker} 盈利预测失败: {e}")
            return pd.DataFrame()

    @staticmethod
    def get_daily_kline(ticker: str, days: int = 90) -> pd.DataFrame:
        """获取日 K 线"""
        if not AKSHARE_AVAILABLE:
            return pd.DataFrame()
        try:
            prefix = "sh" if ticker.startswith("6") else "sz"
            if ticker.startswith("68") or ticker.startswith("30"):
                prefix = "sz" if ticker.startswith("30") else "sh"
            symbol = f"{prefix}{ticker}"

            end_date = datetime.now().strftime("%Y%m%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")

            df = ak.stock_zh_a_hist(
                symbol=symbol,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust="qfq"
            )
            column_map = {
                "日期": "trade_date",
                "开盘": "open",
                "收盘": "close",
                "最高": "high",
                "最低": "low",
                "成交量": "volume",
            }
            df = df.rename(columns=column_map)
            df["ticker"] = ticker
            return df[["ticker", "trade_date", "open", "high", "low", "close", "volume"]]
        except Exception as e:
            logger.error(f"获取 {ticker} K线失败: {e}")
            return pd.DataFrame()
