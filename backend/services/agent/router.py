from services.rag.rag_chain import ask_rag


def route_question(question: str):

    text = question.lower()

    # Weather
    if any(word in text for word in [
        "weather",
        "temperature",
        "rain",
        "humidity",
        "wind",
        "forecast"
    ]):

        return {
            "tool": "weather"
        }

    # Crop Recommendation
    if any(word in text for word in [
        "crop",
        "recommend",
        "soil",
        "nitrogen",
        "phosphorus",
        "potassium",
        "fertilizer"
    ]):

        return {
            "tool": "crop"
        }

    # Disease
    if any(word in text for word in [
        "disease",
        "leaf",
        "spot",
        "fungus",
        "infection",
        "yellow"
    ]):

        return {
            "tool": "disease"
        }

    # Default

    return {
        "tool": "rag"
    }