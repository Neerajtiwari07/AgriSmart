from services.agent.router import route_question
from services.rag.rag_chain import ask_rag


def get_chat_response(data):

    question = data.get("message", "")

    session = data.get("session_id", "default")

    tool = route_question(question)

    if tool["tool"] == "rag":

        answer = ask_rag(
            question,
            session
        )

        return {
            "success": True,
            "reply": answer
        }

    return {
        "success": True,
        "reply": f"Selected Tool : {tool['tool']}"
    }