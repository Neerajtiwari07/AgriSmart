from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from services.rag.loader import load_documents
from services.rag.query_understanding import understand_query


# ============================================================
# PHASE 5 - RAG 2.0
# TOPIC-AWARE HYBRID RETRIEVAL
# ============================================================


# ============================================================
# EMBEDDING MODEL
# ============================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


# ============================================================
# LOAD FAISS DATABASE
# ============================================================

db = FAISS.load_local(
    "vector_db/faiss_index",
    embedding_model,
    allow_dangerous_deserialization=True,
)


# ============================================================
# LOAD ALL CLEAN DOCUMENTS
# ============================================================

all_documents = load_documents()


# ============================================================
# SETTINGS
# ============================================================

SEMANTIC_K = 20
FINAL_K = 5


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:

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
        ",", ".", "?", "!", ":",
        ";", "(", ")", "/"
    ]:
        text = text.replace(char, " ")

    return [
        token
        for token in text.split()
        if token
    ]


# ============================================================
# CROP SCORE
# ============================================================

def crop_score(crop, doc):

    if not crop:
        return 0.0

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

    crop = normalize_text(crop)

    if crop in searchable:
        return 1.0

    return 0.0


# ============================================================
# INTENT SCORE
# ============================================================

def intent_score(intent, doc):

    if not intent:
        return 0.0

    topic = normalize_text(
        doc.metadata.get("topic", "")
    )

    if intent in topic:
        return 1.0

    return 0.0


# ============================================================
# RELATED TOPIC SCORE
# ============================================================

def related_topic_score(
    related_topics,
    doc
):

    if not related_topics:
        return 0.0

    topic = normalize_text(
        doc.metadata.get("topic", "")
    )

    if not topic:
        return 0.0

    # Exact primary topic
    if topic == normalize_text(
        related_topics[0]
    ):
        return 1.0

    # Other related topics
    for index, related_topic in enumerate(
        related_topics[1:],
        start=1
    ):

        related_topic = normalize_text(
            related_topic
        )

        if related_topic == topic:

            # Slightly lower score for secondary topics
            return max(
                0.5,
                0.9 - (index * 0.1)
            )

    return 0.0


# ============================================================
# LEXICAL SCORE
# ============================================================

def lexical_score(query, doc):

    query_tokens = set(
        tokenize(query)
    )

    if not query_tokens:
        return 0.0

    question = normalize_text(
        doc.metadata.get("question", "")
    )

    keywords = normalize_text(
        doc.metadata.get("keywords", "")
    )

    category = normalize_text(
        doc.metadata.get("category", "")
    )

    topic = normalize_text(
        doc.metadata.get("topic", "")
    )

    searchable = " ".join([
        question,
        keywords,
        category,
        topic
    ])

    matched = 0

    for token in query_tokens:

        if token in searchable:
            matched += 1

    return matched / len(query_tokens)


# ============================================================
# SEMANTIC SCORE NORMALIZATION
# ============================================================

def normalize_semantic_scores(results):

    if not results:
        return {}

    distances = [
        distance
        for _, distance in results
    ]

    min_distance = min(distances)
    max_distance = max(distances)

    scores = {}

    for doc, distance in results:

        key = (
            doc.metadata.get("row")
            or doc.metadata.get("question")
        )

        if max_distance == min_distance:

            score = 1.0

        else:

            score = (
                max_distance - distance
            ) / (
                max_distance - min_distance
            )

        scores[key] = max(
            0.0,
            min(1.0, score)
        )

    return scores


# ============================================================
# MAIN RETRIEVAL
# ============================================================

