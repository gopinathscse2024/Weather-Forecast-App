import streamlit as st
import requests
import pandas as pd
from datetime import datetime

GEO_IP_API = "https://ipapi.co/json/"
GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_API = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    80: "Rain showers",
    81: "Moderate showers",
    82: "Violent showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

def code_to_text(code):
    return WEATHER_CODES.get(code, f"Weather code {code}")

def get_location_by_ip():
    r = requests.get(GEO_IP_API, timeout=10)
    r.raise_for_status()
    data = r.json()
    return {
        "city": data.get("city", "Unknown"),
        "region": data.get("region", ""),
        "country": data.get("country_name", ""),
        "latitude": float(data["latitude"]),
        "longitude": float(data["longitude"]),
        "display": f'{data.get("city", "Unknown")}, {data.get("region", "")}, {data.get("country_name", "")}'.strip(", "),
    }

def search_city(city_name):
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
    r = requests.get(GEOCODING_API, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    results = data.get("results", [])
    if not results:
        return None
    place = results[0]
    return {
        "city": place.get("name", city_name),
        "country": place.get("country", ""),
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "timezone": place.get("timezone", "auto"),
        "display": f'{place.get("name", city_name)}, {place.get("admin1", "")}, {place.get("country", "")}'.strip(", "),
    }

def fetch_weather(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
        "forecast_days": 7,
    }
    r = requests.get(WEATHER_API, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

st.set_page_config(page_title="Weather Forecast App", page_icon="🌦️", layout="centered")

st.title("Weather Forecast App")
st.write("Get real-time weather with automatic location detection or city search.")

col1, col2 = st.columns(2)
with col1:
    use_location = st.button("Use My Location")
with col2:
    city = st.text_input("Search city", placeholder="Enter city name")

place = None

if use_location:
    try:
        place = get_location_by_ip()
    except Exception as e:
        st.error(f"Could not detect location: {e}")

if st.button("Search Weather"):
    if city.strip():
        try:
            place = search_city(city.strip())
            if not place:
                st.error("City not found.")
        except Exception as e:
            st.error(f"Search failed: {e}")
    else:
        st.warning("Please enter a city name.")

if place:
    try:
        data = fetch_weather(place["latitude"], place["longitude"])
        current = data["current"]
        daily = data["daily"]

        st.subheader(place["display"])
        st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        st.metric("Temperature", f'{current["temperature_2m"]} °C')
        st.write(f'**Condition:** {code_to_text(current["weather_code"])}')
        st.write(f'**Humidity:** {current["relative_humidity_2m"]}%')
        st.write(f'**Wind:** {current["wind_speed_10m"]} km/h')

        forecast_df = pd.DataFrame({
            "Date": daily["time"],
            "Weather": [code_to_text(c) for c in daily["weather_code"]],
            "Max Temp (°C)": daily["temperature_2m_max"],
            "Min Temp (°C)": daily["temperature_2m_min"],
        })

        st.subheader("7-Day Forecast")
        st.dataframe(forecast_df, use_container_width=True)

        st.line_chart(
            forecast_df.set_index("Date")[["Max Temp (°C)", "Min Temp (°C)"]]
        )
    except Exception as e:
        st.error(f"Failed to load weather data: {e}")