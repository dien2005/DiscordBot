import oracledb
import config
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger("bot.db")

_pool: Optional[oracledb.AsyncConnectionPool] = None

async def init_pool():
    global _pool
    _pool = oracledb.create_pool_async(
        user=config.DB_CONFIG["user"],
        password=config.DB_CONFIG["password"],
        dsn=config.DB_CONFIG["dsn"],
        min=2,
        max=10,
        increment=1,
    )
    logger.info("Oracle connection pool initialized")

async def close_pool():
    global _pool
    if _pool:
        await _pool.close()
        logger.info("Oracle connection pool closed")

async def get_connection():
    if _pool is None:
        raise RuntimeError("Pool chưa khởi tạo! Gọi init_pool() trước.")
    return await _pool.acquire()