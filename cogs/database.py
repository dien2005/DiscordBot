import discord
from discord.ext import commands
from db.queries import test_connection
from scheduler.tasks import morning_report

class DatabaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="dbping",
        description="Kiểm tra kết nối Oracle DB"
    )
    async def dbping(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            version = await test_connection()
            embed = discord.Embed(
                title="Oracle DB Connected",
                description=f"```{version}```",
                color=discord.Color.green()
            )
            embed.set_footer(text="Oracle 23ai Free · FREEPDB1")
        except Exception as e:
            embed = discord.Embed(
                title="Kết nối thất bại",
                description=f"```{e}```",
                color=discord.Color.red()
            )
        await interaction.followup.send(embed=embed)
    @discord.app_commands.command(
        name="reportnow",
        description="Gửi báo cáo sáng ngay lập tức (để test)"
    )
    async def reportnow(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await morning_report(self.bot)
        await interaction.followup.send("Đã gửi báo cáo!")

async def setup(bot):
    await bot.add_cog(DatabaseCog(bot))