import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_weather():
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY not set in .env file")
    city = 'Copenhagen'
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

    return {'main': weather_main, 'is_night': is_night}


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

    record = base_mapping.get(weather)
    if record:
        if is_night:
            return {'emoji': record['night_emoji'], 'message': f"{record['night_text']} in Copenhagen"}
        else:
            return {'emoji': record['day_emoji'], 'message': f"{record['day_text']} in Copenhagen"}

    if is_night:
        return {'emoji': '🌙', 'message': f'{weather} at night in Copenhagen'}
    return {'emoji': '🌤️', 'message': f'{weather} in Copenhagen'}


def update_github_status(weather):
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError('GITHUB_TOKEN must be set in .env with user status scope')

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


if __name__ == '__main__':
    try:
        weather_info = get_weather()
        response = update_github_status(weather_info)
        print(f"GitHub status updated: {response}")
    except Exception as e:
        print('Error:', e)
