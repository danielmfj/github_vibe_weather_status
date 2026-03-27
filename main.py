import os
import requests
from dotenv import load_dotenv

from weather_api import get_weather
from github_api import update_github_status

load_dotenv()

DEFAULT_STATUS = {
    'emoji': '👀',
    'message': 'Status temporarily unavailable'
}


def set_default_status():
    """Set a default status when API calls fail"""
    try:
        token = os.getenv('GH_TOKEN')
        if not token:
            raise ValueError('GH_TOKEN must be set in .env with user status scope')

        payload = {
            'emoji': DEFAULT_STATUS['emoji'],
            'message': DEFAULT_STATUS['message'],
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
    except Exception as e:
        print(f'Failed to set default status: {e}')
        return None


if __name__ == '__main__':
    try:
        weather_info = get_weather()
        response = update_github_status(weather_info)
        print(f"GitHub status updated: {response}")
    except Exception as e:
        print(f'Error fetching weather or updating status: {e}')
        print('Setting default status...')
        set_default_status()

