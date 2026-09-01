import requests

from services.rag.rag_chain import ask_rag


# ============================================================
# EXECUTE TOOL
# ============================================================

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

            # ------------------------------------------------
            # Current Location Weather
            # ------------------------------------------------

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

                return format_weather_response(
                    data,
                    question,
                )


            # ------------------------------------------------
            # Default City
            # ------------------------------------------------

            if city is None:
                city = "Lucknow"


            # ------------------------------------------------
            # City Weather + Forecast
            # ------------------------------------------------

            response = requests.get(
                "http://127.0.0.1:8000/weather-location",
                params={
                    "lat": get_city_coordinates(city)[0],
                    "lon": get_city_coordinates(city)[1],
                },
                timeout=10,
            )

            data = response.json()

            if "error" in data:
                return data["error"]

            return format_weather_response(
                data,
                question,
            )


        except Exception as e:

            return f"Weather API Error: {e}"


    # ---------------- Crop ----------------

    elif tool == "crop":

        return {
            "type": "navigation",
            "page": "/crop-recommendation",
            "reply": (
                "🌾 I can help you recommend the best crop.\n\n"
                "Opening Crop Recommendation Tool..."
            ),
        }


    # ---------------- Disease ----------------

    elif tool == "disease":

        return {
            "type": "navigation",
            "page": "/disease-detection",
            "reply": (
                "🦠 I can help detect crop diseases.\n\n"
                "Opening Disease Detection Tool..."
            ),
        }


    # ---------------- Mandi ----------------

    elif tool == "mandi":

        return {
            "type": "navigation",
            "page": "/mandi-rates",
            "reply": "📈 Opening Mandi Rates Tool...",
        }


    return "I don't understand the request."


# ============================================================
# CITY COORDINATES
# ============================================================

def get_city_coordinates(city):

    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        },
        timeout=10,
    )

    data = response.json()

    if "results" not in data or not data["results"]:
        raise ValueError(f"City not found: {city}")

    result = data["results"][0]

    return (
        result["latitude"],
        result["longitude"],
    )


# ============================================================
# WEATHER RESPONSE
# ============================================================

def format_weather_response(data, question):

    weather = data.get("weather", {})
    forecast = data.get("forecast", [])

    q = question.lower()

    # --------------------------------------------------------
    # Rain Question Detection
    # --------------------------------------------------------

    rain_words = [
        "rain",
        "rainfall",
        "barish",
        "baarish",
        "बारिश",
        "वर्षा",
        "rain forecast",
        "barish kab",
        "baarish kab",
        "बारिश कब",
        "वर्षा कब",
        "will it rain",
        "when will it rain",
    ]

    is_rain_question = any(
        word in q
        for word in rain_words
    )


    # --------------------------------------------------------
    # Rain Forecast
    # --------------------------------------------------------

    if is_rain_question:

        forecast_lines = []

        for day in forecast:

            date = day.get("date", "Unknown")
            probability = day.get(
                "rain_probability",
                0,
            )
            condition = day.get(
                "condition",
                "Unknown",
            )

            forecast_lines.append(
                f"📅 {date}\n"
                f"🌧 Rain Probability : {probability}%\n"
                f"☁ Condition : {condition}"
            )


        forecast_text = "\n\n".join(
            forecast_lines
        )


        return f"""
🌧 Rain Forecast

📍 Location : {data.get('city', 'Current Location')}

{forecast_text}

💡 Advisory:
{data.get('advisory', '')}
"""


    # --------------------------------------------------------
    # Normal Current Weather
    # --------------------------------------------------------

    return f"""
🌦 Current Weather

📍 Location : {data.get('city', 'Current Location')}

🌡 Temperature : {weather.get('temperature')}°C

💧 Humidity : {weather.get('humidity')}%

💨 Wind Speed : {weather.get('wind_speed')} km/h

☁ Condition : {weather.get('condition')}

💡 Advisory:
{data.get('advisory', '')}
"""


# ============================================================
# EXTRACT CITY
# ============================================================

def extract_city(question):

    q = question.lower().strip()

    # --------------------------------------------------------
    # Common spelling
    # --------------------------------------------------------

    q = q.replace(
        "wether",
        "weather"
    )


    # --------------------------------------------------------
    # Weather questions without city
    # --------------------------------------------------------

    no_city_questions = [

        # English
        "weather",
        "today weather",
        "current weather",
        "weather today",
        "today",

        "when will it rain",
        "when will it rain?",
        "rain today",
        "rain forecast",
        "will it rain",
        "will it rain?",
        "is it going to rain",
        "is it going to rain?",

        "temperature today",
        "humidity today",

        # Hinglish
        "barish",
        "barish?",
        "baarish",
        "baarish?",

        "barish kab hogi",
        "barish kab hogi?",

        "baarish kab hogi",
        "baarish kab hogi?",

        "mausam",
        "mausam kaisa hai",
        "mausam kaisa hai?",

        "aaj barish hogi",
        "aaj barish hogi?",

        "aaj baarish hogi",
        "aaj baarish hogi?",

        # Hindi
        "बारिश",
        "बारिश?",

        "बारिश कब होगी",
        "बारिश कब होगी?",

        "आज बारिश होगी",
        "आज बारिश होगी?",

        "वर्षा",
        "वर्षा कब होगी",
        "वर्षा कब होगी?",

        "मौसम",
        "मौसम कैसा है",
        "मौसम कैसा है?",

        "आज का मौसम",

        "तापमान",
        "आज तापमान कितना है",
        "आज तापमान कितना है?",

        "नमी",
        "हवा",
    ]


    if q in no_city_questions:
        return None


    # --------------------------------------------------------
    # Remove weather words
    # --------------------------------------------------------

    keywords = [

        "weather in",
        "weather at",
        "weather of",
        "weather for",

        "weather",
        "today",
        "current",
        "forecast",
        "temperature",
        "humidity",
        "wind",
        "rain",
        "rainfall",

        "barish",
        "baarish",
        "mausam",
        "taapman",
        "nami",
        "hawa",

        "बारिश",
        "वर्षा",
        "मौसम",
        "तापमान",
        "नमी",
        "हवा",
    ]


    for word in keywords:

        q = q.replace(
            word,
            ""
        )


    city = q.strip()


    if not city:
        return None


    return city.title()