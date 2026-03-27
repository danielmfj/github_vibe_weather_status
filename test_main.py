import os
import pytest
from unittest.mock import Mock, patch

from weather_api import get_weather
from github_api import map_weather_to_status

SAMPLE_WEATHER_RESPONSE = {
    'weather': [{'main': 'Clear'}],
    'dt': 1700000000,
    'sys': {'sunrise': 1699990000, 'sunset': 1700010000},
}


@patch('weather_api.requests.get')
def test_get_weather_uses_city_env(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = SAMPLE_WEATHER_RESPONSE
    mock_get.return_value = mock_response

    os.environ['OPENWEATHER_API_KEY'] = 'dummy'
    os.environ['CITY'] = 'Berlin'

    result = get_weather()

    assert result['main'] == 'Clear'
    assert result['is_night'] is False
    assert result['city'] == 'Berlin'
    mock_get.assert_called_once()
    assert 'q=Berlin' in mock_get.call_args[0][0]


@patch('weather_api.requests.get')
def test_get_weather_defaults_to_copenhagen(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = SAMPLE_WEATHER_RESPONSE
    mock_get.return_value = mock_response

    os.environ['OPENWEATHER_API_KEY'] = 'dummy'
    os.environ.pop('CITY', None)

    result = get_weather()

    assert result['city'] == 'Copenhagen'


@patch('weather_api.requests.get')
def test_get_weather_raises_when_no_api_key(mock_get):
    os.environ.pop('OPENWEATHER_API_KEY', None)
    with pytest.raises(ValueError, match='OPENWEATHER_API_KEY not set'):
        get_weather()


def test_map_weather_to_status_night():
    payload = {'main': 'Snow', 'is_night': True, 'city': 'Rome'}
    output = map_weather_to_status(payload)
    assert output['emoji'] == '❄️'
    assert 'Rome' in output['message']


def test_map_weather_to_status_unknown_weather():
    payload = {'main': 'Ash', 'is_night': False, 'city': 'Paris'}
    output = map_weather_to_status(payload)
    assert output['emoji'] == '🌤️'
    assert 'Paris' in output['message']
