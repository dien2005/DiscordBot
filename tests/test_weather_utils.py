import pytest
from utils.weather import parse_weather, weather_emoji


class TestParseWeather:
    """Test parse_weather function."""

    def test_parse_weather_basic(self):
        data = {
            "name": "Hanoi",
            "sys": {"country": "VN"},
            "main": {
                "temp": 32.5,
                "feels_like": 35.1,
                "temp_min": 30.0,
                "temp_max": 34.0,
                "humidity": 70,
            },
            "weather": [{"description": "mây rải rác", "icon": "03d"}],
            "wind": {"speed": 3.5},
            "visibility": 10000,
        }
        result = parse_weather(data)

        assert result["city"] == "Hanoi"
        assert result["country"] == "VN"
        assert result["temp"] == 32  # round(32.5) = 32 (banker's rounding)
        assert result["feels_like"] == 35
        assert result["humidity"] == 70
        assert result["wind_speed"] == 3.5
        assert result["visibility"] == 10  # 10000m -> 10km
        assert result["icon"] == "03d"

    def test_parse_weather_no_visibility(self):
        data = {
            "name": "Test",
            "sys": {"country": "US"},
            "main": {
                "temp": 20, "feels_like": 18,
                "temp_min": 15, "temp_max": 22,
                "humidity": 50,
            },
            "weather": [{"description": "clear sky", "icon": "01d"}],
            "wind": {"speed": 1.0},
        }
        result = parse_weather(data)
        assert result["visibility"] == 0

    def test_parse_weather_description_capitalized(self):
        data = {
            "name": "Test",
            "sys": {"country": "US"},
            "main": {
                "temp": 20, "feels_like": 18,
                "temp_min": 15, "temp_max": 22,
                "humidity": 50,
            },
            "weather": [{"description": "light rain", "icon": "10d"}],
            "wind": {"speed": 2.0},
            "visibility": 5000,
        }
        result = parse_weather(data)
        assert result["description"] == "Light rain"


class TestWeatherEmoji:
    """Test weather_emoji function."""

    def test_clear_sky(self):
        assert weather_emoji("01d") == "☀️"
        assert weather_emoji("01n") == "☀️"

    def test_cloudy(self):
        assert weather_emoji("02d") == "⛅"
        assert weather_emoji("03d") == "☁️"
        assert weather_emoji("04d") == "☁️"

    def test_rain(self):
        assert weather_emoji("09d") == "🌧️"
        assert weather_emoji("10d") == "🌦️"

    def test_thunderstorm(self):
        assert weather_emoji("11d") == "⛈️"

    def test_snow(self):
        assert weather_emoji("13d") == "❄️"

    def test_fog(self):
        assert weather_emoji("50d") == "🌫️"

    def test_unknown_icon(self):
        assert weather_emoji("99x") == "🌡️"
