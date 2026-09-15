# ============================================================
# PHASE 5 - RAG 2.0
# RAG PIPELINE + CONVERSATIONAL REFERENCE RESOLUTION
#
# User Query
#      ↓
# Conversation History
#      ↓
# Reference Resolution
#      ↓
# Query Understanding
#      ↓
# Hybrid Retrieval
#      ↓
# Context Validation
#      ↓
# Clean Context
#      ↓
# Local Qwen Answer Generation
#      ↓
# Final Answer
#      ↓
# Save Conversation
#
# LOCAL GENAI:
# Ollama + Qwen 2.5 1.5B
#
# Groq has been completely removed.
# ============================================================

import re

from langchain_core.messages import HumanMessage, AIMessage

from services.rag.vector_store import retrieve
from services.rag.context_validator import validate_context
from services.rag.reference_resolver import resolve_reference
from services.rag.local_llm import generate_with_ollama
from services.memory.history import get_session_history


# ============================================================
# CONFIG
# ============================================================

FALLBACK = (
    "I don't have enough information "
    "in my knowledge base."
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

    answer = str(answer).strip()

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
            cleaned_lines.append(line)

    answer = "\n".join(
        cleaned_lines
    ).strip()

    # --------------------------------------------------------
    # Remove complete duplicated answer
    # --------------------------------------------------------

    if len(answer) > 20:

        half = len(answer) // 2

        first = answer[:half].strip()
        second = answer[half:].strip()

        if first == second:
            answer = first

    return answer.strip()


# ============================================================
# LOCAL QWEN PROMPT
# PHASE 6 - GENAI + RAG
# ============================================================

def build_answer_prompt(
    question: str,
    resolved_question: str,
    conversation_history: str,
    context: str,
) -> str:

    return f"""
You are AgriSmart AI.

Answer the user's question using the agriculture information
provided below.

RULES:
- Give ONLY the answer.
- Do not repeat the question.
- Do not explain your reasoning.
- Use the agriculture context as the main factual source.
- Do not invent exact doses, quantities, dates, or measurements.
- Hindi question = Hindi answer.
- English question = English answer.
- Hinglish question = natural Hinglish/Hindi answer.
- Do not mention the system, RAG, FAISS, Qwen, Ollama, or database.

LANGUAGE RULE:

The answer MUST use the same language as the CURRENT USER QUESTION.

- If the CURRENT USER QUESTION is written in Hindi (Devanagari),
  answer ONLY in Hindi (Devanagari).

- If the CURRENT USER QUESTION is written in English,
  answer ONLY in English.

- If the CURRENT USER QUESTION is Hinglish written mainly in Roman script,
  answer in natural Hinglish.

IMPORTANT:
- Determine the language ONLY from the CURRENT USER QUESTION.
- Do NOT determine the answer language from the agriculture context.
- The retrieved context may be in English or Hindi, but that does NOT
  determine the answer language.
- Never answer a Hindi Devanagari question in English.
- Never translate the user's Hindi question into English before answering.

USER QUESTION:
{question}

RESOLVED QUESTION:
{resolved_question}

AGRICULTURE CONTEXT:
{context}

ANSWER:
""".strip()
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
        # Only recent messages
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
# GET PREVIOUS USER QUESTION
# ============================================================

def get_previous_user_question(
    session_id: str
) -> str:

    try:

        history = get_session_history(
            session_id
        )

        if not history.messages:
            return ""

        # ----------------------------------------------------
        # Search backwards for latest human message
        # ----------------------------------------------------

        for message in reversed(
            history.messages
        ):

            message_type = getattr(
                message,
                "type",
                ""
            )

            if message_type != "human":
                continue

            content = str(
                getattr(
                    message,
                    "content",
                    ""
                )
            ).strip()

            if content:
                return content

        return ""

    except Exception as e:

        print(
            "PREVIOUS QUESTION ERROR:",
            e
        )

        return ""


# ============================================================
# RESOLVE CURRENT QUERY
# ============================================================

def resolve_current_question(
    question: str,
    session_id: str
):

    previous_question = (
        get_previous_user_question(
            session_id
        )
    )

    # --------------------------------------------------------
    # Reference Resolver
    # --------------------------------------------------------

    try:

        result = resolve_reference(
            current_query=question,
            previous_query=previous_question
        )

    except Exception as e:

        print(
            "REFERENCE RESOLUTION ERROR:",
            e
        )

        return {
            "original_query": question,
            "resolved_query": question,
            "reference": None,
            "crop": None,
            "intent": None,
            "resolved": False,
        }

    print("=" * 70)
    print("REFERENCE RESOLUTION")

    print(
        "PREVIOUS QUESTION:",
        previous_question
    )

    print(
        "CURRENT QUESTION :",
        question
    )

    print(
        "REFERENCE        :",
        result.get("reference")
    )

    print(
        "RESOLVED         :",
        result.get("resolved")
    )

    print(
        "RESOLVED QUERY   :",
        result.get("resolved_query")
    )

    print("=" * 70)

    return result


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
# SAVE CONVERSATION
# ============================================================

def save_conversation(
    session_id: str,
    user_question: str,
    assistant_answer: str
):

    try:

        history = get_session_history(
            session_id
        )

        history.add_message(
            HumanMessage(
                content=user_question
            )
        )

        history.add_message(
            AIMessage(
                content=assistant_answer
            )
        )

    except Exception as e:

        print(
            "MEMORY SAVE ERROR:",
            e
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

        answer = GREETINGS[
            normalized
        ]

        save_conversation(
            session_id,
            question,
            answer
        )

        return answer

    # ========================================================
    # REFERENCE RESOLUTION
    # ========================================================

    reference_result = (
        resolve_current_question(
            question,
            session_id
        )
    )

    resolved_question = (
        reference_result.get(
            "resolved_query",
            question
        )
    )

    if not resolved_question:
        resolved_question = question

    # ========================================================
    # RETRIEVAL
    #
    # No LLM query rewriting.
    #
    # vector_store.retrieve()
    # performs deterministic:
    #
    # crop detection
    # intent detection
    # topic expansion
    # semantic retrieval
    # lexical matching
    # crop matching
    # intent matching
    # topic matching
    # ========================================================

    search_query = resolved_question

    print("=" * 70)
    print(
        "USER QUESTION :",
        question
    )

    print(
        "RESOLVED QUERY:",
        resolved_question
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

        answer = FALLBACK

        save_conversation(
            session_id,
            question,
            answer
        )

        return answer

    print(
        "DOCUMENTS RETRIEVED:",
        len(docs)
    )

    # ========================================================
    # NO RETRIEVED DOCUMENTS
    # ========================================================

    if not docs:

        answer = FALLBACK

        save_conversation(
            session_id,
            question,
            answer
        )

        return answer

    # ========================================================
    # CONTEXT VALIDATION
    # ========================================================

    context = build_validated_context(
        resolved_question,
        docs
    )

    # ========================================================
    # NO VALID CONTEXT
    # ========================================================

    if not context:

        answer = FALLBACK

        save_conversation(
            session_id,
            question,
            answer
        )

        return answer

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

    # BUILD LOCAL QWEN PROMPT

    conversation_history = get_history_text(
        session_id
    )

    prompt = build_answer_prompt(
        question=question,
        resolved_question=resolved_question,
        conversation_history=conversation_history,
        context=context,
    )

    print("=" * 70)
    print(
        "LOCAL QWEN GENERATION"
    )

    print(
        "MODEL: qwen2.5:1.5b"
    )

    print(
        "QUESTION:",
        question
    )

    print("=" * 70)

    # ========================================================
    # GENERATE ANSWER USING OLLAMA
    # ========================================================

    try:

        answer = generate_with_ollama(
            prompt=prompt,
            temperature=0.0
        )

        # ----------------------------------------------------
        # DEBUG RAW LOCAL LLM RESPONSE
        # ----------------------------------------------------

        print("=" * 70)
        print(
            "RAW LOCAL QWEN ANSWER:"
        )

        print(
            repr(answer)
        )

        print("=" * 70)

    except Exception as e:

        print(
            "LOCAL LLM ERROR:",
            e
        )

        answer = FALLBACK

        save_conversation(
            session_id,
            question,
            answer
        )

        return answer

    # ========================================================
    # PHASE 6 - GENERATED ANSWER VALIDATION
    # ========================================================

    answer = clean_response(answer)

    # Model ne question hi repeat kiya?
    if answer.strip().lower() == question.strip().lower():

        print("=" * 70)
        print("GENAI VALIDATION: QUESTION REPEATED")
        print("USING RAG CONTEXT ANSWER")
        print("=" * 70)

        context_answers = re.findall(
            r"Answer:\s*(.*?)(?=\nCategory:|\nLanguage:|\nTopic:|$)",
            context,
            flags=re.DOTALL | re.IGNORECASE,
        )

        if context_answers:
            answer = context_answers[0].strip()
        else:
            answer = FALLBACK

    # ========================================================
    # SAVE CONVERSATION
    # ========================================================

    save_conversation(
        session_id,
        question,
        answer
    )

    # ========================================================
    # FINAL ANSWER
    # ========================================================

    return answer
    
    # ========================================================
    # EMPTY / INVALID ANSWER
    # ========================================================

    if not answer:

        answer = FALLBACK

    # ========================================================
    # SAVE CONVERSATION
    # ========================================================

    save_conversation(
        session_id,
        question,
        answer
    )

    # ========================================================
    # FINAL ANSWER
    # ========================================================

    return answer