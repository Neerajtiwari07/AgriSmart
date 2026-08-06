import requests

from services.rag.rag_chain import ask_rag


def execute_tool(tool: str, question: str, session_id: str = "default"):

    # ---------------- RAG ----------------
    if tool == "rag":
        return ask_rag(question, session_id)

    # ---------------- Weather ----------------
    elif tool == "weather":

        city = extract_city(question)

        try:
            response = requests.get(
                f"http://127.0.0.1:8000/weather/{city}",
                timeout=10
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
            return f"Weather API Error : {e}"

    # ---------------- Crop ----------------
    elif tool == "crop":

     return {
        "type": "navigation",
        "page": "/crop-recommendation",
        "reply": "🌾 I can help you recommend the best crop.\n\nClick below to open the Crop Recommendation Tool."
    }

    # ---------------- Disease ----------------
    elif tool == "disease":

      return {
        "type": "navigation",
        "page": "/disease-detection",
        "reply": "🦠 I can help detect crop diseases.\n\nOpening Disease Detection Tool..."
    }
      
    # ---------------- Mandi ----------------
    
    elif tool == "mandi":

       return {
        "type": "navigation",
        "page": "/mandi-rates",
        "reply": "📈 I can help you check the latest mandi rates.\n\nOpening Mandi Rates Tool..."
    }


def extract_city(question):

    q = question.lower()

    q = q.replace("weather in", "")
    q = q.replace("weather", "")
    q = q.replace("temperature in", "")
    q = q.replace("forecast", "")

    city = q.strip()

    if city == "":
        city = "Lucknow"

    return city.title()