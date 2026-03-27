import os
import requests


def get_weather():
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY not set in .env file")

    city = os.getenv('CITY', 'Copenhagen').strip()
    if not city:
        raise ValueError("CITY must be set in .env file or environment variables")

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    weather_main = data['weather'][0]['main']
    now = data.get('dt')
    sunrise = data.get('sys', {}).get('sunrise')
    sunset = data.get('sys', {}).get('sunset')
    is_night = False
    if now and sunrise and sunset:
        is_night = now < sunrise or now > sunset

    return {'main': weather_main, 'is_night': is_night, 'city': city}