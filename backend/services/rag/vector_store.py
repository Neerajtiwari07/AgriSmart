from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ============================================================
# EMBEDDING MODEL
# ============================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


# ============================================================
# LOAD FAISS
# ============================================================

db = FAISS.load_local(
    "vector_db/faiss_index",
    embedding_model,
    allow_dangerous_deserialization=True,
)


# ============================================================
# RETRIEVER
# ============================================================

retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 15,
        "lambda_mult": 0.7,
    },
)


# ============================================================
# RETRIEVE
# ============================================================

def retrieve(question: str):

    if not question or not question.strip():
        return []

    question = question.strip()

    try:

        docs = retriever.invoke(question)

        print("=" * 70)
        print("RETRIEVAL QUERY :", question)
        print("DOCUMENTS FOUND :", len(docs))
        print("=" * 70)

        for i, doc in enumerate(docs, start=1):

            print(f"\n--- Document {i} ---")

            print(
                doc.page_content[:700]
            )

        print("=" * 70)

        return docs

    except Exception as e:

        print("=" * 70)
        print("VECTOR SEARCH ERROR:", e)
        print("=" * 70)

        return []