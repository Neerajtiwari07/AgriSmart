import requests
import pandas as pd
from fastapi import APIRouter

from services.crop_model import crop_model


router = APIRouter(
    prefix="/smart-crop",
    tags=["Smart Crop Recommendation"]
)


@router.post("/predict")
def smart_predict(data: dict):

    location = data.get("location", "").strip()
    soil_type = data.get("soil_type", "medium").lower()
    month = data.get("month")

    if not location:
        return {
            "success": False,
            "message": "Location is required."
        }

    # Soil mapping
    soil_values = {
        "low": {
            "N": 40,
            "P": 30,
            "K": 30,
            "ph": 6.0
        },
        "medium": {
            "N": 80,
            "P": 40,
            "K": 40,
            "ph": 6.5
        },
        "high": {
            "N": 120,
            "P": 60,
            "K": 60,
            "ph": 7.0
        }
    }

    soil = soil_values.get(
        soil_type,
        soil_values["medium"]
    )

    # Get coordinates
    geo_url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={location}&count=1"
    )

    geo_response = requests.get(
        geo_url,
        timeout=10
    ).json()

    if "results" not in geo_response:
        return {
            "success": False,
            "message": "Location not found."
        }

    lat = geo_response["results"][0]["latitude"]
    lon = geo_response["results"][0]["longitude"]

    # Get weather
    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m"
        "&daily=precipitation_sum"
        "&forecast_days=1"
    )

    weather_response = requests.get(
        weather_url,
        timeout=10
    ).json()

    temperature = weather_response["current"]["temperature_2m"]
    humidity = weather_response["current"]["relative_humidity_2m"]
    rainfall = weather_response["daily"]["precipitation_sum"][0]

    # Prepare ML features
    features = pd.DataFrame([
        {
            "N": soil["N"],
            "P": soil["P"],
            "K": soil["K"],
            "temperature": temperature,
            "humidity": humidity,
            "ph": soil["ph"],
            "rainfall": rainfall
        }
    ])

    # Existing crop model
    prediction = crop_model.predict(features)

    return {
        "success": True,
        "location": location.title(),
        "soil_type": soil_type,
        "month": month,
        "weather": {
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall
        },
        "recommended_crop": prediction[0]
    }