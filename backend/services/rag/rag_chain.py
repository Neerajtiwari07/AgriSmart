import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser

from services.rag.vector_store import retrieve
from services.memory.history import get_session_history

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0.3
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are AgriSmart AI, an expert Agriculture Assistant.

Rules:

1. Answer ONLY from the provided context.
2. Never make up information.
3. If the answer is not present in the context, reply exactly:

"I don't have enough information in my knowledge base."

4. Answer in the same language as the user's question.
5. Keep answers short, practical and farmer-friendly.
6. If appropriate, explain in bullet points.
7. Never mention the word "context".

Context:
{context}
"""
    ),
    ("placeholder", "{history}"),
    ("human", "{question}")
])

chain = prompt | llm | StrOutputParser()

conversation = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)


def ask_rag(question: str, session_id: str = "default"):

    docs = retrieve(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    answer = conversation.invoke(
        {
            "question": question,
            "context": context,
        },
        config={
            "configurable": {
                "session_id": session_id
            }
        }
    )

    return answer