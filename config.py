import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "!"
REPORT_CHANNEL_ID = int(os.getenv("REPORT_CHANNEL_ID", 0))
GUILD_ID = int(os.getenv("GUILD_ID", 0))

# Database
DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "dsn": f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_SERVICE')}",
}

# API Keys
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Validation
_REQUIRED = {
    "DISCORD_TOKEN": DISCORD_TOKEN,
    "DB_USER": DB_CONFIG["user"],
    "DB_PASSWORD": DB_CONFIG["password"],
}

_missing = [k for k, v in _REQUIRED.items() if not v]
if _missing:
    print(f"[ERROR] Thiếu biến môi trường: {', '.join(_missing)}")
    print("Hãy copy .env.example thành .env và điền đầy đủ.")
    sys.exit(1)