from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import pickle
import pandas as pd
import requests
import os

from groq import Groq
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found in .env")

# Initialize Groq Client
client = Groq(
    api_key=GROQ_API_KEY
)

print("✅ Groq API configured successfully")

# FastAPI App
app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://agri-smart-nu.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Crop Recommendation Model
with open("models/crop_model.pkl", "rb") as f:
    crop_model = pickle.load(f)


@app.get("/")
def home():
    return {"message": "AgriSmart AI Backend Running"}


@app.post("/predict")
def predict(data: dict):

    features = pd.DataFrame([{
        "N": float(data["nitrogen"]),
        "P": float(data["phosphorus"]),
        "K": float(data["potassium"]),
        "temperature": float(data["temperature"]),
        "humidity": float(data["humidity"]),
        "ph": float(data["ph"]),
        "rainfall": float(data["rainfall"])
    }])

    prediction = crop_model.predict(features)

    return {
        "recommended_crop": prediction[0]
    }
    
@app.post("/detect-disease")
async def detect_disease(file: UploadFile = File(...)):

    return {
        "disease": "Tomato Healthy",
        "confidence": "98.5%",
        "treatment": "No treatment required."
    }
    
@app.get("/weather/{city}")
def weather(city: str):

    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"

    geo_response = requests.get(geo_url).json()

    if "results" not in geo_response:
        return {"error": "City not found"}

    lat = geo_response["results"][0]["latitude"]
    lon = geo_response["results"][0]["longitude"]

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )

    weather_response = requests.get(weather_url).json()

    current = weather_response["current"]

    return {
        "city": city.title(),
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "condition": "Live Weather"
    }
    
@app.get("/mandi/{city}")
def mandi(city: str):

    return {
        "city": city.title(),
        "crops": [
            {"name": "Wheat", "price": 2450},
            {"name": "Rice", "price": 2200},
            {"name": "Potato", "price": 1800},
            {"name": "Tomato", "price": 1500}
        ]
    }
    

@app.post("/chat")
def chat(data: dict):

    try:

        user_message = data.get("message","").strip()

        if user_message == "":
            return {
                "success":False,
                "reply":"Please enter a question."
            }

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            temperature=0.5,

            messages=[

                {
                    "role":"system",

                    "content":"""

You are AgriSmart AI.

You are an expert Agriculture Assistant.

Rules:

1. Answer only farming related questions.

2. If user asks unrelated questions politely refuse.

3. Support Hindi and English.

4. Keep answers short and practical.

5. Give fertilizer suggestions if needed.

6. Give disease treatment if needed.

7. Give irrigation advice whenever useful.

"""

                },

                {
                    "role":"user",
                    "content":user_message
                }

            ]

        )

        answer = completion.choices[0].message.content

        return {

            "success":True,

            "reply":answer

        }

    except Exception as e:

        return {

            "success":False,

            "reply":str(e)

        }
    
@app.get("/weather-location")
def weather_location(lat: float, lon: float):
    try:
        weather_url = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={lat}"
    f"&longitude={lon}"
    f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
    f"&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max"
    f"&forecast_days=7"
    f"&timezone=auto"
)

        response = requests.get(weather_url, timeout=10).json()

        current = response["current"]
        daily = response["daily"]

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
            return mapping.get(int(code), "Unknown")

        forecast = []

        for i in range(len(daily["time"])):
            forecast.append({
                "date": daily["time"][i],
                "max_temp": daily["temperature_2m_max"][i],
                "min_temp": daily["temperature_2m_min"][i],
                "condition": get_condition(daily["weather_code"][i]),
                "rain_probability": daily.get("precipitation_probability_max", [0] * len(daily["time"]))[i]
            })

        temp = current["temperature_2m"]
        rain = daily.get("precipitation_probability_max", [0])[0]

        if rain >= 80:
            advice = "🌧 Heavy rainfall expected. Avoid irrigation and ensure proper field drainage."

        elif rain >= 60:
            advice = "☔ High chance of rain. Delay irrigation and protect harvested crops."

        elif temp >= 35:
            advice = "🌞 High temperature. Irrigate crops during morning or evening."

        elif temp >= 25:
            advice = "🌱 Good weather for farming activities."

        elif temp >= 15:
            advice = "🌤 Pleasant weather. Continue regular crop care."

        else:
            advice = "❄ Low temperature. Protect crops from cold."

        # Reverse Geocoding
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
                    "lon": lon
                },
                headers=headers,
                timeout=10
            ).json()

            print("Geo Response:", geo)

            address = geo.get("address", {})

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
            print("Reverse Geocoding Error:", e)

        return {
            "city": city_name,
            "weather": {
                "temperature": current["temperature_2m"],
                "humidity": current["relative_humidity_2m"],
                "wind_speed": current["wind_speed_10m"],
                "condition": get_condition(current["weather_code"]),
                "rain_probability": daily["precipitation_probability_max"][0]
            },
            "forecast": forecast,
            "advisory": advice
        }

    except Exception as e:
        return {"error": str(e)}