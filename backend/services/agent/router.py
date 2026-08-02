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
GENERAL_AGRICULTURE

Rules:

WEATHER:
Current weather, rain, humidity, temperature, wind, forecast.

CROP_PREDICTION:
ONLY when user wants crop prediction using soil values.

Examples:

N=90 P=40 K=40
Recommend crop

Predict crop

Best crop for my soil

DISEASE:
Leaf disease
Yellow spots
Pest
Fungus
Plant infection

GENERAL_AGRICULTURE:
Everything else.

Examples:

How to grow wheat

Best fertilizer for wheat

Wheat cultivation

PM Kisan

Irrigation

Organic farming

Reply ONLY ONE LABEL.
"""
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    label = response.choices[0].message.content.strip()

    mapping = {
        "WEATHER": "weather",
        "CROP_PREDICTION": "crop",
        "DISEASE": "disease",
        "GENERAL_AGRICULTURE": "rag",
    }

    return mapping.get(label, "rag")