import pytest
from utils.news import parse_article


class TestParseArticle:
    """Test parse_article function."""

    def test_full_article(self):
        article = {
            "title": "AI Revolution in 2026",
            "source": {"name": "TechCrunch"},
            "url": "https://techcrunch.com/article",
            "description": "AI is transforming everything.",
            "publishedAt": "2026-07-21T10:00:00Z",
            "urlToImage": "https://example.com/image.jpg",
        }
        result = parse_article(article)

        assert result["title"] == "AI Revolution in 2026"
        assert result["source"] == "TechCrunch"
        assert result["url"] == "https://techcrunch.com/article"
        assert result["description"] == "AI is transforming everything."
        assert result["published"] == "2026-07-21"
        assert result["image"] == "https://example.com/image.jpg"

    def test_missing_fields(self):
        article = {}
        result = parse_article(article)

        assert result["title"] == "No title"
        assert result["source"] == "Unknown"
        assert result["url"] == ""
        assert result["description"] == "Không có mô tả."
        assert result["image"] == ""

    def test_none_description(self):
        article = {
            "title": "Test",
            "description": None,
            "source": {"name": "Test"},
            "url": "https://test.com",
            "publishedAt": "2026-01-01T00:00:00Z",
            "urlToImage": None,
        }
        result = parse_article(article)
        assert result["description"] == "Không có mô tả."

    def test_published_date_format(self):
        article = {
            "publishedAt": "2026-07-21T15:30:00Z",
        }
        result = parse_article(article)
        assert result["published"] == "2026-07-21"  # only date part
