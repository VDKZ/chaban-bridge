# Built-in
from typing import Any, Dict

# Third-party
import requests

BORDEAUX_LATITUDE = "44.83"
BORDEAUX_LONGITUDE = "-0.57"

WEATHER_URL = "https://api.open-meteo.com/v1/"


def weather_api() -> Dict[str, Any]:
    params = "&current=temperature_2m,relative_humidity_2m,weather_code"
    url = f"{WEATHER_URL}forecast?latitude={BORDEAUX_LATITUDE}&longitude={BORDEAUX_LONGITUDE}"
    response = requests.get(url + params)

    if response.status_code != 200:
        print(f"Error status {response.status_code} during Weather api call")
        return {"status": f"error status {response.status_code}"}

    data = response.json()

    if "current" not in data:
        print("Error no data for current weather")
        return {"status": "Error no data fir current weather"}

    temperature = data["current"].get("temperature_2m", None)
    relative_humidity = data["current"].get("relative_humidity_2m", None)
    weather_code = data["current"].get("weather_code", None)

    result = {
        "temperature": temperature,
        "relative_humidity": relative_humidity,
        "weather_code": weather_code,
    }
    return result
