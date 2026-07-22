import discord
from discord.ext import commands
from datetime import datetime
from utils.news import get_tech_news, parse_article


class NewsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #  /technews 
    @discord.app_commands.command(
        name="technews",
        description="Tin tức công nghệ mới nhất"
    )
    @discord.app_commands.describe(
        query="Từ khóa tìm kiếm (vd: AI, Python, cybersecurity)",
        count="Số bài muốn xem (1-5, mặc định 5)"
    )
    async def technews(
        self,
        interaction: discord.Interaction,
        query: str = None,
        count: int = 5
    ):
        await interaction.response.defer()
        try:
            count = max(1, min(count, 5))  # giới hạn 1-5
            articles = await get_tech_news(query, count)

            if not articles:
                await interaction.followup.send("Không tìm thấy tin tức.")
                return

            title = f"📰 Tin tức IT — '{query}'" if query else "📰 Tin tức công nghệ hôm nay"
            embed = discord.Embed(
                title=title,
                color=discord.Color.blurple(),
                timestamp=datetime.utcnow()
            )

            for i, article in enumerate(articles, 1):
                a = parse_article(article)
                embed.add_field(
                    name=f"{i}. {a['title'][:80]}{'...' if len(a['title']) > 80 else ''}",
                    value=(
                        f"📌 **{a['source']}** · {a['published']}\n"
                        f"{a['description'][:100]}...\n"
                        f"[🔗 Đọc thêm]({a['url']})"
                    ),
                    inline=False
                )

            # Ảnh bài đầu tiên làm thumbnail
            first = parse_article(articles[0])
            if first["image"]:
                embed.set_thumbnail(url=first["image"])

            embed.set_footer(text="Nguồn: NewsAPI")
            await interaction.followup.send(embed=embed)

        except ValueError as e:
            await interaction.followup.send(f"{e}")
        except Exception as e:
            await interaction.followup.send(f"Lỗi: {e}")

    #  /ainews
    @discord.app_commands.command(
        name="ainews",
        description="Tin tức AI & Machine Learning mới nhất"
    )
    async def ainews(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            articles = await get_tech_news("artificial intelligence OR machine learning", 5)

            embed = discord.Embed(
                title="🤖 Tin tức AI & Machine Learning",
                color=discord.Color.purple(),
                timestamp=datetime.utcnow()
            )

            for i, article in enumerate(articles, 1):
                a = parse_article(article)
                embed.add_field(
                    name=f"{i}. {a['title'][:80]}{'...' if len(a['title']) > 80 else ''}",
                    value=(
                        f"📌 **{a['source']}** · {a['published']}\n"
                        f"[🔗 Đọc thêm]({a['url']})"
                    ),
                    inline=False
                )

            first = parse_article(articles[0])
            if first["image"]:
                embed.set_thumbnail(url=first["image"])

            embed.set_footer(text="Nguồn: NewsAPI")
            await interaction.followup.send(embed=embed)

        except ValueError as e:
            await interaction.followup.send(f"{e}")
        except Exception as e:
            await interaction.followup.send(f"Lỗi: {e}")

    #  /cybernews 
    @discord.app_commands.command(
        name="cybernews",
        description="Tin tức bảo mật & network mới nhất"
    )
    async def cybernews(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            articles = await get_tech_news("cybersecurity OR network security OR hacking", 5)

            embed = discord.Embed(
                title="🔐 Tin tức Bảo mật & Network",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )

            for i, article in enumerate(articles, 1):
                a = parse_article(article)
                embed.add_field(
                    name=f"{i}. {a['title'][:80]}{'...' if len(a['title']) > 80 else ''}",
                    value=(
                        f"📌 **{a['source']}** · {a['published']}\n"
                        f"[🔗 Đọc thêm]({a['url']})"
                    ),
                    inline=False
                )

            first = parse_article(articles[0])
            if first["image"]:
                embed.set_thumbnail(url=first["image"])

            embed.set_footer(text="Nguồn: NewsAPI")
            await interaction.followup.send(embed=embed)

        except ValueError as e:
            await interaction.followup.send(f"{e}")
        except Exception as e:
            await interaction.followup.send(f"Lỗi: {e}")


async def setup(bot):
    await bot.add_cog(NewsCog(bot))