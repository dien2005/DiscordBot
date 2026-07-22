from db.connection import get_connection


async def test_connection() -> str:
    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "SELECT banner FROM v$version WHERE rownum = 1"
            )
            row = await cursor.fetchone()
            return row[0] if row else "Unknown"


async def fetch_all(sql: str, params: dict = {}) -> list[dict]:
    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql, params)
            columns = [col[0].lower() for col in cursor.description]
            rows = await cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]


# EXCHANGE 

async def save_exchange(base_cur: str, target_cur: str, rate: float):
    sql = """
        INSERT INTO exchange_history (base_cur, target_cur, rate)
        VALUES (:base_cur, :target_cur, :rate)
    """
    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql, {
                "base_cur": base_cur.upper(),
                "target_cur": target_cur.upper(),
                "rate": rate
            })
        await conn.commit()


async def get_exchange_history(base_cur: str, target_cur: str, days: int = 7) -> list[dict]:
    """Lấy lịch sử tỷ giá N ngày gần nhất."""
    sql = """
        SELECT
            TO_CHAR(recorded_at, 'DD/MM HH24:MI') AS thoi_gian,
            rate
        FROM exchange_history
        WHERE base_cur   = :base
          AND target_cur = :target
          AND recorded_at >= SYSTIMESTAMP - :days
        ORDER BY recorded_at
    """
    return await fetch_all(sql, {
        "base": base_cur.upper(),
        "target": target_cur.upper(),
        "days": days
    })


async def get_exchange_stats(base_cur: str, target_cur: str, days: int = 7) -> dict:
    """Thống kê tỷ giá: min, max, avg."""
    sql = """
        SELECT
            MIN(rate)  AS min_rate,
            MAX(rate)  AS max_rate,
            AVG(rate)  AS avg_rate,
            COUNT(*)   AS total
        FROM exchange_history
        WHERE base_cur   = :base
          AND target_cur = :target
          AND recorded_at >= SYSTIMESTAMP - :days
    """
    rows = await fetch_all(sql, {
        "base": base_cur.upper(),
        "target": target_cur.upper(),
        "days": days
    })
    return rows[0] if rows else {}


# WEATHER 

async def save_weather(city: str, temp: float, humidity: float, description: str):
    sql = """
        INSERT INTO weather_history (city, temperature, humidity, description)
        VALUES (:city, :temp, :humidity, :description)
    """
    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql, {
                "city": city,
                "temp": temp,
                "humidity": humidity,
                "description": description
            })
        await conn.commit()


async def get_weather_history(city: str, days: int = 7) -> list[dict]:
    """Lấy lịch sử thời tiết N ngày gần nhất."""
    sql = """
        SELECT
            TO_CHAR(recorded_at, 'DD/MM HH24:MI') AS thoi_gian,
            temperature,
            humidity,
            description
        FROM weather_history
        WHERE LOWER(city) = LOWER(:city)
          AND recorded_at >= SYSTIMESTAMP - :days
        ORDER BY recorded_at
    """
    return await fetch_all(sql, {"city": city, "days": days})


async def get_weather_stats(city: str, days: int = 7) -> dict:
    """Thống kê thời tiết: min, max, avg nhiệt độ."""
    sql = """
        SELECT
            MIN(temperature) AS min_temp,
            MAX(temperature) AS max_temp,
            AVG(temperature) AS avg_temp,
            AVG(humidity)    AS avg_humidity,
            COUNT(*)         AS total
        FROM weather_history
        WHERE LOWER(city) = LOWER(:city)
          AND recorded_at >= SYSTIMESTAMP - :days
    """
    rows = await fetch_all(sql, {"city": city, "days": days})
    return rows[0] if rows else {}