def retrieve(question: str):

    if not question or not question.strip():
        return []

    question = question.strip()

    try:

        # ====================================================
        # STEP 1: QUERY UNDERSTANDING
        # ====================================================

        query_info = understand_query(
            question
        )

        crop = query_info["crop"]

        intent = query_info["intent"]

        related_topics = query_info[
            "related_topics"
        ]

        expanded_query = query_info[
            "expanded_query"
        ]


        print("=" * 70)

        print("QUERY UNDERSTANDING")

        print(
            "Original :",
            question
        )

        print(
            "Crop     :",
            crop
        )

        print(
            "Intent   :",
            intent
        )

        print(
            "Topics   :",
            related_topics
        )

        print(
            "Expanded :",
            expanded_query
        )

        print("=" * 70)


        # ====================================================
        # STEP 2: SEMANTIC SEARCH
        # ====================================================

        semantic_results = (
            db.similarity_search_with_score(
                expanded_query,
                k=SEMANTIC_K
            )
        )


        semantic_scores = (
            normalize_semantic_scores(
                semantic_results
            )
        )


        # ====================================================
        # STEP 3: CREATE CANDIDATES
        # ====================================================

        candidates = {}


        # FAISS candidates
        for doc, distance in semantic_results:

            key = (
                doc.metadata.get("row")
                or doc.metadata.get("question")
            )

            candidates[key] = {

                "doc": doc,

                "distance": distance,

                "semantic":
                    semantic_scores.get(
                        key,
                        0.0
                    )
            }


        # ====================================================
        # STEP 4: LEXICAL + METADATA CANDIDATES
        # ====================================================

        for doc in all_documents:

            key = (
                doc.metadata.get("row")
                or doc.metadata.get("question")
            )

            lex = lexical_score(
                question,
                doc
            )

            crop_match = crop_score(
                crop,
                doc
            )

            intent_match = intent_score(
                intent,
                doc
            )

            topic_match = related_topic_score(
                related_topics,
                doc
            )


            if (
                lex > 0
                or crop_match > 0
                or intent_match > 0
                or topic_match > 0
            ):

                if key not in candidates:

                    candidates[key] = {

                        "doc": doc,

                        "distance": None,

                        "semantic": 0.0
                    }


        # ====================================================
        # STEP 5: FINAL RANKING
        # ====================================================

        ranked = []


        for item in candidates.values():

            doc = item["doc"]


            semantic = item.get(
                "semantic",
                0.0
            )


            lex = lexical_score(
                question,
                doc
            )


            crop_match = crop_score(
                crop,
                doc
            )


            intent_match = intent_score(
                intent,
                doc
            )


            topic_match = related_topic_score(
                related_topics,
                doc
            )


            # =================================================
            # FINAL SCORE
            # =================================================

            final_score = (

                0.25 * semantic

                +

                0.15 * lex

                +

                0.30 * crop_match

                +

                0.20 * intent_match

                +

                0.10 * topic_match
            )


            item["lexical"] = lex

            item["crop"] = crop_match

            item["intent"] = intent_match

            item["topic"] = topic_match

            item["final"] = final_score


            ranked.append(item)


        # ====================================================
        # STEP 6: SORT
        # ====================================================

        ranked.sort(
            key=lambda x: x["final"],
            reverse=True
        )


        # ====================================================
        # STEP 7: FINAL RESULTS
        # ====================================================

        final_documents = []


        print("=" * 70)

        print(
            "TOPIC-AWARE HYBRID RETRIEVAL"
        )

        print(
            "QUERY:",
            question
        )

        print(
            "CROP:",
            crop
        )

        print(
            "INTENT:",
            intent
        )

        print(
            "CANDIDATES:",
            len(ranked)
        )

        print("=" * 70)


        for i, item in enumerate(
            ranked[:FINAL_K],
            start=1
        ):

            doc = item["doc"]


            print(
                f"\n--- Document {i} ---"
            )


            print(
                "Semantic :",
                round(
                    item["semantic"],
                    4
                )
            )


            print(
                "Lexical  :",
                round(
                    item["lexical"],
                    4
                )
            )


            print(
                "Crop     :",
                round(
                    item["crop"],
                    4
                )
            )


            print(
                "Intent   :",
                round(
                    item["intent"],
                    4
                )
            )


            print(
                "Topic    :",
                round(
                    item["topic"],
                    4
                )
            )


            print(
                "FINAL    :",
                round(
                    item["final"],
                    4
                )
            )


            print(
                "Question :",
                doc.metadata.get(
                    "question",
                    ""
                )
            )


            print(
                "Category :",
                doc.metadata.get(
                    "category",
                    ""
                )
            )


            print(
                "Topic    :",
                doc.metadata.get(
                    "topic",
                    ""
                )
            )


            final_documents.append(
                doc
            )


        print("=" * 70)


        return final_documents


    except Exception as e:

        print("=" * 70)

        print(
            "RETRIEVAL ERROR:",
            e
        )

        print("=" * 70)

        return []