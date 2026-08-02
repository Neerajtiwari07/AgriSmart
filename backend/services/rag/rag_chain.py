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
        """You are AgriSmart AI.

You are an expert Agriculture Assistant.

Use ONLY the given context to answer.

If the answer is not available in the context,
say "I don't have enough information."

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