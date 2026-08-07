from services.agent.router import route_question
from services.agent.executor import execute_tool


def get_chat_response(data: dict):

    question = data.get("message", "").strip()
    session_id = data.get("session_id", "default")

    # NEW
    lat = data.get("lat")
    lon = data.get("lon")

    if not question:
        return {
            "success": False,
            "reply": "Please enter a question."
        }

    tool = route_question(question)

    # UPDATED
    answer = execute_tool(
        tool=tool,
        question=question,
        session_id=session_id,
        lat=lat,
        lon=lon
    )

    if isinstance(answer, dict):
        return {
            "success": True,
            **answer
        }

    return {
        "success": True,
        "reply": answer
    }