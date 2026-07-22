# 🤖 Discord Bot — Thời tiết, Tỷ giá & Tin tức IT

Bot Discord đa chức năng hỗ trợ tra cứu **thời tiết**, **tỷ giá tiền tệ**, và **tin tức công nghệ** — tích hợp cơ sở dữ liệu **Oracle 23ai** để lưu trữ lịch sử và tạo biểu đồ phân tích.

## ✨ Tính năng chính

- 🌦️ **Thời tiết** — Tra cứu real-time & dự báo 24h với biểu đồ nhiệt độ/độ ẩm
- 💱 **Tỷ giá** — Xem tỷ giá, quy đổi tiền tệ, thống kê & biểu đồ lịch sử
- 📰 **Tin tức IT** — Tin công nghệ, AI/ML, bảo mật từ các nguồn uy tín
- ⏰ **Báo cáo tự động** — Tổng hợp thông tin gửi mỗi sáng 8h
- 📊 **Biểu đồ** — Visualization dữ liệu lịch sử với Matplotlib (dark theme)
- 🗄️ **Lưu trữ** — Oracle 23ai database với async connection pool

## 🛠️ Tech Stack

| Công nghệ | Mục đích |
|-----------|----------|
| **Python 3.12** | Ngôn ngữ chính |
| **discord.py 2.3+** | Discord API wrapper |
| **Oracle 23ai** (oracledb) | Cơ sở dữ liệu |
| **aiohttp** | HTTP client async |
| **APScheduler** | Scheduled tasks |
| **Matplotlib** | Biểu đồ & visualization |
| **Docker** | Containerization |

## 📁 Cấu trúc Project

```
bot_chat_discord/
├── main.py                 # Entry point
├── config.py               # Cấu hình & validation
├── requirements.txt        # Dependencies
├── Dockerfile              # Container image
├── docker-compose.yml      # Multi-container setup
│
├── cogs/                   # Slash command modules
│   ├── weather.py          # /weather, /forecast, /weatherchart
│   ├── exchange.py         # /tygia, /doitien, /exchangestats, /exchangechart
│   ├── news.py             # /technews, /ainews, /cybernews
│   └── database.py         # /dbping, /reportnow
│
├── db/                     # Database layer
│   ├── connection.py       # Async connection pool
│   └── queries.py          # SQL queries (CRUD)
│
├── scheduler/              # Background tasks
│   └── tasks.py            # Báo cáo sáng, auto-save data
│
├── utils/                  # Utilities
│   ├── weather.py          # OpenWeatherMap API client
│   ├── exchange.py         # ExchangeRate-API client
│   ├── news.py             # NewsAPI client
│   ├── chart.py            # Matplotlib chart generator
│   ├── cache.py            # TTL cache (tránh spam API)
│   └── logger.py           # Logging configuration
│
└── tests/                  # Unit tests (pytest)
    ├── test_weather_utils.py
    ├── test_exchange_utils.py
    ├── test_news_utils.py
    └── test_cache.py
```

## 📋 Danh sách Slash Commands

| Command | Mô tả |
|---------|--------|
| `/weather <city>` | Xem thời tiết hiện tại của thành phố |
| `/forecast <city>` | Dự báo thời tiết 24 giờ tới |
| `/weatherchart <city> [days]` | Biểu đồ nhiệt độ & độ ẩm theo thời gian |
| `/tygia [base]` | Xem tỷ giá các đồng tiền (mặc định: USD) |
| `/doitien <amount> <from> <to>` | Quy đổi tiền tệ |
| `/exchangestats [base] [target] [days]` | Thống kê tỷ giá trong N ngày |
| `/exchangechart [base] [target] [days]` | Biểu đồ lịch sử tỷ giá |
| `/technews [query] [count]` | Tin tức công nghệ (tìm theo từ khóa) |
| `/ainews` | Tin tức AI & Machine Learning |
| `/cybernews` | Tin tức bảo mật & network |
| `/dbping` | Kiểm tra kết nối Oracle DB |
| `/reportnow` | Gửi báo cáo tổng hợp ngay lập tức |

## ⚡ Cài đặt & Chạy

### Yêu cầu
- Python 3.10+
- Oracle Database 23ai Free
- API Keys: [OpenWeatherMap](https://openweathermap.org/api), [ExchangeRate-API](https://www.exchangerate-api.com/), [NewsAPI](https://newsapi.org/)

### Bước 1: Clone & cài đặt

```bash
git clone https://github.com/your-username/bot_chat_discord.git
cd bot_chat_discord

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
```

### Bước 2: Cấu hình

```bash
copy .env.example .env       # Windows
# cp .env.example .env       # Linux/Mac
```

Mở file `.env` và điền các thông tin cần thiết (Discord token, API keys, DB credentials).

### Bước 3: Chạy bot

```bash
python main.py
```

### Chạy với Docker (khuyên dùng)

```bash
docker-compose up -d
```

### Chạy tests

```bash
pip install pytest
pytest tests/ -v
```

## 🔗 Nguồn API

- [OpenWeatherMap API](https://openweathermap.org/api) — Dữ liệu thời tiết
- [ExchangeRate-API](https://www.exchangerate-api.com/) — Tỷ giá tiền tệ
- [NewsAPI](https://newsapi.org/) — Tin tức công nghệ

## 📄 License

MIT License
