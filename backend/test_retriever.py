from services.rag.vector_store import retrieve

docs = retrieve("Best fertilizer for wheat")

print("=" * 80)

for doc in docs:
    print(doc.page_content)
    print("-" * 80)