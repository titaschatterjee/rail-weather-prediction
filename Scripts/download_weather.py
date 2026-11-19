"""Download daily historical weather for UK rail hub cities from Open-Meteo."""
import time
from pathlib import Path

import pandas as pd
import requests

API_URL = "https://archive-api.open-meteo.com/v1/archive"
START_DATE = "2023-01-01"
END_DATE = "2025-12-31"
DAILY_VARS = [
    "temperature_2m_max", "temperature_2m_min", "precipitation_sum",
    "rain_sum", "snowfall_sum", "wind_speed_10m_max", "wind_gusts_10m_max",
]
CITIES = {
    "London": (51.5074, -0.1278), "Birmingham": (52.4862, -1.8904),
    "Manchester": (53.4808, -2.2426), "Leeds": (53.8008, -1.5491),
    "Bristol": (51.4545, -2.5879), "York": (53.9600, -1.0873),
    "Edinburgh": (55.9533, -3.1883), "Glasgow": (55.8642, -4.2518),
}
OUT_FILE = Path("data/raw/weather_daily.csv")


def fetch_city(name, lat, lon):
    params = {
        "latitude": lat, "longitude": lon,
        "start_date": START_DATE, "end_date": END_DATE,
        "daily": ",".join(DAILY_VARS), "timezone": "Europe/London",
    }
    resp = requests.get(API_URL, params=params, timeout=60)
    resp.raise_for_status()
    df = pd.DataFrame(resp.json()["daily"])
    df.insert(0, "city", name)
    return df


def main():
    frames = []
    for name, (lat, lon) in CITIES.items():
        print(f"Downloading {name}...")
        frames.append(fetch_city(name, lat, lon))
        time.sleep(1)  # be polite to the free API
    result = pd.concat(frames, ignore_index=True)
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUT_FILE, index=False)
    print(f"Saved {len(result):,} rows to {OUT_FILE}")


if __name__ == "__main__":
    main()