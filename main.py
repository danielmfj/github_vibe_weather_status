import os
from dotenv import load_dotenv

from weather_api import get_weather
from github_api import update_github_status

load_dotenv()


if __name__ == '__main__':
    try:
        weather_info = get_weather()
        response = update_github_status(weather_info)
        print(f"GitHub status updated: {response}")
    except Exception as e:
        print('Error:', e)
