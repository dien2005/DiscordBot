import discord
from discord.ext import commands
from utils.weather import get_weather, get_forecast, parse_weather, weather_emoji
from datetime import datetime
from db.queries import save_weather, get_weather_stats, get_weather_history
from utils.chart import create_weather_chart

class WeatherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # weather
    @discord.app_commands.command(
        name="weather",
        description="Xem thời tiết hiện tại của một thành phố"
    )
    @discord.app_commands.describe(city="Tên thành phố (vd: Hanoi, Ho Chi Minh City)")
    async def weather(self, interaction: discord.Interaction, city: str):
        await interaction.response.defer()
        try:
            data = await get_weather(city)
            w = parse_weather(data)
            emoji = weather_emoji(w["icon"])

            embed = discord.Embed(
                title=f"{emoji} Thời tiết tại {w['city']}, {w['country']}",
                description=f"*{w['description']}*",
                color=discord.Color.blurple(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(
                name="🌡️ Nhiệt độ",
                value=f"**{w['temp']}°C**\nCảm giác: {w['feels_like']}°C\nMin/Max: {w['temp_min']}°C / {w['temp_max']}°C",
                inline=True
            )
            embed.add_field(
                name="💧 Độ ẩm & Gió",
                value=f"Độ ẩm: **{w['humidity']}%**\nGió: **{w['wind_speed']} m/s**\nTầm nhìn: {w['visibility']} km",
                inline=True
            )
            embed.set_thumbnail(
                url=f"https://openweathermap.org/img/wn/{w['icon']}@2x.png"
            )
            embed.set_footer(text="Nguồn: OpenWeatherMap")
            await interaction.followup.send(embed=embed)

        except ValueError as e:
            await interaction.followup.send(f"{e}")
        except Exception as e:
            await interaction.followup.send(f"Lỗi không xác định: {e}")

    # forecast
    @discord.app_commands.command(
        name="forecast",
        description="Dự báo thời tiết 24 giờ tới"
    )
    @discord.app_commands.describe(city="Tên thành phố")
    async def forecast(self, interaction: discord.Interaction, city: str):
        await interaction.response.defer()
        try:
            data = await get_forecast(city)
            city_name = data["city"]["name"]
            country   = data["city"]["country"]

            embed = discord.Embed(
                title=f"📅 Dự báo 24h tới — {city_name}, {country}",
                color=discord.Color.teal(),
                timestamp=datetime.utcnow()
            )

            for item in data["list"]:
                time  = datetime.fromtimestamp(item["dt"]).strftime("%H:%M %d/%m")
                temp  = round(item["main"]["temp"])
                desc  = item["weather"][0]["description"].capitalize()
                icon  = item["weather"][0]["icon"]
                emoji = weather_emoji(icon)
                humid = item["main"]["humidity"]

                embed.add_field(
                    name=f"{emoji} {time}",
                    value=f"**{temp}°C** · {desc}\n💧 {humid}%",
                    inline=True
                )

            embed.set_footer(text="Nguồn: OpenWeatherMap")
            await interaction.followup.send(embed=embed)

        except ValueError as e:
            await interaction.followup.send(f"{e}")
        except Exception as e:
            await interaction.followup.send(f"Lỗi không xác định: {e}")


    @discord.app_commands.command(
    name="weatherchart",
    description="Biểu đồ nhiệt độ & độ ẩm theo thời gian"
    )
    @discord.app_commands.describe(
        city="Tên thành phố",
        days="Số ngày (mặc định 7)"
    )
    async def weatherchart(
        self,
        interaction: discord.Interaction,
        city: str,
        days: int = 7
    ):
        await interaction.response.defer()
        try:
            history = await get_weather_history(city, days)
            if not history:
                await interaction.followup.send(
                    f"Chưa có dữ liệu cho **{city}**. Dùng `/weather` vài lần trước nhé!"
                )
                return

            buf = create_weather_chart(history, city)
            file = discord.File(buf, filename="weather_chart.png")

            embed = discord.Embed(
                title=f"🌡️ Biểu đồ thời tiết — {city} ({days} ngày)",
                color=discord.Color.teal()
            )
            embed.set_image(url="attachment://weather_chart.png")
            embed.set_footer(text="Dữ liệu từ Oracle 23ai · OpenWeatherMap")
            await interaction.followup.send(embed=embed, file=file)

        except Exception as e:
            await interaction.followup.send(f"Lỗi: {e}")

async def setup(bot):
    await bot.add_cog(WeatherCog(bot))