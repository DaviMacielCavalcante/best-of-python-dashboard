import pytest
from unittest.mock import MagicMock, patch
from src.cache.manager import get_or_set_value_from_cache, get_last_update


class TestGetOrSetValueFromCache:
    """Tests for the get_or_set_value_from_cache() function."""

    def test_calls_func_and_returns_value_on_cache_miss(self):
        """On a cache miss, should call func() and return its result."""
        mock_cache = MagicMock()
        mock_cache.get.return_value = None
        func = MagicMock(return_value={"projects": []})

        with patch("src.cache.manager.start_cache", return_value=mock_cache):
            result = get_or_set_value_from_cache("projects", func)

        func.assert_called_once()
        assert result == {"projects": []}

    def test_returns_cached_value_on_cache_hit(self):
        """On a cache hit, should return the cached value without calling func()."""
        cached_value = {"projects": [{"name": "numpy"}]}
        mock_cache = MagicMock()
        mock_cache.get.return_value = cached_value
        func = MagicMock()

        with patch("src.cache.manager.start_cache", return_value=mock_cache):
            result = get_or_set_value_from_cache("projects", func)

        func.assert_not_called()
        assert result == cached_value

    def test_stores_value_with_24h_ttl_on_cache_miss(self):
        """On a cache miss, should store the computed value with a 24-hour TTL."""
        mock_cache = MagicMock()
        mock_cache.get.return_value = None
        value = {"projects": []}
        func = MagicMock(return_value=value)

        with patch("src.cache.manager.start_cache", return_value=mock_cache):
            get_or_set_value_from_cache("projects", func)

        mock_cache.set.assert_any_call(key="projects", value=value, expire=24 * 3600)

    def test_stores_last_update_timestamp_on_cache_miss(self):
        """On a cache miss, should store a YYYY-MM-DD timestamp under '{key}_last_update'."""
        mock_cache = MagicMock()
        mock_cache.get.return_value = None
        func = MagicMock(return_value={})

        with patch("src.cache.manager.start_cache", return_value=mock_cache):
            get_or_set_value_from_cache("projects", func)

        calls = [str(c) for c in mock_cache.set.call_args_list]
        assert any("projects_last_update" in c for c in calls)

    def test_last_update_value_matches_date_format(self):
        """The stored last_update value should be a YYYY-MM-DD formatted string."""
        import re

        mock_cache = MagicMock()
        mock_cache.get.return_value = None
        func = MagicMock(return_value={})
        captured = {}

        def capture_set(key, value, **kwargs):
            captured[key] = value

        mock_cache.set.side_effect = capture_set

        with patch("src.cache.manager.start_cache", return_value=mock_cache):
            get_or_set_value_from_cache("projects", func)

        date_value = captured.get("projects_last_update", "")
        assert re.match(r"^\d{4}-\d{2}-\d{2}$", date_value), f"Unexpected date format: {date_value}"


class TestGetLastUpdate:
    """Tests for the get_last_update() function."""

    def test_returns_none_when_key_has_never_been_cached(self):
        """get_last_update() should return None when the cache has no entry."""
        mock_cache = MagicMock()
        mock_cache.get.return_value = None

        with patch("src.cache.manager.start_cache", return_value=mock_cache):
            result = get_last_update("projects")

        assert result is None

    def test_returns_date_string_when_entry_exists(self):
        """get_last_update() should return the stored date string."""
        mock_cache = MagicMock()
        mock_cache.get.return_value = "2024-01-15"

        with patch("src.cache.manager.start_cache", return_value=mock_cache):
            result = get_last_update("projects")

        assert result == "2024-01-15"

    def test_queries_correct_suffixed_key(self):
        """get_last_update() should look up '{key}_last_update' in the cache."""
        mock_cache = MagicMock()
        mock_cache.get.return_value = None

        with patch("src.cache.manager.start_cache", return_value=mock_cache):
            get_last_update("projects")

        mock_cache.get.assert_called_with("projects_last_update")
