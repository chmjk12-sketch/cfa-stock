"""Zhitu Data Adapter - 机构目标价获取"""
import os
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger.warning("requests 未安装，智兔数服功能不可用。")


class ZhituAdapter:
    """智兔数服 API 适配器"""

    BASE_URL = "https://api.zhituapi.com"
    TOKEN = os.getenv("ZHITU_TOKEN", "ZHITU_TOKEN_LIMIT_TEST")

    @classmethod
    def get_target_price(cls, ticker: str) -> Optional[Dict[str, Any]]:
        """获取机构目标价"""
        if not REQUESTS_AVAILABLE:
            return None
        try:
            url = f"{cls.BASE_URL}/hs/target/{ticker}"
            params = {"token": cls.TOKEN}
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "target_price_optimistic": data.get("target_price_high"),
                    "target_price_neutral": data.get("target_price_avg"),
                    "target_price_pessimistic": data.get("target_price_low"),
                    "source_count": data.get("institution_count"),
                    "source_names": data.get("institution_names", []),
                }
            else:
                logger.warning(f"智兔 API 返回 {response.status_code}: {response.text}")
                return None
        except Exception as e:
            logger.error(f"获取 {ticker} 目标价失败: {e}")
            return None
