"""Local environment configuration; no credentials are bundled with the source."""

import os


def get_weather_api_key():
    """Return the caller's OpenWeatherMap key or stop before making a request."""
    api_key = os.environ.get("OPENWEATHERMAP_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "Set OPENWEATHERMAP_API_KEY in your local environment before "
            "using weather or location-time features. Never commit its value."
        )
    return api_key
