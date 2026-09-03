# ============================================================
# PHASE 5 - RAG 2.0
# REFERENCE RESOLVER 1.1
# ============================================================

import re

from services.rag.query_understanding import (
    understand_query
)


# ============================================================
# REFERENCE WORDS
# ============================================================

REFERENCE_WORDS = [
    "isko",
    "isme",
    "isey",
    "ise",
    "iska",
    "iski",
    "iske",
    "ispar",
    "ispe",

    "उसको",
    "उसमें",
    "इसे",
    "इसमे",
    "इसमें",
    "इसका",
    "इसकी",
    "इसके",
    "उसका",
    "उसकी",
    "उसके",
]


# ============================================================
# NORMALIZE
# ============================================================

def normalize_text(text: str):

    if not text:
        return ""

    return " ".join(
        text.lower().strip().split()
    )


# ============================================================
# DETECT REFERENCE
# ============================================================

def detect_reference(query: str):

    query = normalize_text(query)

    if not query:
        return None

    words = query.split()

    for word in words:

        if word in REFERENCE_WORDS:
            return word

    return None


# ============================================================
# REPLACE REFERENCE SAFELY
# ============================================================

def replace_reference(
    query: str,
    reference: str,
    replacement: str
):

    if not query:
        return query

    if not reference:
        return query

    if not replacement:
        return query

    # --------------------------------------------------------
    # Hindi / English exact word replacement
    # --------------------------------------------------------
    #
    # IMPORTANT:
    # We use token/word boundaries instead of simple
    # string replacement.
    #
    # This prevents:
    #
    # ise  → accidentally changing "kaise"
    #
    # --------------------------------------------------------

    pattern = (
        r"(?<!\w)"
        + re.escape(reference)
        + r"(?!\w)"
    )

    return re.sub(
        pattern,
        replacement,
        query,
        flags=re.IGNORECASE
    )


# ============================================================
# RESOLVE REFERENCE
# ============================================================

def resolve_reference(
    current_query: str,
    previous_query: str = ""
):

    current_query = (
        current_query or ""
    ).strip()

    previous_query = (
        previous_query or ""
    ).strip()

    # --------------------------------------------------------
    # Empty query
    # --------------------------------------------------------

    if not current_query:

        return {
            "original_query": "",
            "resolved_query": "",
            "reference": None,
            "crop": None,
            "intent": None,
            "resolved": False,
        }

    # --------------------------------------------------------
    # Understand current query
    # --------------------------------------------------------

    current_info = understand_query(
        current_query
    )

    current_crop = current_info.get(
        "crop"
    )

    current_intent = current_info.get(
        "intent"
    )

    reference = detect_reference(
        current_query
    )

    # --------------------------------------------------------
    # No reference
    # --------------------------------------------------------

    if not reference:

        return {
            "original_query": current_query,
            "resolved_query": current_query,
            "reference": None,
            "crop": current_crop,
            "intent": current_intent,
            "resolved": False,
        }

    # --------------------------------------------------------
    # No previous query
    # --------------------------------------------------------

    if not previous_query:

        return {
            "original_query": current_query,
            "resolved_query": current_query,
            "reference": reference,
            "crop": current_crop,
            "intent": current_intent,
            "resolved": False,
        }

    # --------------------------------------------------------
    # Understand previous query
    # --------------------------------------------------------

    previous_info = understand_query(
        previous_query
    )

    previous_crop = previous_info.get(
        "crop"
    )

    # --------------------------------------------------------
    # Previous crop unavailable
    # --------------------------------------------------------

    if not previous_crop:

        return {
            "original_query": current_query,
            "resolved_query": current_query,
            "reference": reference,
            "crop": current_crop,
            "intent": current_intent,
            "resolved": False,
        }

    # --------------------------------------------------------
    # SAFE REFERENCE REPLACEMENT
    # --------------------------------------------------------

    resolved_query = replace_reference(
        current_query,
        reference,
        previous_crop
    )

    # --------------------------------------------------------
    # Re-understand resolved query
    # --------------------------------------------------------

    resolved_info = understand_query(
        resolved_query
    )

    return {
        "original_query": current_query,
        "resolved_query": resolved_query,
        "reference": reference,
        "crop": resolved_info.get(
            "crop"
        ),
        "intent": resolved_info.get(
            "intent"
        ),
        "resolved": True,
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_cases = [

        (
            "tamatar kaise ugaye?",
            "isko kab lagaye?"
        ),

        (
            "tamatar kaise ugaye?",
            "isme rog kaise control kare?"
        ),

        (
            "wheat kaise grow kare?",
            "isko kab lagaye?"
        ),

        (
            "गेहूं की खेती कैसे करें?",
            "इसमें खाद कब डालें?"
        ),

        (
            "धान की खेती कैसे करें?",
            "इसमें खरपतवार कैसे नियंत्रित करें?"
        ),

        (
            "tomato kaise ugaye?",
            "tomato me rog kaise control kare?"
        ),

        (
            "आलू की खेती कैसे करें?",
            "इसमें सिंचाई कब करें?"
        ),

        (
            "सरसों की खेती कैसे करें?",
            "इसकी बुवाई कब करें?"
        ),

    ]

    for previous, current in test_cases:

        result = resolve_reference(
            current_query=current,
            previous_query=previous
        )

        print("\n")
        print("=" * 70)

        print(
            "PREVIOUS :",
            previous
        )

        print(
            "CURRENT  :",
            current
        )

        print("-" * 70)

        print(
            "REFERENCE:",
            result["reference"]
        )

        print(
            "CROP     :",
            result["crop"]
        )

        print(
            "INTENT   :",
            result["intent"]
        )

        print(
            "RESOLVED :",
            result["resolved"]
        )

        print(
            "QUERY    :",
            result["resolved_query"]
        )

        print("=" * 70)