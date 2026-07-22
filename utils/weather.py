import aiohttp
import config
from utils.cache import weather_cache
from utils.logger import setup_logger

logger = setup_logger("bot.weather")

BASE_URL = "https://api.openweathermap.org/data/2.5"

async def get_weather(city: str) -> dict:
    """Lấy thời tiết hiện tại theo tên thành phố."""
    cache_key = f"weather:{city.lower()}"
    cached = weather_cache.get(cache_key)
    if cached:
        logger.debug(f"Cache hit: {cache_key}")
        return cached

    params = {
        "q": city,
        "appid": config.WEATHER_API_KEY,
        "units": "metric",   # độ C
        "lang": "vi",        # mô tả tiếng Việt
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/weather", params=params) as resp:
            if resp.status == 404:
                raise ValueError(f"Không tìm thấy thành phố: **{city}**")
            if resp.status == 401:
                raise ValueError("API key không hợp lệ!")
            if resp.status != 200:
                raise ValueError(f"Lỗi API: {resp.status}")
            data = await resp.json()
            weather_cache.set(cache_key, data)
            logger.info(f"Fetched weather for {city}")
            return data


async def get_forecast(city: str) -> dict:
    """Lấy dự báo 5 ngày (cách 3 tiếng/lần)."""
    cache_key = f"forecast:{city.lower()}"
    cached = weather_cache.get(cache_key)
    if cached:
        logger.debug(f"Cache hit: {cache_key}")
        return cached

    params = {
        "q": city,
        "appid": config.WEATHER_API_KEY,
        "units": "metric",
        "lang": "vi",
        "cnt": 8,   # 8 mốc = 24 giờ tới
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/forecast", params=params) as resp:
            if resp.status == 404:
                raise ValueError(f"Không tìm thấy thành phố: **{city}**")
            if resp.status != 200:
                raise ValueError(f"Lỗi API: {resp.status}")
            data = await resp.json()
            weather_cache.set(cache_key, data)
            logger.info(f"Fetched forecast for {city}")
            return data


def parse_weather(data: dict) -> dict:
    """Trích xuất thông tin cần thiết từ response."""
    return {
        "city":        data["name"],
        "country":     data["sys"]["country"],
        "temp":        round(data["main"]["temp"]),
        "feels_like":  round(data["main"]["feels_like"]),
        "temp_min":    round(data["main"]["temp_min"]),
        "temp_max":    round(data["main"]["temp_max"]),
        "humidity":    data["main"]["humidity"],
        "description": data["weather"][0]["description"].capitalize(),
        "icon":        data["weather"][0]["icon"],
        "wind_speed":  data["wind"]["speed"],
        "visibility":  data.get("visibility", 0) // 1000,  # m → km
    }


def weather_emoji(icon: str) -> str:
    """Map icon code sang emoji."""
    mapping = {
        "01": "☀️", "02": "⛅", "03": "☁️", "04": "☁️",
        "09": "🌧️", "10": "🌦️", "11": "⛈️",
        "13": "❄️", "50": "🌫️",
    }
    return mapping.get(icon[:2], "🌡️")