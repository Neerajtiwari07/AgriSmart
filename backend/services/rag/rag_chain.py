import os
import re

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from services.rag.vector_store import retrieve
from services.rag.context_validator import validate_context
from services.memory.history import get_session_history


# ============================================================
# PHASE 5 - RAG 2.0
# RAG PIPELINE INTEGRATION
#
# User Query
#      ↓
# Query Rewriting
#      ↓
# Retrieval
#      ↓
# Context Validation
#      ↓
# Clean Context
#      ↓
# Groq
#      ↓
# Final Answer
# ============================================================


# ============================================================
# CONFIG
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing"
    )


FALLBACK = (
    "I don't have enough information "
    "in my knowledge base."
)


# ============================================================
# MODEL
# ============================================================

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="qwen/qwen3.6-27b",
    temperature=0,
    reasoning_format="hidden",
)


# ============================================================
# ANSWER PROMPT
# ============================================================

# ============================================================
# ANSWER GENERATION PROMPT
# ============================================================

answer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are AgriSmart AI, an agriculture assistant.

Answer the user's question using ONLY the agriculture context provided below.

Rules:
1. Use the provided context as the primary knowledge source.
2. Do not invent facts that are not supported by the context.
3. If the exact answer is not available, clearly say that the available context does not contain the exact information.
4. You may combine information from multiple context documents when they are relevant.
5. Answer in the same language as the user's question.
6. Keep the answer concise and practical.
7. Do not mention FAISS, RAG, vector database, retrieval, prompts, or internal system details.

AGRICULTURE CONTEXT:
{context}
"""
    ),
    (
        "human",
        """
User Question:
{question}

Provide the best answer supported by the agriculture context.
"""
    ),
])

# ============================================================
# ANSWER CHAIN
# ============================================================

answer_chain = (
    answer_prompt
    | llm
    | StrOutputParser()
)


# ============================================================
# SEARCH QUERY REWRITER PROMPT
# ============================================================

search_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a search-query optimizer for an agriculture knowledge base.

Your job is ONLY to rewrite the user's question into a better
semantic search query.

Rules:

1. Do not answer the question.
2. Do not provide explanations.
3. Do not invent agricultural facts.
4. Preserve the exact meaning of the user's question.
5. If the query is Hindi, Hinglish, or Roman Hindi, include useful
   equivalent words in Hindi and English when appropriate.
6. If the query is an English word, include its common Hindi equivalent
   when appropriate.
7. For a crop/topic name, include its common equivalent spellings
   or translations.
8. For a follow-up question, use the previous conversation to resolve
   words such as:
   isko, ise, iska, iski, isme, this, it, when, how, why.
9. Keep the result short.
10. Return ONLY the search query.
11. Never return an answer.
"""
    ),
    (
        "human",
        """
Previous conversation:
{history}

Current question:
{question}
"""
    )
])


# ============================================================
# SEARCH CHAIN
# ============================================================

search_chain = (
    search_prompt
    | llm
    | StrOutputParser()
)


# ============================================================
# GREETINGS
# ============================================================

GREETINGS = {

    "hello":
        "Hello! I am AgriSmart AI. I can help you with farming-related questions.",

    "hi":
        "Hi! I am AgriSmart AI. I can help you with farming-related questions.",

    "hey":
        "Hey! I am AgriSmart AI. I can help you with farming-related questions.",

    "namaste":
        "Namaste! Main AgriSmart AI hoon. Main kheti se jude sawalon me aapki madad kar sakta hoon.",

    "नमस्ते":
        "नमस्ते! मैं AgriSmart AI हूँ। मैं खेती से जुड़े सवालों में आपकी मदद कर सकता हूँ।",
}


# ============================================================
# CLEAN RESPONSE
# ============================================================

