# ============================================================
# PHASE 5 - RAG 2.0
# CONTEXT VALIDATOR 2.1
# ============================================================

MIN_RELEVANCE_SCORE = 0.50


# ============================================================
# INTENT CONFLICTS
# ============================================================

INTENT_CONFLICTS = {
    "sowing": [
        "harvest",
        "disease",
        "pest",
        "fertilizer",
        "weed",
        "irrigation",
    ],

    "harvest": [
        "sowing",
        "disease",
        "pest",
        "fertilizer",
        "weed",
        "irrigation",
    ],

    "fertilizer": [
        "harvest",
        "sowing",
        "disease",
        "pest",
        "weed",
        "irrigation",
    ],

    "irrigation": [
        "harvest",
        "sowing",
        "disease",
        "pest",
        "fertilizer",
        "weed",
    ],

    "weed": [
        "harvest",
        "sowing",
        "fertilizer",
        "irrigation",
    ],

    "pest": [
        "harvest",
        "sowing",
        "fertilizer",
        "irrigation",
        "weed",
    ],

    "disease": [
        "harvest",
        "sowing",
        "fertilizer",
        "irrigation",
        "weed",
    ],
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text: str):
    if not text:
        return ""

    return " ".join(
        text.lower().strip().split()
    )


# ============================================================
# CROP VALIDATION
# ============================================================

def validate_crop(query_info, doc):

    crop = normalize_text(
        query_info.get("crop")
    )

    # Agar query mein crop detect nahi hua
    # to crop validation neutral rahega.
    if not crop:
        return 0.5

    question = normalize_text(
        doc.metadata.get("question", "")
    )

    keywords = normalize_text(
        doc.metadata.get("keywords", "")
    )

    category = normalize_text(
        doc.metadata.get("category", "")
    )

    searchable = " ".join(
        [
            question,
            keywords,
            category,
        ]
    )

    if crop in searchable:
        return 1.0

    return 0.0


# ============================================================
# TOPIC / INTENT VALIDATION
# ============================================================

def validate_topic(query_info, doc):

    intent = normalize_text(
        query_info.get("intent")
    )

    related_topics = query_info.get(
        "related_topics",
        []
    )

    topic = normalize_text(
        doc.metadata.get("topic", "")
    )

    # Query mein intent nahi mila
    if not intent:

        if topic:
            return 0.5

        return 0.4

    # Exact intent match
    if topic == intent:
        return 1.0

    # Related topic match
    for index, related_topic in enumerate(
        related_topics
    ):

        related_topic = normalize_text(
            related_topic
        )

        if topic == related_topic:

            if index == 0:
                return 1.0

            return max(
                0.5,
                0.9 - (index * 0.1)
            )

    # IMPORTANT:
    # Explicitly unrelated / missing topic
    return 0.0


# ============================================================
# STRICT TOPIC MATCH
# ============================================================

def strict_topic_match(query_info, doc):

    intent = normalize_text(
        query_info.get("intent")
    )

    topic = normalize_text(
        doc.metadata.get("topic", "")
    )

    if not intent:
        return True

    # Topic missing hai
    if not topic:
        return False

    # Exact intent required
    if topic == intent:
        return True

    return False


# ============================================================
# TOPIC CONFLICT
# ============================================================

def topic_conflict(query_info, doc):

    intent = normalize_text(
        query_info.get("intent")
    )

    topic = normalize_text(
        doc.metadata.get("topic", "")
    )

    if not intent or not topic:
        return False

    conflicts = INTENT_CONFLICTS.get(
        intent,
        []
    )

    return topic in conflicts


# ============================================================
# CONTENT VALIDATION
# ============================================================

def validate_content(query_info, doc):

    query = normalize_text(
        query_info.get(
            "original_query",
            ""
        )
    )

    question = normalize_text(
        doc.metadata.get(
            "question",
            ""
        )
    )

    answer = normalize_text(
        doc.metadata.get(
            "answer",
            ""
        )
    )

    if not question and not answer:
        return 0.0

    query_words = set(
        query.split()
    )

    if not query_words:
        return 0.0

    document_text = (
        question
        + " "
        + answer
    )

    matched = 0

    for word in query_words:

        if len(word) < 2:
            continue

        if word in document_text:
            matched += 1

    usable_words = [
        word
        for word in query_words
        if len(word) >= 2
    ]

    if not usable_words:
        return 0.0

    return min(
        1.0,
        matched / len(usable_words)
    )


# ============================================================
# DOCUMENT VALIDATION
# ============================================================

