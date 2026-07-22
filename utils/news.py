import aiohttp
import config

BASE_URL = "https://newsapi.org/v2"

# Các nguồn tin công nghệ uy tín
TECH_SOURCES = "techcrunch,the-verge,wired,ars-technica,hacker-news"

async def get_tech_news(query: str = None, page_size: int = 5) -> list[dict]:
    """Lấy tin tức công nghệ mới nhất."""
    if query:
        url = f"{BASE_URL}/everything"
        params = {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": page_size,
            "apiKey": config.NEWS_API_KEY,
        }
    else:
        url = f"{BASE_URL}/top-headlines"
        params = {
            "category": "technology",
            "language": "en",
            "pageSize": page_size,
            "apiKey": config.NEWS_API_KEY,
        }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status == 401:
                raise ValueError("API key không hợp lệ!")
            if resp.status != 200:
                raise ValueError(f"Lỗi API: {resp.status}")

            data = await resp.json()
            if data["status"] != "ok":
                raise ValueError(f"Lỗi: {data.get('message', 'Unknown')}")

            return data["articles"]


def parse_article(article: dict) -> dict:
    """Trích xuất thông tin cần thiết từ article."""
    return {
        "title":       article.get("title", "No title"),
        "source":      article.get("source", {}).get("name", "Unknown"),
        "url":         article.get("url", ""),
        "description": article.get("description") or "Không có mô tả.",
        "published":   article.get("publishedAt", "")[:10],  # YYYY-MM-DD
        "image":       article.get("urlToImage", ""),
    }