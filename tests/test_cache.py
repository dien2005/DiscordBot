import pytest
import time
from utils.cache import TTLCache


class TestTTLCache:
    """Test TTLCache implementation."""

    def test_set_and_get(self):
        cache = TTLCache(default_ttl=60)
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"

    def test_get_missing_key(self):
        cache = TTLCache(default_ttl=60)
        assert cache.get("nonexistent") is None

    def test_ttl_expiry(self):
        cache = TTLCache(default_ttl=1)  # 1 second TTL
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"

        time.sleep(1.1)  # wait for expiry
        assert cache.get("key1") is None

    def test_custom_ttl(self):
        cache = TTLCache(default_ttl=60)
        cache.set("key1", "value1", ttl=1)  # override TTL

        assert cache.get("key1") == "value1"
        time.sleep(1.1)
        assert cache.get("key1") is None

    def test_overwrite_value(self):
        cache = TTLCache(default_ttl=60)
        cache.set("key1", "old")
        cache.set("key1", "new")
        assert cache.get("key1") == "new"

    def test_clear(self):
        cache = TTLCache(default_ttl=60)
        cache.set("key1", "v1")
        cache.set("key2", "v2")
        cache.clear()
        assert cache.get("key1") is None
        assert cache.get("key2") is None

    def test_cleanup(self):
        cache = TTLCache(default_ttl=1)
        cache.set("expired1", "v1")
        cache.set("expired2", "v2")
        cache.set("valid", "v3", ttl=60)  # this one stays

        time.sleep(1.1)
        removed = cache.cleanup()
        assert removed == 2
        assert cache.get("valid") == "v3"

    def test_different_value_types(self):
        cache = TTLCache(default_ttl=60)
        cache.set("str", "hello")
        cache.set("int", 42)
        cache.set("dict", {"key": "value"})
        cache.set("list", [1, 2, 3])

        assert cache.get("str") == "hello"
        assert cache.get("int") == 42
        assert cache.get("dict") == {"key": "value"}
        assert cache.get("list") == [1, 2, 3]
