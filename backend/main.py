from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
from fastapi import UploadFile, File
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Trained Model
with open("models/crop_model.pkl", "rb") as f:
    model = pickle.load(f)


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

    prediction = model.predict(features)

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

    message = data["message"].lower()

    if "yellow" in message or "पीले" in message:
        reply = """
        Yellow leaves may indicate Nitrogen deficiency.
        Apply urea and check soil nutrients.
        """

    elif "wheat" in message or "गेहूं" in message:
        reply = """
        Wheat grows best in well-drained loamy soil.
        Recommended temperature: 10-25°C.
        Use balanced NPK fertilizer.
        """

    elif "rice" in message or "धान" in message:
        reply = """
        Rice requires high rainfall and standing water.
        Maintain proper irrigation and nitrogen supply.
        """

    else:
        reply = "Please provide more details."

    return {"reply": reply}