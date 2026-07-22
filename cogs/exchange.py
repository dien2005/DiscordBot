import discord
from discord.ext import commands
from datetime import datetime
from utils.exchange import get_rates, convert, flag, DEFAULT_CURRENCIES
from db.queries import save_exchange, get_exchange_stats, get_exchange_history
from utils.chart import create_exchange_chart

class ExchangeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /tygia
    @discord.app_commands.command(
        name="tygia",
        description="Xem tỷ giá các đồng tiền so với VND"
    )
    @discord.app_commands.describe(
        base="Đồng tiền gốc (mặc định: USD)"
    )
    async def tygia(
        self,
        interaction: discord.Interaction,
        base: str = "USD"
    ):
        await interaction.response.defer()
        try:
            data = await get_rates(base.upper())
            rates = data["conversion_rates"]
            updated = data["time_last_update_utc"]

            currencies = DEFAULT_CURRENCIES.copy()
            if "VND" not in currencies:
                currencies.append("VND")
            if base.upper() in currencies:
                currencies.remove(base.upper())

            # Lưu vào DB trước
            for cur in currencies:
                if cur in rates:
                    await save_exchange(base.upper(), cur, rates[cur])

            embed = discord.Embed(
                title=f"{flag(base)} Tỷ giá {base.upper()} hôm nay",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )

            lines = []
            for cur in currencies:
                if cur in rates:
                    rate = rates[cur]
                    if rate >= 1000:
                        formatted = f"{rate:,.0f}"
                    elif rate >= 1:
                        formatted = f"{rate:,.4f}"
                    else:
                        formatted = f"{rate:.6f}"
                    lines.append(f"{flag(cur)} **{cur}**: {formatted}")

            embed.description = "\n".join(lines)
            embed.set_footer(text=f"Cập nhật: {updated[:16]} UTC · ExchangeRate-API · Đã lưu DB")
            await interaction.followup.send(embed=embed)

        except ValueError as e:
            await interaction.followup.send(f"{e}")
        except Exception as e:
            await interaction.followup.send(f"Lỗi: {e}")

    # /doitien
    @discord.app_commands.command(
        name="doitien",
        description="Quy đổi tiền tệ"
    )
    @discord.app_commands.describe(
        amount="Số tiền muốn đổi",
        from_cur="Đồng tiền nguồn (vd: USD)",
        to_cur="Đồng tiền đích (vd: VND)"
    )
    async def doitien(
        self,
        interaction: discord.Interaction,
        amount: float,
        from_cur: str,
        to_cur: str
    ):
        await interaction.response.defer()
        try:
            data = await convert(amount, from_cur, to_cur)
            result = data["conversion_result"]
            rate = data["conversion_rate"]

            embed = discord.Embed(
                title="💱 Quy đổi tiền tệ",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(
                name="Số tiền",
                value=f"{flag(from_cur)} **{amount:,.2f} {from_cur.upper()}**",
                inline=True
            )
            embed.add_field(
                name="Kết quả",
                value=f"{flag(to_cur)} **{result:,.2f} {to_cur.upper()}**",
                inline=True
            )
            embed.add_field(
                name="Tỷ giá",
                value=f"1 {from_cur.upper()} = {rate:,.4f} {to_cur.upper()}",
                inline=False
            )
            embed.set_footer(text="ExchangeRate-API")
            await interaction.followup.send(embed=embed)

        except ValueError as e:
            await interaction.followup.send(f"{e}")
        except Exception as e:
            await interaction.followup.send(f"Lỗi: {e}")

    # /exchangestats
    @discord.app_commands.command(
        name="exchangestats",
        description="Thống kê tỷ giá trong N ngày qua"
    )
    @discord.app_commands.describe(
        base="Đồng tiền gốc (vd: USD)",
        target="Đồng tiền đích (vd: VND)",
        days="Số ngày (mặc định 7)"
    )
    async def exchangestats(
        self,
        interaction: discord.Interaction,
        base: str = "USD",
        target: str = "VND",
        days: int = 7
    ):
        await interaction.response.defer()
        try:
            stats = await get_exchange_stats(base, target, days)
            if not stats or stats.get("total") == 0:
                await interaction.followup.send(
                    "Chưa có dữ liệu. Dùng `/tygia` trước nhé!"
                )
                return

            embed = discord.Embed(
                title=f"📊 Thống kê {base.upper()}/{target.upper()} ({days} ngày)",
                color=discord.Color.gold(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(
                name="📈 Min / Max",
                value=f"**{stats['min_rate']:,.4f}** / **{stats['max_rate']:,.4f}**",
                inline=True
            )
            embed.add_field(
                name="📊 Trung bình",
                value=f"**{stats['avg_rate']:,.4f}**",
                inline=True
            )
            embed.add_field(
                name="📝 Số lần ghi",
                value=f"**{int(stats['total'])}** lần",
                inline=True
            )
            embed.set_footer(text="Dữ liệu từ Oracle 23ai")
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"Lỗi: {e}")

    @discord.app_commands.command(
    name="exchangechart",
    description="Biểu đồ lịch sử tỷ giá"
    )
    @discord.app_commands.describe(
        base="Đồng tiền gốc (vd: USD)",
        target="Đồng tiền đích (vd: VND)",
        days="Số ngày (mặc định 7)"
    )
    async def exchangechart(
        self,
        interaction: discord.Interaction,
        base: str = "USD",
        target: str = "VND",
        days: int = 7
    ):
        await interaction.response.defer()
        try:
            history = await get_exchange_history(base, target, days)
            if not history:
                await interaction.followup.send(
                    "Chưa có dữ liệu. Dùng `/tygia` vài lần trước nhé!"
                )
                return

            buf = create_exchange_chart(history, base.upper(), target.upper())
            file = discord.File(buf, filename="exchange_chart.png")

            embed = discord.Embed(
                title=f"📈 Biểu đồ {base.upper()}/{target.upper()} ({days} ngày)",
                color=discord.Color.blurple()
            )
            embed.set_image(url="attachment://exchange_chart.png")
            embed.set_footer(text="Dữ liệu từ Oracle 23ai · ExchangeRate-API")
            await interaction.followup.send(embed=embed, file=file)

        except Exception as e:
            await interaction.followup.send(f"Lỗi: {e}")

async def setup(bot):
    await bot.add_cog(ExchangeCog(bot))