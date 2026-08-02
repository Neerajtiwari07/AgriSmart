import os
import sys

# Backend folder ko Python path me add karo
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from services.rag.loader import load_documents

print("Loading documents...")

documents = load_documents()

print("Loading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

print("Creating Vector DB...")

db = FAISS.from_documents(
    documents,
    embeddings
)

# Folder agar na ho to bana do
os.makedirs("vector_db", exist_ok=True)

db.save_local("vector_db/faiss_index")

print("✅ Vector DB Created Successfully")