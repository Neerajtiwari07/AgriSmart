from services.rag.rag_chain import ask_rag


def execute_tool(tool: str, question: str, session_id: str = "default"):

    if tool == "rag":
        return ask_rag(question, session_id)

    elif tool == "weather":
        return "🌦 Weather tool selected (API integration next)."

    elif tool == "crop":
        return "🌾 Crop Prediction tool selected (ML model integration next)."

    elif tool == "disease":
        return "🦠 Disease Detection tool selected (Image model integration next)."

    return "I couldn't determine the correct tool."