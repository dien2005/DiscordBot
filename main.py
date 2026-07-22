import discord
from discord.ext import commands
import asyncio
import config
from db.connection import init_pool, close_pool
from scheduler.tasks import setup_scheduler
from utils.logger import setup_logger

logger = setup_logger("bot.main")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

COGS = [
    "cogs.database",
    "cogs.weather",
    "cogs.exchange",
    "cogs.news",
]

@bot.event
async def on_ready():
    await init_pool()
    logger.info(f"Bot online: {bot.user}")

    setup_scheduler(bot)

    try:
        if config.GUILD_ID:
            guild = discord.Object(id=config.GUILD_ID)
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            logger.info(f"Synced {len(synced)} slash commands to guild {config.GUILD_ID}")
        else:
            synced = await bot.tree.sync()
            logger.info(f"Synced {len(synced)} slash commands globally")
    except Exception as e:
        logger.error(f"Sync error: {e}")

async def main():
    async with bot:
        for cog in COGS:
            try:
                await bot.load_extension(cog)
                logger.info(f"Loaded: {cog}")
            except Exception as e:
                logger.error(f"Failed to load {cog}: {e}")
        try:
            await bot.start(config.DISCORD_TOKEN)
        except discord.LoginFailure:
            logger.critical("Token không hợp lệ!")
        except Exception as e:
            logger.critical(f"Lỗi kết nối: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        asyncio.run(close_pool())
        logger.info("Bot stopped")