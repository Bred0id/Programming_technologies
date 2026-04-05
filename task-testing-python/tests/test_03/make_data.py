import json
import os
import requests

BASE_URL = "http://dataservice.accuweather.com/currentconditions/v1/"
FORECAST_URL = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/"
LOCATION_URL = "http://dataservice.accuweather.com/locations/v1/cities/search"
API_KEY = "test_key"
BASE_DIR = "testing_data"
os.makedirs(BASE_DIR, exist_ok=True)

def save(name, data):
    with open(f"{BASE_DIR}/{name}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

def get(city, url):
    return requests.get(
        url,
        params={
            "q": city,
            "apikey": API_KEY,
            "metric": True,
            "language": "en-us",
        },
    )

def get_response_city(city, url):
    response = get(city, url)
    return response.json()

def get_location_key(city):
    response = get_response_city(city, LOCATION_URL)
    return response[0]["Key"]

def main():
    for city in ["Moscow", "London"]:
        location = get_response_city(city, LOCATION_URL)
        save(f"location_{city.lower()}", location)

        if len(location) < 1:
            continue

        location_key = get_location_key(city)
        current = get_response_city(city, BASE_URL + location_key)
        save(f"current_{city.lower()}", current)

        forecast = get_response_city(city, FORECAST_URL + location_key)
        save(f"primary_{city.lower()}", forecast)


if __name__ == "__main__":
    main()