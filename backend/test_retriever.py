from services.rag.vector_store import retrieve


queries = [
    "tamatar kab lagaye",
    "tamatar me rog kaise control kare",
    "tomato kaise ugaye",
    "टमाटर में रोग कैसे रोकें",
    "गेहूं में खाद कब डालें",
    "wheat kaise grow kare",
    "धान में खरपतवार कैसे नियंत्रित करें",
    "सरसों की बुवाई कब करें",
    "आलू कब लगाएं"
]


for query in queries:

    print("\n" + "=" * 70)
    print("QUERY:", query)
    print("=" * 70)

    docs = retrieve(query)

    print("\nRESULTS:", len(docs))

    for i, doc in enumerate(docs, start=1):

        print(f"\n--- Document {i} ---")
        print("Question:", doc.metadata.get("question"))
        print("Category:", doc.metadata.get("category"))
        print("Topic:", doc.metadata.get("topic"))
        print("Answer:", doc.metadata.get("answer", ""))