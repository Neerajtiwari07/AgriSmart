import requests

from services.rag.rag_chain import ask_rag


def execute_tool(
    tool: str,
    question: str,
    session_id: str = "default",
    lat=None,
    lon=None,
):

    # ---------------- RAG ----------------
    if tool == "rag":
        return ask_rag(question, session_id)

    # ---------------- Weather ----------------
    elif tool == "weather":

        city = extract_city(question)

        try:

            # Current Location Weather
            if city is None and lat is not None and lon is not None:

                response = requests.get(
                    "http://127.0.0.1:8000/weather-location",
                    params={
                        "lat": lat,
                        "lon": lon,
                    },
                    timeout=10,
                )

                data = response.json()

                if "error" in data:
                    return data["error"]

                weather = data["weather"]

                return f"""
🌦 Current Weather

📍 Location : {data['city']}

🌡 Temperature : {weather['temperature']}°C

💧 Humidity : {weather['humidity']}%

💨 Wind Speed : {weather['wind_speed']} km/h

☁ Condition : {weather['condition']}

💡 Advisory:
{data['advisory']}
"""

            # Weather by City
            if city is None:
                city = "Lucknow"

            response = requests.get(
                f"http://127.0.0.1:8000/weather/{city}",
                timeout=10,
            )

            data = response.json()

            if "error" in data:
                return data["error"]

            return f"""
🌦 Weather Report

📍 City : {data['city']}

🌡 Temperature : {data['temperature']}°C

💧 Humidity : {data['humidity']}%

💨 Wind Speed : {data['wind_speed']} km/h

☁ Condition : {data['condition']}
"""

        except Exception as e:
            return f"Weather API Error: {e}"

    # ---------------- Crop ----------------
    elif tool == "crop":

        return {
            "type": "navigation",
            "page": "/crop-recommendation",
            "reply": "🌾 I can help you recommend the best crop.\n\nOpening Crop Recommendation Tool...",
        }

    # ---------------- Disease ----------------
    elif tool == "disease":

        return {
            "type": "navigation",
            "page": "/disease-detection",
            "reply": "🦠 I can help detect crop diseases.\n\nOpening Disease Detection Tool...",
        }

    # ---------------- Mandi ----------------
    elif tool == "mandi":

        return {
            "type": "navigation",
            "page": "/mandi-rates",
            "reply": "📈 Opening Mandi Rates Tool...",
        }

    return "I don't understand the request."


def extract_city(question):

    q = question.lower().strip()

    # Common spelling mistakes
    q = q.replace("wether", "weather")

    # If user wants current weather
    if q in [
        "weather",
        "today weather",
        "current weather",
        "weather today",
        "today",
    ]:
        return None

    keywords = [
        "weather in",
        "weather at",
        "weather",
        "today",
        "current",
        "forecast",
        "temperature",
        "humidity",
        "wind",
        "rain",
    ]

    for word in keywords:
        q = q.replace(word, "")

    city = q.strip()

    if city == "":
        return None

    return city.title()