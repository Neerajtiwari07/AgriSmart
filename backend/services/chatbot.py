from services.agent.router import route_question
from services.agent.executor import execute_tool


def get_chat_response(data: dict):

    question = data.get("message", "").strip()
    session_id = data.get("session_id", "default")

    if not question:
        return {
            "success": False,
            "reply": "Please enter a question."
        }

    tool = route_question(question)

    answer = execute_tool(tool, question, session_id)

    if isinstance(answer, dict):   

     return {
        "success": True,
        **answer
    }

    return {
    "success": True,
    "reply": answer
}