from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from services.rag.loader import load_documents

import os
import shutil


# ============================================================
# LOAD DOCUMENTS
# ============================================================

documents = load_documents()

print("=" * 70)
print("TOTAL DOCUMENTS:", len(documents))
print("=" * 70)


# ============================================================
# SHOW DOCUMENTS
# ============================================================

for i, doc in enumerate(documents):

    print(f"\n--- Document {i + 1} ---")
    print(doc.page_content[:500])


# ============================================================
# EMBEDDING MODEL
# ============================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


# ============================================================
# DELETE OLD FAISS INDEX
# ============================================================

index_path = "vector_db/faiss_index"

if os.path.exists(index_path):

    print("\nDeleting old FAISS index...")

    shutil.rmtree(index_path)


# ============================================================
# CREATE NEW FAISS INDEX
# ============================================================

print("\nCreating new FAISS index...")

db = FAISS.from_documents(
    documents,
    embedding_model,
)


# ============================================================
# SAVE INDEX
# ============================================================

db.save_local(index_path)


print("\n" + "=" * 70)
print("FAISS INDEX CREATED SUCCESSFULLY")
print("LOCATION:", index_path)
print("DOCUMENTS:", len(documents))
print("=" * 70)