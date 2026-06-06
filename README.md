# Weather Forecast App

A Streamlit app for checking current weather and a 7-day forecast. It can detect your approximate location from your IP address or search for a city name.

## Features

- Detects location using `ipapi.co`
- Searches cities with the Open-Meteo Geocoding API
- Shows current temperature, condition, humidity, and wind speed
- Displays a 7-day forecast table
- Charts daily maximum and minimum temperatures

## Requirements

- Python 3.10 or newer
- Internet access for the weather and location APIs

Install the Python packages:

```powershell
pip install -r requirements.txt
```

## Run

Start the app from the project root:

```powershell
streamlit run app.py
```

If you are using the included virtual environment on Windows:

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

Then open the local URL printed by Streamlit, usually:

```text
http://localhost:8501
```

## Project Files

- `app.py` - main Streamlit weather app
- `weather_app.py` - alternate weather app implementation
- `requirements.txt` - Python dependencies
- `chat-app/` - separate chat app project

## Notes

Location detection is approximate because it is based on IP address. City search and forecast data require network access.
🌦️ Excited to share my Weather Forecast Application developed during my Python Development Internship at Pinnacle Labs.

Pinnacle Labs delivers innovative IT solutions in software development, cybersecurity, cloud computing, and data analytics, helping organizations leverage technology for business growth and digital transformation.

✨ Features:
• Real-time weather updates
• Automatic location detection
• Current temperature and weather conditions
• Humidity and wind speed information
• User-friendly interface

🛠️ Technologies Used:
Python, Weather API, HTML, CSS, JavaScript

This project enhanced my understanding of API integration, real-time data processing, and user interface development. It was a great opportunity to apply Python programming skills to a practical real-world application.

Thank you Pinnacle Labs for the valuable internship experience and continuous learning opportunities.

#Python #WeatherApp #API #Internship #Programming #SoftwareDevelopment #PinnacleLabs #TechInnovation

@Pinnacle Labs

