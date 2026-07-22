import aiohttp
import config
from utils.cache import exchange_cache
from utils.logger import setup_logger

logger = setup_logger("bot.exchange")

BASE_URL = "https://v6.exchangerate-api.com/v6"

# Các đồng tiền hay dùng
DEFAULT_CURRENCIES = ["USD", "EUR", "JPY", "CNY", "KRW", "GBP", "SGD"]

async def get_rates(base: str = "VND") -> dict:
    """Lấy tỷ giá theo đồng tiền gốc."""
    cache_key = f"rates:{base.upper()}"
    cached = exchange_cache.get(cache_key)
    if cached:
        logger.debug(f"Cache hit: {cache_key}")
        return cached

    url = f"{BASE_URL}/{config.EXCHANGE_API_KEY}/latest/{base.upper()}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 404:
                raise ValueError(f"Không tìm thấy đồng tiền: **{base}**")
            if resp.status == 401:
                raise ValueError("API key không hợp lệ!")
            if resp.status != 200:
                raise ValueError(f"Lỗi API: {resp.status}")

            data = await resp.json()
            if data["result"] != "success":
                raise ValueError(f"Lỗi: {data.get('error-type', 'Unknown')}")
            exchange_cache.set(cache_key, data)
            logger.info(f"Fetched exchange rates for {base.upper()}")
            return data


async def convert(amount: float, from_cur: str, to_cur: str) -> dict:
    """Quy đổi tiền tệ."""
    url = f"{BASE_URL}/{config.EXCHANGE_API_KEY}/pair/{from_cur.upper()}/{to_cur.upper()}/{amount}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise ValueError(f"Lỗi API: {resp.status}")

            data = await resp.json()
            if data["result"] != "success":
                raise ValueError(f"Đồng tiền không hợp lệ!")
            return data


# Map emoji cờ cho từng đồng tiền
CURRENCY_FLAG = {
    "USD": "🇺🇸", "EUR": "🇪🇺", "JPY": "🇯🇵",
    "CNY": "🇨🇳", "KRW": "🇰🇷", "GBP": "🇬🇧",
    "SGD": "🇸🇬", "VND": "🇻🇳", "THB": "🇹🇭",
    "AUD": "🇦🇺", "CAD": "🇨🇦", "HKD": "🇭🇰",
}

def flag(currency: str) -> str:
    return CURRENCY_FLAG.get(currency.upper(), "💱")