import tkinter as tk
from tkinter import ttk, messagebox
import requests
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
    try:
        r = requests.get(GEO_IP_API, timeout=10)
        r.raise_for_status()
        data = r.json()
        return {
            "city": data.get("city") or "Unknown",
            "region": data.get("region") or "",
            "country": data.get("country_name") or "",
            "latitude": float(data["latitude"]),
            "longitude": float(data["longitude"]),
            "display": f'{data.get("city", "Unknown")}, {data.get("region", "")}, {data.get("country_name", "")}'.strip(", "),
        }
    except Exception:
        return None

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

def update_weather(place):
    try:
        data = fetch_weather(place["latitude"], place["longitude"])
        current = data["current"]
        daily = data["daily"]

        location_label.config(text=place["display"])
        time_label.config(text=f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        temp = current.get("temperature_2m", "--")
        humidity = current.get("relative_humidity_2m", "--")
        wind = current.get("wind_speed_10m", "--")
        code = current.get("weather_code", -1)

        current_weather_label.config(text=code_to_text(code))
        temperature_label.config(text=f"{temp} °C")
        details_label.config(
            text=f"Humidity: {humidity}%   |   Wind: {wind} km/h   |   {code_to_text(code)}"
        )

        forecast_text = ""
        dates = daily.get("time", [])
        codes = daily.get("weather_code", [])
        tmax = daily.get("temperature_2m_max", [])
        tmin = daily.get("temperature_2m_min", [])

        for i in range(min(7, len(dates))):
            day = datetime.strptime(dates[i], "%Y-%m-%d").strftime("%a, %d %b")
            forecast_text += (
                f"{day:<15}  {code_to_text(codes[i]):<28} "
                f"Max: {tmax[i]}°C  Min: {tmin[i]}°C\n"
            )

        forecast_box.config(state="normal")
        forecast_box.delete("1.0", tk.END)
        forecast_box.insert(tk.END, forecast_text)
        forecast_box.config(state="disabled")
    except Exception as e:
        messagebox.showerror("Weather App", f"Failed to load weather data:\n{e}")

def use_my_location():
    place = get_location_by_ip()
    if not place:
        messagebox.showerror("Weather App", "Could not detect your location automatically.")
        return
    update_weather(place)

def search_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Weather App", "Please enter a city name.")
        return
    try:
        place = search_city(city)
        if not place:
            messagebox.showerror("Weather App", "City not found.")
            return
        update_weather(place)
    except Exception as e:
        messagebox.showerror("Weather App", f"Search failed:\n{e}")

root = tk.Tk()
root.title("Weather Forecast App")
root.geometry("760x620")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#1f2937")
style.configure("TLabel", background="#1f2937", foreground="white", font=("Segoe UI", 11))
style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
style.configure("Big.TLabel", font=("Segoe UI", 28, "bold"))
style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"))

main = ttk.Frame(root, padding=20)
main.pack(fill="both", expand=True)

title = ttk.Label(main, text="Weather Forecast App", style="Title.TLabel")
title.pack(pady=(0, 10))

search_frame = ttk.Frame(main)
search_frame.pack(fill="x", pady=10)

city_entry = ttk.Entry(search_frame, font=("Segoe UI", 12))
city_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
city_entry.insert(0, "Enter city name")

search_btn = ttk.Button(search_frame, text="Search City", command=search_weather)
search_btn.pack(side="left", padx=(0, 10))

location_btn = ttk.Button(search_frame, text="Use My Location", command=use_my_location)
location_btn.pack(side="left")

location_label = ttk.Label(main, text="Location: --", font=("Segoe UI", 14, "bold"))
location_label.pack(pady=(20, 5))

time_label = ttk.Label(main, text="Updated: --")
time_label.pack(pady=(0, 10))

temperature_label = ttk.Label(main, text="-- °C", style="Big.TLabel")
temperature_label.pack(pady=5)

current_weather_label = ttk.Label(main, text="--", font=("Segoe UI", 16))
current_weather_label.pack(pady=5)

details_label = ttk.Label(main, text="Humidity: --   |   Wind: --   |   --")
details_label.pack(pady=(5, 20))

forecast_title = ttk.Label(main, text="7-Day Forecast", font=("Segoe UI", 14, "bold"))
forecast_title.pack(anchor="w", pady=(10, 5))

forecast_box = tk.Text(main, height=14, wrap="none", font=("Consolas", 10))
forecast_box.pack(fill="both", expand=True)
forecast_box.config(state="disabled")

footer = ttk.Label(main, text="Powered by Open-Meteo", font=("Segoe UI", 10))
footer.pack(pady=(10, 0))

root.bind("<Return>", lambda event: search_weather())
root.mainloop()