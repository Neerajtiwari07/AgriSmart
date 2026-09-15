# ============================================================
# PHASE 5 - RAG 2.0
# CONTEXT VALIDATOR 2.3
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
# GENERIC TOPIC RELATIONSHIPS
# ============================================================

INTENT_TOPIC_RELATIONS = {

    "cultivation": {
    "cultivation": 1.00,
    "sowing": 0.90,
    "season": 0.85,
    "vegetable": 0.85,
    "fruit": 0.85,
    "soil": 0.80,
    "land": 0.75,
    "crop": 0.70,
    "production": 0.70,
    "seed": 0.65,
    "management": 0.60,
    "water": 0.55,
    "irrigation": 0.55,
},

   "sowing": {
    "sowing": 1.00,
    "season": 0.90,
    "cultivation": 0.85,
    "seed": 0.80,
    "transplanting": 0.75,
    "soil": 0.65,
    "land": 0.60,
    "management": 0.55,
},

    "fertilizer": {
        "fertilizer": 1.00,
        "nutrient": 0.90,
        "nutrients": 0.90,
        "INM": 0.85,
        "soil": 0.75,
        "organic": 0.70,
        "management": 0.55,
    },

    "irrigation": {
        "irrigation": 1.00,
        "water": 0.95,
        "drainage": 0.75,
        "soil": 0.60,
        "management": 0.55,
    },

    "weed": {
        "weed": 1.00,
        "management": 0.75,
        "cultivation": 0.60,
        "crop": 0.55,
    },

    "pest": {
        "pest": 1.00,
        "IPM": 0.95,
        "protection": 0.80,
        "disease": 0.65,
        "management": 0.60,
    },

    "disease": {
        "disease": 1.00,
        "problem": 0.90,
        "protection": 0.80,
        "pest": 0.65,
        "management": 0.60,
    },

    "harvest": {
        "harvest": 1.00,
        "postharvest": 0.80,
        "storage": 0.70,
        "production": 0.60,
        "management": 0.55,
    },

    "season": {
        "season": 1.00,
        "sowing": 0.90,
        "cultivation": 0.80,
        "weather": 0.65,
        "climate": 0.55,
    },

    "management": {
        "management": 1.00,
        "cultivation": 0.75,
        "production": 0.65,
        "soil": 0.55,
        "water": 0.55,
        "irrigation": 0.55,
    },

    "crop": {
        "crop": 1.00,
        "cultivation": 0.75,
        "production": 0.65,
        "vegetable": 0.60,
        "fruit": 0.60,
    },
}


# ============================================================
# STOP WORDS
# ============================================================

