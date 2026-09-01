import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def route_question(question: str):

    question = question.strip()

    if not question:
        return "rag"

    # --------------------------------------------------------
    # Direct Weather Detection
    # --------------------------------------------------------

    weather_keywords = [
        "weather",
        "temperature",
        "humidity",
        "wind",
        "rain",
        "rainfall",
        "forecast",

        # Hindi
        "बारिश",
        "वर्षा",
        "मौसम",
        "तापमान",
        "नमी",
        "हवा",

        # Hinglish
        "barish",
        "baarish",
        "mausam",
        "taapman",
        "nami",
        "hawa",
    ]

    q_lower = question.lower()

    if any(word in q_lower for word in weather_keywords):
        return "weather"

    # --------------------------------------------------------
    # Follow-up Questions
    # --------------------------------------------------------

    follow_up_words = [
        "isko",
        "ise",
        "iska",
        "iski",
        "iske",
        "isme",
        "isey",
        "kab",
        "kaise",
        "kyu",
        "kyun",
        "kitna",
        "kitni",
        "kitne",
        "what about this",
        "how about this",
        "when should i",
        "how should i",
        "and this",
        "this",
        "it",
    ]

    if any(word in q_lower for word in follow_up_words):
        return "rag"

    # --------------------------------------------------------
    # Intent Classification
    # --------------------------------------------------------

    try:

        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

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

    except Exception as e:

        print("ROUTER ERROR:", e)

        return "rag"

    # --------------------------------------------------------
    # Label Mapping
    # --------------------------------------------------------

    mapping = {
        "WEATHER": "weather",
        "CROP_PREDICTION": "crop",
        "DISEASE": "disease",
        "MANDI": "mandi",
        "GENERAL_AGRICULTURE": "rag",
    }

    return mapping.get(label, "rag")