def clean_response(answer: str) -> str:

    if not answer:
        return ""

    answer = str(
        answer
    ).strip()


    # --------------------------------------------------------
    # Remove <think>...</think>
    # --------------------------------------------------------

    answer = re.sub(
        r"<think>.*?</think>",
        "",
        answer,
        flags=re.DOTALL | re.IGNORECASE,
    )


    # --------------------------------------------------------
    # Remove remaining think tags
    # --------------------------------------------------------

    answer = re.sub(
        r"</?think>",
        "",
        answer,
        flags=re.IGNORECASE,
    )


    # --------------------------------------------------------
    # Remove common prefixes
    # --------------------------------------------------------

    answer = re.sub(
        r"^\s*(Output|Final Answer|Answer|Response)\s*:\s*",
        "",
        answer,
        flags=re.IGNORECASE,
    )


    # --------------------------------------------------------
    # Reject visible reasoning
    # --------------------------------------------------------

    bad_phrases = [

        "thinking process",

        "analyze user input",

        "check provided information",

        "scan provided information",

        "apply rules",

        "match & extract",

        "draft response",

        "verify against constraints",

        "self-correction",

        "tags in output",

        "output matches requirement",

        "final check",

        "[output generation]",

        "[final response generation]",
    ]


    lower = answer.lower()


    if any(
        phrase in lower
        for phrase in bad_phrases
    ):

        return ""


    # --------------------------------------------------------
    # Remove duplicate consecutive lines
    # --------------------------------------------------------

    cleaned_lines = []


    for line in answer.splitlines():

        line = line.strip()


        if not line:
            continue


        if (
            not cleaned_lines
            or line != cleaned_lines[-1]
        ):

            cleaned_lines.append(
                line
            )


    answer = "\n".join(
        cleaned_lines
    ).strip()


    # --------------------------------------------------------
    # Remove complete duplicated answer
    # --------------------------------------------------------

    if len(answer) > 20:

        half = len(answer) // 2

        first = answer[
            :half
        ].strip()

        second = answer[
            half:
        ].strip()


        if first == second:

            answer = first


    return answer.strip()


# ============================================================
# GET CONVERSATION HISTORY
# ============================================================

def get_history_text(
    session_id: str
) -> str:

    try:

        history = get_session_history(
            session_id
        )


        if not history.messages:

            return ""


        messages = []


        # ----------------------------------------------------
        # Only use recent messages
        # ----------------------------------------------------

        for message in history.messages[-6:]:

            message_type = getattr(
                message,
                "type",
                ""
            )


            content = str(
                getattr(
                    message,
                    "content",
                    ""
                )
            ).strip()


            if not content:
                continue


            if message_type == "human":

                messages.append(
                    f"User: {content}"
                )


            elif message_type == "ai":

                messages.append(
                    f"Assistant: {content}"
                )


        return "\n".join(
            messages
        )


    except Exception as e:

        print(
            "MEMORY ERROR:",
            e
        )

        return ""


# ============================================================
# BUILD SEARCH QUERY
# ============================================================

def build_search_query(
    question: str,
    session_id: str,
) -> str:

    history_text = get_history_text(
        session_id
    )


    # --------------------------------------------------------
    # No history
    # --------------------------------------------------------

    if not history_text:

        history_for_prompt = (
            "No previous conversation."
        )

    else:

        history_for_prompt = (
            history_text
        )


    # --------------------------------------------------------
    # Query rewrite
    # --------------------------------------------------------

    try:

        rewritten = search_chain.invoke(
            {
                "history":
                    history_for_prompt,

                "question":
                    question,
            }
        )


        rewritten = str(
            rewritten
        ).strip()


    except Exception as e:

        print(
            "QUERY REWRITE ERROR:",
            e
        )

        rewritten = question


    # --------------------------------------------------------
    # Safety
    # --------------------------------------------------------

    if not rewritten:

        rewritten = question


    # --------------------------------------------------------
    # Never completely lose original query
    # --------------------------------------------------------

    if (
        question.lower()
        not in rewritten.lower()
    ):

        rewritten = (
            f"{question} {rewritten}"
        )


    return rewritten.strip()


# ============================================================
# BUILD VALIDATED CONTEXT
# ============================================================

