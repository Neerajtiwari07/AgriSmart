from services.rag.vector_store import retrieve
from services.rag.context_validator import (
    validate_document
)
from services.rag.query_understanding import (
    understand_query
)


# ============================================================
# TEST QUERIES
# ============================================================

queries = [

    "tamatar me rog kaise control kare",

    "गेहूं में खाद कब डालें",

    "धान में खरपतवार कैसे नियंत्रित करें",

    "सरसों की बुवाई कब करें",

    "आलू कब लगाएं",
]


# ============================================================
# RUN TEST
# ============================================================

for query in queries:

    print("\n")
    print("=" * 70)
    print("QUERY:", query)
    print("=" * 70)


    # --------------------------------------------------------
    # Query Understanding
    # --------------------------------------------------------

    query_info = understand_query(
        query
    )


    print(
        "CROP:",
        query_info["crop"]
    )

    print(
        "INTENT:",
        query_info["intent"]
    )


    # --------------------------------------------------------
    # Retrieval
    # --------------------------------------------------------

    documents = retrieve(
        query
    )


    print(
        "\nRETRIEVED:",
        len(documents)
    )


    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    accepted = []
    rejected = []


    for doc in documents:

        result = validate_document(
            query_info,
            doc
        )


        if result["is_relevant"]:

            accepted.append(
                result
            )

        else:

            rejected.append(
                result
            )


    # --------------------------------------------------------
    # ACCEPTED
    # --------------------------------------------------------

    accepted.sort(
        key=lambda x:
            x["relevance_score"],
        reverse=True
    )


    print("\n")
    print("-" * 70)
    print("✅ ACCEPTED CONTEXT")
    print("-" * 70)


    for i, item in enumerate(
        accepted,
        start=1
    ):

        doc = item["document"]


        print(
            f"\n{i}.",
            doc.metadata.get(
                "question",
                ""
            )
        )

        print(
            "   Crop:",
            round(
                item["crop_score"],
                3
            )
        )

        print(
            "   Topic:",
            round(
                item["topic_score"],
                3
            )
        )

        print(
            "   Content:",
            round(
                item["content_score"],
                3
            )
        )

        print(
            "   Score:",
            round(
                item["relevance_score"],
                3
            )
        )

        print(
            "   Reason:",
            item["reason"]
        )


    # --------------------------------------------------------
    # REJECTED
    # --------------------------------------------------------

    print("\n")
    print("-" * 70)
    print("❌ REJECTED CONTEXT")
    print("-" * 70)


    for i, item in enumerate(
        rejected,
        start=1
    ):

        doc = item["document"]


        print(
            f"\n{i}.",
            doc.metadata.get(
                "question",
                ""
            )
        )

        print(
            "   Topic:",
            doc.metadata.get(
                "topic",
                ""
            )
        )

        print(
            "   Reason:",
            item["reason"]
        )


    print("\n" + "=" * 70)