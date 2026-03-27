import os
import requests


def map_weather_to_status(weather_info):
    weather = weather_info.get('main')
    is_night = weather_info.get('is_night', False)

    base_mapping = {
        'Clear': {'day_emoji': '☀️', 'day_text': 'Sunny', 'night_emoji': '🌙', 'night_text': 'Clear night'},
        'Clouds': {'day_emoji': '⛅', 'day_text': 'Cloudy', 'night_emoji': '☁️', 'night_text': 'Cloudy night'},
        'Rain': {'day_emoji': '🌧️', 'day_text': 'Raining', 'night_emoji': '🌧️', 'night_text': 'Raining at night'},
        'Drizzle': {'day_emoji': '🌦️', 'day_text': 'Drizzle', 'night_emoji': '🌦️', 'night_text': 'Drizzle at night'},
        'Thunderstorm': {'day_emoji': '⛈️', 'day_text': 'Thunderstorms', 'night_emoji': '🌩️', 'night_text': 'Thunderstorms at night'},
        'Snow': {'day_emoji': '🌨️', 'day_text': 'Snowing', 'night_emoji': '❄️', 'night_text': 'Snowing at night'},
        'Mist': {'day_emoji': '🌫️', 'day_text': 'Misty', 'night_emoji': '🌫️', 'night_text': 'Misty night'}
    }

    city = weather_info.get('city', 'Copenhagen')
    record = base_mapping.get(weather)
    if record:
        if is_night:
            return {'emoji': record['night_emoji'], 'message': f"{record['night_text']} in {city}"}
        else:
            return {'emoji': record['day_emoji'], 'message': f"{record['day_text']} in {city}"}

    if is_night:
        return {'emoji': '🌙', 'message': f'{weather} at night in {city}'}
    return {'emoji': '🌤️', 'message': f'{weather} in {city}'}


def update_github_status(weather):
    token = os.getenv('GH_TOKEN')
    if not token:
        raise ValueError('GH_TOKEN must be set in .env with user status scope')

    status = map_weather_to_status(weather)
    payload = {
        'emoji': status['emoji'],
        'message': status['message'],
        'limited_availability': False
    }
    url = 'https://api.github.com/user/status'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github+json'
    }
    r = requests.patch(url, json=payload, headers=headers)
    r.raise_for_status()
    return r.json()