def validate_document(
    query_info,
    doc,
    retrieval_score=0.0
):

    crop_score = validate_crop(
        query_info,
        doc
    )

    topic_score = validate_topic(
        query_info,
        doc
    )

    content_score = validate_content(
        query_info,
        doc
    )

    conflict = topic_conflict(
        query_info,
        doc
    )

    # --------------------------------------------------------
    # CROP MISMATCH
    # --------------------------------------------------------

    query_crop = query_info.get(
        "crop"
    )

    if (
        query_crop
        and crop_score == 0.0
    ):

        return {
            "is_relevant": False,
            "relevance_score": 0.0,
            "crop_score": crop_score,
            "topic_score": topic_score,
            "content_score": content_score,
            "conflict": conflict,
            "reason": "Crop mismatch",
            "document": doc,
        }

    # --------------------------------------------------------
    # CONFLICTING TOPIC
    # --------------------------------------------------------

    if conflict:

        return {
            "is_relevant": False,
            "relevance_score": 0.0,
            "crop_score": crop_score,
            "topic_score": topic_score,
            "content_score": content_score,
            "conflict": True,
            "reason": "Conflicting topic",
            "document": doc,
        }

    # --------------------------------------------------------
    # STRICT INTENT VALIDATION
    # --------------------------------------------------------

    intent = query_info.get(
        "intent"
    )

    topic = normalize_text(
        doc.metadata.get(
            "topic",
            ""
        )
    )

    if intent:

        # Agar document ka topic missing hai
        # aur query specific intent wali hai,
        # document ko reject karenge.
        if not topic:

            return {
                "is_relevant": False,
                "relevance_score": 0.0,
                "crop_score": crop_score,
                "topic_score": topic_score,
                "content_score": content_score,
                "conflict": False,
                "reason": "Missing topic for specific intent",
                "document": doc,
            }

        # Exact intent match required
        if not strict_topic_match(
            query_info,
            doc
        ):

            return {
                "is_relevant": False,
                "relevance_score": 0.0,
                "crop_score": crop_score,
                "topic_score": topic_score,
                "content_score": content_score,
                "conflict": False,
                "reason": "Intent mismatch",
                "document": doc,
            }

    # --------------------------------------------------------
    # FINAL RELEVANCE SCORE
    # --------------------------------------------------------

    relevance_score = (
        0.45 * crop_score
        + 0.40 * topic_score
        + 0.15 * content_score
    )

    if retrieval_score > 0:

        relevance_score = (
            0.85 * relevance_score
            + 0.15 * retrieval_score
        )

    is_relevant = (
        relevance_score
        >= MIN_RELEVANCE_SCORE
    )

    reason = (
        "Relevant context"
        if is_relevant
        else "Low relevance"
    )

    return {
        "is_relevant": is_relevant,
        "relevance_score": relevance_score,
        "crop_score": crop_score,
        "topic_score": topic_score,
        "content_score": content_score,
        "conflict": False,
        "reason": reason,
        "document": doc,
    }


# ============================================================
# VALIDATE COMPLETE CONTEXT
# ============================================================

def validate_context(
    query,
    documents
):

    if not query or not documents:
        return []

    from services.rag.query_understanding import (
        understand_query
    )

    query_info = understand_query(
        query
    )

    validated = []

    for doc in documents:

        result = validate_document(
            query_info,
            doc
        )

        if result["is_relevant"]:
            validated.append(
                result
            )

    validated.sort(
        key=lambda item:
        item["relevance_score"],
        reverse=True
    )

    return validated


# ============================================================
# CHECK WHETHER VALID CONTEXT EXISTS
# ============================================================

def has_valid_context(
    query,
    documents
):

    return bool(
        validate_context(
            query,
            documents
        )
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    from services.rag.vector_store import retrieve

    test_queries = [
        "गेहूं में खाद कब डालें",
        "धान में खरपतवार कैसे नियंत्रित करें",
        "सरसों की बुवाई कब करें",
        "आलू कब लगाएं",
        "tamatar me rog kaise control kare",
    ]

    for query in test_queries:

        print("\n")
        print("=" * 70)
        print("TEST QUERY:")
        print(query)
        print("=" * 70)

        documents = retrieve(
            query
        )

        validated = validate_context(
            query,
            documents
        )

        print("\nVALIDATED DOCUMENTS:")

        for index, item in enumerate(
            validated,
            start=1
        ):

            doc = item["document"]

            print(
                f"\n--- Document {index} ---"
            )

            print(
                "Question:",
                doc.metadata.get(
                    "question",
                    ""
                )
            )

            print(
                "Category:",
                doc.metadata.get(
                    "category",
                    ""
                )
            )

            print(
                "Topic:",
                doc.metadata.get(
                    "topic",
                    ""
                )
            )

            print(
                "Score:",
                round(
                    item["relevance_score"],
                    4
                )
            )

            print(
                "Reason:",
                item["reason"]
            )

        print("\n")