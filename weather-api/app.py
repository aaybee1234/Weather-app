from flask import Flask, request, jsonify
import requests
import os


app = Flask(__name__)
ACCU_API_KEY = os.getenv("ACCU_API_KEY")  # loaded from Docker env


def get_location_key(city):
    """Get AccuWeather location key for a given city."""
    url = "http://dataservice.accuweather.com/locations/v1/cities/search"
    params = {"apikey": ACCU_API_KEY, "q": city}
    res = requests.get(url, params=params).json()

    if not isinstance(res, list) or len(res) == 0:
        return None  # city not found or invalid key

    return res[0]["Key"], res[0]["LocalizedName"]


@app.route("/weather", methods=["GET"])
def get_weather():
    """Return current or 5-day forecast weather data for a city."""
    city = request.args.get("city")
    forecast_type = request.args.get("type", "current")

    loc = get_location_key(city)
    if not loc:
        return jsonify({"error": "City not found or invalid API key"}), 404

    location_key, city_name = loc

    if forecast_type == "current":
        url = (
            f"http://dataservice.accuweather.com/currentconditions/v1/"
            f"{location_key}"
        )
        params = {"apikey": ACCU_API_KEY, "details": "true"}
        data = requests.get(url, params=params).json()[0]

        result = {
            "city": city_name,
            "description": data["WeatherText"],
            "temperature": data["Temperature"]["Metric"]["Value"],
            "unit": data["Temperature"]["Metric"]["Unit"],
            "humidity": data["RelativeHumidity"],
            "windspeed": data["Wind"]["Speed"]["Metric"]["Value"],
            "uv_index": data["UVIndexText"],
        }
        return jsonify(result)

    if forecast_type == "daily":
        url = (
            f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/"
            f"{location_key}"
        )
        params = {"apikey": ACCU_API_KEY, "metric": "true"}
        data = requests.get(url, params=params).json()
        return jsonify(data)

    return jsonify({"error": "Invalid forecast type"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
