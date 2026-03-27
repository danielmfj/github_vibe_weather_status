import os
import requests


def map_weather_to_status(weather_info):
    weather = weather_info.get('main')
    is_night = weather_info.get('is_night', False)

    base_mapping = {
        'Clear': {'day_emoji': '☀️', 'day_text': 'sunny day', 'night_emoji': '🌙', 'night_text': 'clear night'},
        'Clouds': {'day_emoji': '⛅', 'day_text': 'cloudy day', 'night_emoji': '☁️', 'night_text': 'cloudy night'},
        'Rain': {'day_emoji': '🌧️', 'day_text': 'rainy day', 'night_emoji': '🌧️', 'night_text': 'rainy night'},
        'Drizzle': {'day_emoji': '🌦️', 'day_text': 'drizzly day', 'night_emoji': '🌦️', 'night_text': 'drizzly night'},
        'Thunderstorm': {'day_emoji': '⛈️', 'day_text': 'thunderstorm day', 'night_emoji': '🌩️', 'night_text': 'thunderstorm night'},
        'Snow': {'day_emoji': '🌨️', 'day_text': 'snowy day', 'night_emoji': '❄️', 'night_text': 'snowy night'},
        'Mist': {'day_emoji': '🌫️', 'day_text': 'misty day', 'night_emoji': '🌫️', 'night_text': 'misty night'}
    }

    city = weather_info.get('city', 'Copenhagen')
    record = base_mapping.get(weather)
    if record:
        if is_night:
            return {'emoji': record['night_emoji'], 'message': f"Living in a {record['night_text']} in {city}"}
        else:
            return {'emoji': record['day_emoji'], 'message': f"Living in a {record['day_text']} in {city}"}

    if is_night:
        return {'emoji': '🌙', 'message': f'Living in a {weather} at night in {city}'}
    return {'emoji': '🌤️', 'message': f'Living in a {weather} in {city}'}


def update_github_status_graphql(weather):
    """Update GitHub status using GraphQL API"""
    token = os.getenv('GH_TOKEN')
    if not token:
        raise ValueError('GH_TOKEN must be set in .env')

    status = map_weather_to_status(weather)
    
    query = '''
    mutation {
      changeUserStatus(input: {emoji: "%s", message: "%s"}) {
        clientMutationId
      }
    }
    ''' % (status['emoji'], status['message'].replace('"', '\\"'))
    
    url = 'https://api.github.com/graphql'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'query': query
    }
    
    r = requests.post(url, json=payload, headers=headers)
    response_data = r.json()
    
    # Check for GraphQL errors
    if 'errors' in response_data:
        error_msg = response_data['errors'][0]['message'] if response_data['errors'] else 'Unknown GraphQL error'
        raise ValueError(f'GitHub GraphQL error: {error_msg}')
    
    r.raise_for_status()
    return response_data


def update_github_status(weather):
    """Alias for GraphQL update (main entry point)"""
    return update_github_status_graphql(weather)