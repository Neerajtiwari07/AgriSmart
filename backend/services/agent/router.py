import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def route_question(question):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        temperature=0,

        messages=[
            {
                "role": "system",
                "content": """
You are an intent classifier.

Return ONLY one label.

Labels:

WEATHER
CROP_PREDICTION
DISEASE
MANDI
GENERAL_AGRICULTURE

Rules:

WEATHER:
Current weather, rain, humidity, temperature, wind, forecast.

Examples:
Weather in Lucknow
Temperature today
Rain forecast
Humidity

CROP_PREDICTION:
ONLY when user wants crop prediction using soil values.

Examples:
Recommend crop
Predict crop
Best crop for my soil
N=90 P=40 K=40

DISEASE:
Plant disease
Leaf disease
Yellow spots
Pest
Fungus
Tomato disease

MANDI:
Questions related to crop prices, mandi rates, market prices, MSP.

Examples:
Mandi rates
Wheat mandi price
Rice price today
Tomato market price
Today's mandi rate
आज का मंडी भाव
गेहूं का भाव
धान का रेट

GENERAL_AGRICULTURE:
Everything else.

Examples:
How to grow wheat
Best fertilizer for wheat
Organic farming
PM Kisan
Irrigation
Crop rotation

Reply ONLY ONE LABEL.
"""
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    label = response.choices[0].message.content.strip().upper()

    mapping = {
        "WEATHER": "weather",
        "CROP_PREDICTION": "crop",
        "DISEASE": "disease",
        "MANDI": "mandi",
        "GENERAL_AGRICULTURE": "rag",
    }

    return mapping.get(label, "rag")