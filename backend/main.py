from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import pickle
import pandas as pd

from pathlib import Path


from services.chatbot import get_chat_response
from routes.smart_crop import router as smart_crop_router

from disease_predictor import predict_disease
from disease_knowledge import get_disease_knowledge
from routes.disease import router as disease_router



# =========================================================
# FastAPI App
# =========================================================

app = FastAPI(
    title="AgriSmart AI API",
    description="AI-powered agriculture assistant",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# Crop Recommendation Model
# =========================================================

with open("models/crop_model.pkl", "rb") as f:
    crop_model = pickle.load(f)


# =========================================================
# Smart Crop Router
# =========================================================

app.include_router(smart_crop_router)
app.include_router(disease_router)

# =========================================================
# Home
# =========================================================

@app.get("/")
def home():
    return {
        "message": "AgriSmart AI Backend Running"
    }


# =========================================================
# Chatbot
# =========================================================

@app.post("/chat")
def chat(data: dict):
    return get_chat_response(data)


# =========================================================
# Existing Crop Recommendation
# =========================================================

@app.post("/predict")
def predict(data: dict):

    features = pd.DataFrame([
        {
            "N": float(data["nitrogen"]),
            "P": float(data["phosphorus"]),
            "K": float(data["potassium"]),
            "temperature": float(data["temperature"]),
            "humidity": float(data["humidity"]),
            "ph": float(data["ph"]),
            "rainfall": float(data["rainfall"]),
        }
    ])

    prediction = crop_model.predict(features)

    return {
        "recommended_crop": prediction[0]
    }


# Weather by City
# =========================================================

@app.get("/weather/{city}")
def weather(city: str):

    import requests

    try:

        # ---------------------------------------------
        # Get Coordinates
        # ---------------------------------------------

        geo_url = (
            "https://geocoding-api.open-meteo.com/v1/search"
            f"?name={city}&count=1"
        )

        geo_response = requests.get(
            geo_url,
            timeout=10
        ).json()

        if "results" not in geo_response:
            return {
                "error": "City not found"
            }

        lat = geo_response["results"][0]["latitude"]
        lon = geo_response["results"][0]["longitude"]

        # ---------------------------------------------
        # Get Current Weather
        # ---------------------------------------------

        weather_url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}"
            f"&longitude={lon}"
            "&current=temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m"
        )

        weather_response = requests.get(
            weather_url,
            timeout=10
        ).json()

        current = weather_response["current"]

        return {
            "city": city.title(),
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "wind_speed": current["wind_speed_10m"],
            "condition": "Live Weather"
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# =========================================================
# Mandi Rates
# =========================================================

@app.get("/mandi/{city}")
def mandi(city: str):

    return {
        "city": city.title(),
        "crops": [
            {
                "name": "Wheat",
                "price": 2450
            },
            {
                "name": "Rice",
                "price": 2200
            },
            {
                "name": "Potato",
                "price": 1800
            },
            {
                "name": "Tomato",
                "price": 1500
            }
        ]
    }


# =========================================================
# Weather by Current Location
# =========================================================

@app.get("/weather-location")
def weather_location(
    lat: float,
    lon: float
):

    import requests

    try:

        # ---------------------------------------------
        # Weather API
        # ---------------------------------------------

        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}"
            f"&longitude={lon}"
            "&current=temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "weather_code"
            "&daily=weather_code,"
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max"
            "&forecast_days=7"
            "&timezone=auto"
        )

        response = requests.get(
            weather_url,
            timeout=10
        ).json()

        current = response["current"]
        daily = response["daily"]

        # ---------------------------------------------
        # Weather Condition
        # ---------------------------------------------

        def get_condition(code):

            mapping = {

                0: "Clear Sky",
                1: "Mainly Clear",
                2: "Partly Cloudy",
                3: "Cloudy",

                45: "Fog",
                48: "Fog",

                51: "Light Drizzle",
                53: "Drizzle",
                55: "Heavy Drizzle",

                56: "Freezing Drizzle",
                57: "Heavy Freezing Drizzle",

                61: "Light Rain",
                63: "Rain",
                65: "Heavy Rain",

                66: "Freezing Rain",
                67: "Heavy Freezing Rain",

                71: "Light Snow",
                73: "Snow",
                75: "Heavy Snow",

                77: "Snow Grains",

                80: "Rain Showers",
                81: "Heavy Showers",
                82: "Violent Rain",

                85: "Snow Showers",
                86: "Heavy Snow Showers",

                95: "Thunderstorm",
                96: "Thunderstorm with Hail",
                99: "Severe Thunderstorm",
            }

            return mapping.get(
                int(code),
                "Unknown"
            )

        # ---------------------------------------------
        # 7-Day Forecast
        # ---------------------------------------------

        forecast = []

        rain_probability = daily.get(
            "precipitation_probability_max",
            [0] * len(daily["time"])
        )

        for i in range(len(daily["time"])):

            forecast.append(
                {
                    "date": daily["time"][i],

                    "max_temp":
                        daily["temperature_2m_max"][i],

                    "min_temp":
                        daily["temperature_2m_min"][i],

                    "condition":
                        get_condition(
                            daily["weather_code"][i]
                        ),

                    "rain_probability":
                        rain_probability[i],
                }
            )

        # ---------------------------------------------
        # Farming Advisory
        # ---------------------------------------------

        temperature = current["temperature_2m"]

        rain = rain_probability[0]

        if rain >= 80:

            advice = (
                "🌧 Heavy rainfall expected. "
                "Avoid irrigation and ensure proper "
                "field drainage."
            )

        elif rain >= 60:

            advice = (
                "☔ High chance of rain. "
                "Delay irrigation and protect "
                "harvested crops."
            )

        elif temperature >= 35:

            advice = (
                "🌞 High temperature. "
                "Irrigate crops during morning "
                "or evening."
            )

        elif temperature >= 25:

            advice = (
                "🌱 Good weather for farming activities."
            )

        elif temperature >= 15:

            advice = (
                "🌤 Pleasant weather. "
                "Continue regular crop care."
            )

        else:

            advice = (
                "❄ Low temperature. "
                "Protect crops from cold."
            )

        # ---------------------------------------------
        # Reverse Geocoding
        # ---------------------------------------------

        city_name = "Current Location"

        try:

            headers = {
                "User-Agent": "AgriSmartAI/1.0"
            }

            geo = requests.get(
                "https://nominatim.openstreetmap.org/reverse",
                params={
                    "format": "jsonv2",
                    "lat": lat,
                    "lon": lon,
                },
                headers=headers,
                timeout=10,
            ).json()

            address = geo.get(
                "address",
                {}
            )

            city_name = (
                address.get("city")
                or address.get("town")
                or address.get("village")
                or address.get("municipality")
                or address.get("county")
                or address.get("state_district")
                or address.get("suburb")
                or "Current Location"
            )

        except Exception as e:

            print(
                "Reverse Geocoding Error:",
                e
            )

        # ---------------------------------------------
        # Final Response
        # ---------------------------------------------

        return {

            "city": city_name,

            "weather": {

                "temperature":
                    current["temperature_2m"],

                "humidity":
                    current["relative_humidity_2m"],

                "wind_speed":
                    current["wind_speed_10m"],

                "condition":
                    get_condition(
                        current["weather_code"]
                    ),

                "rain_probability":
                    rain_probability[0],
            },

            "forecast": forecast,

            "advisory": advice,
        }

    except Exception as e:

        return {
            "error": str(e)
        }