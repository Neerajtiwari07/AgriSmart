from services.rag.vector_store import retrieve

docs = retrieve("tamatar")

print("\nRESULT:", len(docs))

for i, doc in enumerate(docs):
    print("\nDOCUMENT", i + 1)
    print(doc.page_content)