def build_validated_context(
    question: str,
    docs
):

    if not question:
        return ""


    if not docs:
        return ""


    # --------------------------------------------------------
    # Context Validation
    # --------------------------------------------------------

    try:

        validated_context = (
            validate_context(
                question,
                docs
            )
        )

    except Exception as e:

        print(
            "CONTEXT VALIDATION ERROR:",
            e
        )

        return ""


    print("=" * 70)
    print(
        "VALIDATED CONTEXT:",
        len(validated_context)
    )
    print("=" * 70)


    # --------------------------------------------------------
    # No valid context
    # --------------------------------------------------------

    if not validated_context:

        print(
            "NO RELEVANT CONTEXT FOUND"
        )

        return ""


    # --------------------------------------------------------
    # Build context only from validated docs
    # --------------------------------------------------------

    context_parts = []


    for index, item in enumerate(
        validated_context[:5],
        start=1
    ):

        doc = item.get(
            "document"
        )


        if not doc:
            continue


        if not hasattr(
            doc,
            "page_content"
        ):
            continue


        content = str(
            doc.page_content
        ).strip()


        if not content:
            continue


        context_parts.append(
            content
        )


        print(
            f"Context Document {index}:",
            doc.metadata.get(
                "question",
                ""
            )
        )


        print(
            "Validation Score:",
            round(
                item.get(
                    "relevance_score",
                    0.0
                ),
                4
            )
        )


        print(
            "Reason:",
            item.get(
                "reason",
                ""
            )
        )


    return "\n\n".join(
        context_parts
    )


# ============================================================
# ASK RAG
# ============================================================


def ask_rag(
    question: str,
    session_id: str = "default",
):


    # ========================================================
    # VALIDATE QUESTION
    # ========================================================

    if (
        not question
        or not question.strip()
    ):

        return "Please ask a question."


    question = question.strip()

    normalized = question.lower()


    # ========================================================
    # GREETING
    # ========================================================

    if normalized in GREETINGS:

        return GREETINGS[
            normalized
        ]


    # ========================================================
    # BUILD BETTER SEARCH QUERY
    # ========================================================

    search_query = build_search_query(
        question,
        session_id
    )


    print("=" * 70)
    print(
        "USER QUESTION :",
        question
    )

    print(
        "SEARCH QUERY  :",
        search_query
    )

    print("=" * 70)


    # ========================================================
    # RETRIEVE
    # ========================================================

    try:

        docs = retrieve(
            search_query
        )


    except Exception as e:

        print(
            "RETRIEVAL ERROR:",
            e
        )

        return FALLBACK


    print(
        "DOCUMENTS RETRIEVED:",
        len(docs)
    )


    # ========================================================
    # NO RETRIEVED DOCUMENTS
    # ========================================================

    if not docs:

        return FALLBACK


    # ========================================================
    # CONTEXT VALIDATION
    # ========================================================

    context = build_validated_context(
        question,
        docs
    )


    # ========================================================
    # NO VALID CONTEXT
    # ========================================================

    if not context:

        return FALLBACK


    # ========================================================
    # DEBUG CONTEXT
    # ========================================================

    print("=" * 70)
    print(
        "FINAL VALIDATED CONTEXT:"
    )
    print(
        context[:4000]
    )
    print("=" * 70)


       # ========================================================
    # GENERATE ANSWER
    # ========================================================

    try:

        print("=" * 70)
        print("ANSWER GENERATION INPUT")
        print("QUESTION:", question)
        print("-" * 70)
        print("CONTEXT:")
        print(context)
        print("=" * 70)

        answer = answer_chain.invoke(
            {
                "question": question,
                "context": context,
            }
        )

        # ----------------------------------------------------
        # DEBUG RAW LLM RESPONSE
        # ----------------------------------------------------

        print("=" * 70)
        print("RAW LLM ANSWER:")
        print(repr(answer))
        print("=" * 70)

    except Exception as e:

        print(
            "LLM ERROR:",
            e
        )

        return FALLBACK

    # ========================================================
    # CLEAN RESPONSE
    # ========================================================

    answer = clean_response(
        answer
    )


    # ========================================================
    # EMPTY / INVALID ANSWER
    # ========================================================

    if not answer:

        return FALLBACK


    # ========================================================
    # FINAL ANSWER
    # ========================================================

    return answer