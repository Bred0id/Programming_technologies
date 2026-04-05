import json
import pytest
from pathlib import Path

from weather_03.weather_wrapper import BASE_URL, FORECAST_URL, LOCATION_URL, WeatherWrapper

testing_data = Path(__file__).parent / "testing_data"

def load_data(filename):
    with open(testing_data / filename, "r", encoding="utf-8") as file:
        return json.load(file)

def test_get_location_key(requests_mock):
    weather = WeatherWrapper("test_key")
    requests_mock.get(
        LOCATION_URL,
        json=load_data("location_moscow.json"),
        status_code=200,
    )

    assert weather.get_location_key("Moscow") == "294021"

def test_get_location_key_not_found(requests_mock):
    weather = WeatherWrapper("test_key")
    requests_mock.get(
        LOCATION_URL,
        json=load_data("location_not_found.json"),
        status_code=200,
    )

    with pytest.raises(ValueError) as exc_info:
        weather.get_location_key("Moscow")

    assert str(exc_info.value) == "City Moscow not found"

def test_get_temperature(requests_mock):
    weather = WeatherWrapper("test_key")
    requests_mock.get(
        LOCATION_URL,
        json=load_data("location_moscow.json"),
        status_code=200,
    )
    requests_mock.get(
        BASE_URL + "294021",
        json=load_data("current_moscow.json"),
        status_code=200,
    )

    assert weather.get_temperature("Moscow") == 10.0

def test_get_tomorrow_temperature(requests_mock):
    weather = WeatherWrapper("test_key")
    requests_mock.get(
        LOCATION_URL,
        json=load_data("location_moscow.json"),
        status_code=200,
    )
    requests_mock.get(
        FORECAST_URL + "294021",
        json=load_data("tomorrow_moscow_warmer.json"),
        status_code=200,
    )

    assert weather.get_tomorrow_temperature("Moscow") == 11.3

def test_find_diff_two_cities(requests_mock):
    weather = WeatherWrapper("test_key")
    requests_mock.get(
        LOCATION_URL,
        [
            {"json": load_data("location_moscow.json"), "status_code": 200},
            {"json": load_data("location_london.json"), "status_code": 200},
        ],
    )
    requests_mock.get(
        BASE_URL + "294021",
        json=load_data("current_moscow.json"),
        status_code=200,
    )
    requests_mock.get(
        BASE_URL + "328328",
        json=load_data("current_london.json"),
        status_code=200,
    )

    assert weather.find_diff_two_cities("Moscow", "London") == -5.0

def test_get_diff_string(requests_mock):
    weather = WeatherWrapper("test_key")
    requests_mock.get(
        LOCATION_URL,
        [
            {"json": load_data("location_moscow.json"), "status_code": 200},
            {"json": load_data("location_london.json"), "status_code": 200},
        ],
    )
    requests_mock.get(
        BASE_URL + "294021",
        json=load_data("current_moscow.json"),
        status_code=200,
    )
    requests_mock.get(
        BASE_URL + "328328",
        json=load_data("current_london.json"),
        status_code=200,
    )

    assert weather.get_diff_string("Moscow", "London") == "Weather in Moscow is colder than in London by 5 degrees"

@pytest.mark.parametrize(
    ("tomorrow", "expected"),
    [
        ("tomorrow_moscow_much_warmer.json", "much warmer"),
        ("tomorrow_moscow_warmer.json", "warmer"),
        ("tomorrow_moscow_same.json", "the same"),
        ("tomorrow_moscow_colder.json", "colder"),
        ("tomorrow_moscow_much_colder.json", "much colder"),
    ],
)
def test_get_tomorrow_diff(requests_mock, tomorrow, expected):
    weather = WeatherWrapper("test_key")
    requests_mock.get(
        LOCATION_URL,
        [
            {"json": load_data("location_moscow.json"), "status_code": 200},
            {"json": load_data("location_moscow.json"), "status_code": 200},
        ],
    )
    requests_mock.get(
        BASE_URL + "294021",
        json=load_data("current_moscow.json"),
        status_code=200,
    )
    requests_mock.get(
        FORECAST_URL + "294021",
        json=load_data(tomorrow),
        status_code=200,
    )

    assert weather.get_tomorrow_diff("Moscow") == f"The weather in Moscow tomorrow will be {expected} than today"