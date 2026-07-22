import time
from typing import Any, Optional


class TTLCache:
    """Simple in-memory cache with Time-To-Live (TTL)."""

    def __init__(self, default_ttl: int = 600):
        self._store: dict[str, tuple[Any, float]] = {}
        self._default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        """Lấy value từ cache. Trả về None nếu hết hạn hoặc không tồn tại."""
        if key not in self._store:
            return None
        value, expires_at = self._store[key]
        if time.time() > expires_at:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Lưu value vào cache với TTL (giây)."""
        ttl = ttl or self._default_ttl
        self._store[key] = (value, time.time() + ttl)

    def clear(self) -> None:
        """Xóa toàn bộ cache."""
        self._store.clear()

    def cleanup(self) -> int:
        """Xóa các entry hết hạn. Trả về số entry đã xóa."""
        now = time.time()
        expired = [k for k, (_, exp) in self._store.items() if now > exp]
        for k in expired:
            del self._store[k]
        return len(expired)


# Singleton instances
weather_cache = TTLCache(default_ttl=600)    # 10 phút
exchange_cache = TTLCache(default_ttl=1800)  # 30 phút