STOP_WORDS = {
    # English
    "the",
    "is",
    "are",
    "a",
    "an",
    "to",
    "of",
    "in",
    "on",
    "for",
    "how",
    "what",
    "when",
    "why",
    "which",
    "should",
    "does",
    "do",
    "can",
    "be",
    "and",
    "or",
    "with",

    # Hindi
    "में",
    "मे",
    "का",
    "की",
    "के",
    "को",
    "से",
    "पर",
    "और",
    "या",
    "है",
    "हैं",
    "क्या",
    "कैसे",
    "कब",
    "क्यों",
    "कौन",
    "कितना",
    "कितनी",
    "कितने",
    "करें",
    "करना",
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
# TOKENIZATION
# ============================================================

def tokenize(text: str):

    text = normalize_text(text)

    if not text:
        return []

    for char in [
        ",",
        ".",
        "?",
        "!",
        ":",
        ";",
        "(",
        ")",
        "/",
        "-",
    ]:
        text = text.replace(char, " ")

    return [
        token
        for token in text.split()
        if token
    ]


# ============================================================
# MEANINGFUL TOKENS
# ============================================================

def meaningful_tokens(text: str):

    tokens = tokenize(text)

    return [
        token
        for token in tokens
        if token not in STOP_WORDS
        and len(token) >= 2
    ]


# ============================================================
# CROP VALIDATION
# ============================================================

def validate_crop(query_info, doc):

    crop = normalize_text(
        query_info.get("crop")
    )

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

    searchable = " ".join([
        question,
        keywords,
        category
    ])

    if crop in searchable:
        return 1.0

    return 0.0


# ============================================================
# TOPIC VALIDATION
# ============================================================

def validate_topic(query_info, doc):

    intent = normalize_text(
        query_info.get("intent")
    )

    topic = normalize_text(
        doc.metadata.get("topic", "")
    )

    if not intent:

        if topic:
            return 0.5

        return 0.4

    if not topic:
        return 0.0

    relations = INTENT_TOPIC_RELATIONS.get(
        intent,
        {}
    )

    return relations.get(
        topic,
        0.0
    )


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

    if not query:
        return 0.0

    if not question and not answer:
        return 0.0

    query_tokens = meaningful_tokens(query)

    if not query_tokens:
        return 0.0

    question_tokens = set(
        meaningful_tokens(question)
    )

    answer_tokens = set(
        meaningful_tokens(answer)
    )

    question_matches = sum(
        1
        for token in query_tokens
        if token in question_tokens
    )

    answer_matches = sum(
        1
        for token in query_tokens
        if token in answer_tokens
    )

    question_score = (
        question_matches
        / len(query_tokens)
    )

    answer_score = (
        answer_matches
        / len(query_tokens)
    )

    # Question wording is stronger evidence.
    content_score = (
        0.70 * question_score
        + 0.30 * answer_score
    )

    return min(
        1.0,
        content_score
    )


# ============================================================
# EXACT QUESTION MATCH
# ============================================================

def exact_question_match(
    query_info,
    doc
):

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

    if not query or not question:
        return 0.0

    if query == question:
        return 1.0

    return 0.0


# ============================================================
# DOCUMENT VALIDATION
# ============================================================

def exact_question_match(query_info, doc):
    query = normalize_text(
        query_info.get("original_query", "")
    )

    question = normalize_text(
        doc.metadata.get("question", "")
    )

    if not query or not question:
        return 0.0

    query_tokens = tokenize(query)
    question_tokens = tokenize(question)

    if query_tokens == question_tokens:
        return 1.0

    return 0.0

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

    exact_match = exact_question_match(
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
            "exact_match": exact_match,
            "conflict": conflict,
            "reason": "Crop mismatch",
            "document": doc,
        }


    # --------------------------------------------------------
    # TOPIC CONFLICT
    # --------------------------------------------------------

    if conflict:

        return {
            "is_relevant": False,
            "relevance_score": 0.0,
            "crop_score": crop_score,
            "topic_score": topic_score,
            "content_score": content_score,
            "exact_match": exact_match,
            "conflict": True,
            "reason": "Conflicting topic",
            "document": doc,
        }


    # --------------------------------------------------------
    # INTENT VALIDATION
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

    # ----------------------------------------------------
    # Existing topic but unrelated to query intent
    # ----------------------------------------------------

     if topic and topic_score == 0.0:

        return {
            "is_relevant": False,
            "relevance_score": 0.0,
            "crop_score": crop_score,
            "topic_score": topic_score,
            "content_score": content_score,
            "exact_match": exact_match,
            "conflict": False,
            "reason": "Intent-topic mismatch",
            "document": doc,
        }

    # ----------------------------------------------------
    # Existing topic but weakly related to query intent
    #
    # Allow only strong related-topic matches.
    # Example:
    # sowing -> season/cultivation = allowed
    # sowing -> management = rejected
    # weed -> crop = rejected
    # fertilizer -> management = rejected
    # ----------------------------------------------------

    if topic and topic_score < 0.80:

        return {
            "is_relevant": False,
            "relevance_score": 0.0,
            "crop_score": crop_score,
            "topic_score": topic_score,
            "content_score": content_score,
            "exact_match": exact_match,
            "conflict": False,
            "reason": "Weak related topic",
            "document": doc,
        }

    # ----------------------------------------------------
    # Empty topic
    #
    # Allow only if the actual question strongly matches
    # the user query.
    # ----------------------------------------------------

    if not topic:

        if (
            exact_match == 1.0
            or content_score >= 0.70
        ):

            topic_score = 0.50

        else:

            return {
                "is_relevant": False,
                "relevance_score": 0.0,
                "crop_score": crop_score,
                "topic_score": topic_score,
                "content_score": content_score,
                "exact_match": exact_match,
                "conflict": False,
                "reason": "Insufficient evidence for empty topic",
                "document": doc,
            }


    # --------------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------------

    relevance_score = (
        0.40 * crop_score
        + 0.30 * topic_score
        + 0.20 * content_score
        + 0.10 * exact_match
    )


    # --------------------------------------------------------
    # RETRIEVAL SUPPORT
    # --------------------------------------------------------

    if retrieval_score > 0:

        relevance_score = (
            0.90 * relevance_score
            + 0.10 * retrieval_score
        )


    relevance_score = min(
        1.0,
        max(
            0.0,
            relevance_score
        )
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
        "exact_match": exact_match,
        "conflict": False,
        "reason": reason,
        "document": doc,
    }


# ============================================================
# CONTEXT VALIDATION
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
# SIMPLE VALIDITY CHECK
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
# DEBUG TEST
# ============================================================

if __name__ == "__main__":

    from services.rag.loader import (
        load_documents
    )

    from services.rag.query_understanding import (
        understand_query
    )


    documents = load_documents()


    test_queries = [

        "tomato kaise ugaye?",

        "tomato kab lagaye?",

        "गेहूं में खाद कब डालें",

        "धान में खरपतवार कैसे नियंत्रित करें",

        "सरसों की बुवाई कब करें",

        "आलू कब लगाएं",

    ]


    for query in test_queries:

        print("\n")
        print("=" * 80)
        print("QUERY:", query)
        print("=" * 80)


        query_info = understand_query(
            query
        )


        print(
            "CROP:",
            query_info.get("crop")
        )

        print(
            "INTENT:",
            query_info.get("intent")
        )


        count = 0


        for doc in documents:

            result = validate_document(
                query_info,
                doc
            )


            if result["is_relevant"]:

                count += 1


                print("\nDocument:")
                print(
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
                    "Crop Score:",
                    round(
                        result["crop_score"],
                        3
                    )
                )

                print(
                    "Topic Score:",
                    round(
                        result["topic_score"],
                        3
                    )
                )

                print(
                    "Content Score:",
                    round(
                        result["content_score"],
                        3
                    )
                )

                print(
                    "Exact Match:",
                    round(
                        result["exact_match"],
                        3
                    )
                )

                print(
                    "Final:",
                    round(
                        result["relevance_score"],
                        3
                    )
                )

                print(
                    "Reason:",
                    result["reason"]
                )


        print(
            "\nVALID DOCUMENTS:",
            count
        )