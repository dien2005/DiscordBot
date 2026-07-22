from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import discord
import io
import config
from utils.weather import get_weather, parse_weather, weather_emoji
from utils.exchange import get_rates, flag, DEFAULT_CURRENCIES
from db.queries import save_weather, save_exchange
from utils.chart import create_exchange_chart, create_weather_chart
from db.queries import get_exchange_history, get_weather_history
from utils.news import get_tech_news, parse_article
from utils.logger import setup_logger

logger = setup_logger("bot.scheduler")

# Thành phố mặc định cho báo cáo
DEFAULT_CITY = "Ho Chi Minh City"
DEFAULT_BASE = "USD"

scheduler = AsyncIOScheduler(timezone="Asia/Ho_Chi_Minh")


def setup_scheduler(bot: discord.Client):
    """Đăng ký các task định kỳ."""

    # Báo cáo sáng 8h mỗi ngày
    scheduler.add_job(
        morning_report,
        trigger=CronTrigger(hour=8, minute=0),
        args=[bot],
        id="morning_report",
        replace_existing=True
    )

    # Lưu tỷ giá mỗi 6 tiếng
    scheduler.add_job(
        auto_save_exchange,
        trigger=CronTrigger(hour="0,6,12,18", minute=0),
        args=[bot],
        id="auto_save_exchange",
        replace_existing=True
    )

    # Lưu thời tiết mỗi 3 tiếng
    scheduler.add_job(
        auto_save_weather,
        trigger=CronTrigger(hour="0,3,6,9,12,15,18,21", minute=0),
        args=[bot],
        id="auto_save_weather",
        replace_existing=True
    )

    scheduler.start()
    logger.info("Scheduler started")


async def morning_report(bot: discord.Client):
    """Báo cáo tổng hợp gửi mỗi sáng 8h."""
    try:
        channel = await bot.fetch_channel(config.REPORT_CHANNEL_ID)
    except Exception as e:
        logger.error(f"Không tìm thấy channel: {e}")
        return
    if not channel:
        logger.error("Không tìm thấy channel báo cáo!")
        return

    try:
        # Thời tiết 
        weather_data = await get_weather(DEFAULT_CITY)
        w = parse_weather(weather_data)
        await save_weather(w["city"], w["temp"], w["humidity"], w["description"])
        emoji = weather_emoji(w["icon"])

        # Tỷ giá
        exchange_data = await get_rates(DEFAULT_BASE)
        rates = exchange_data["conversion_rates"]
        currencies = DEFAULT_CURRENCIES.copy()
        if DEFAULT_BASE in currencies:
            currencies.remove(DEFAULT_BASE)
        for cur in currencies:
            if cur in rates:
                await save_exchange(DEFAULT_BASE, cur, rates[cur])

        # Embed chính
        embed = discord.Embed(
            title="Báo cáo buổi sáng",
            description="Tổng hợp thông tin đầu ngày",
            color=discord.Color.orange()
        )

        # Thời tiết
        embed.add_field(
            name=f"{emoji} Thời tiết {w['city']}",
            value=(
                f"🌡️ **{w['temp']}°C** (cảm giác {w['feels_like']}°C)\n"
                f"💧 Độ ẩm: **{w['humidity']}%**\n"
                f"💨 Gió: **{w['wind_speed']} m/s**\n"
                f"*{w['description']}*"
            ),
            inline=False
        )

        # Tỷ giá
        rate_lines = []
        for cur in ["VND", "EUR", "JPY", "CNY", "KRW"]:
            if cur in rates:
                rate = rates[cur]
                if rate >= 1000:
                    fmt = f"{rate:,.0f}"
                elif rate >= 1:
                    fmt = f"{rate:,.4f}"
                else:
                    fmt = f"{rate:.6f}"
                rate_lines.append(f"{flag(cur)} **{cur}**: {fmt}")

        embed.add_field(
            name=f"💱 Tỷ giá {DEFAULT_BASE} hôm nay",
            value="\n".join(rate_lines),
            inline=False
        )

        embed.set_footer(text="Bot báo cáo tự động · Oracle 23ai")

        # Biểu đồ tỷ giá đính kèm
        files = []
        exchange_history = await get_exchange_history(DEFAULT_BASE, "VND", days=7)
        if exchange_history:
            buf = create_exchange_chart(exchange_history, DEFAULT_BASE, "VND")
            files.append(discord.File(buf, filename="exchange_chart.png"))
            embed.set_image(url="attachment://exchange_chart.png")
        # news    
        try:
            articles = await get_tech_news(page_size=3)
            news_lines = []
            for i, article in enumerate(articles, 1):
                a = parse_article(article)
                news_lines.append(f"{i}. [{a['title'][:60]}...]({a['url']})")
            
            embed.add_field(
                name="📰 Tin tức IT sáng nay",
                value="\n".join(news_lines),
                inline=False
            )
        except Exception:
            pass
        await channel.send(embed=embed, files=files)
        logger.info("Morning report sent!")
    except Exception as e:
        logger.error(f"Morning report error: {e}")
        await channel.send(f"Lỗi báo cáo sáng: {e}")


async def auto_save_exchange(bot: discord.Client):
    """Tự động lưu tỷ giá định kỳ."""
    try:
        data = await get_rates(DEFAULT_BASE)
        rates = data["conversion_rates"]
        currencies = DEFAULT_CURRENCIES.copy()
        if DEFAULT_BASE in currencies:
            currencies.remove(DEFAULT_BASE)
        for cur in currencies:
            if cur in rates:
                await save_exchange(DEFAULT_BASE, cur, rates[cur])
        logger.info("Auto saved exchange rates")
    except Exception as e:
        logger.error(f"Auto save exchange error: {e}")


async def auto_save_weather(bot: discord.Client):
    """Tự động lưu thời tiết định kỳ."""
    try:
        data = await get_weather(DEFAULT_CITY)
        w = parse_weather(data)
        await save_weather(w["city"], w["temp"], w["humidity"], w["description"])
        logger.info("Auto saved weather")
    except Exception as e:
        logger.error(f"Auto save weather error: {e}")