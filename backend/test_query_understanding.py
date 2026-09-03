from services.rag.query_understanding import understand_query


queries = [
    "tamatar kab lagaye",
    "tamatar me rog kaise control kare",
    "tomato kaise ugaye",
    "टमाटर में रोग कैसे रोकें",
    "गेहूं में खाद कब डालें",
    "wheat kaise grow kare",
    "धान में खरपतवार कैसे नियंत्रित करें",
    "सरसों की बुवाई कब करें",
    "आलू कब लगाएं",
]


for query in queries:

    result = understand_query(query)

    print("\n" + "=" * 70)
    print("QUERY :", result["original_query"])
    print("CROP  :", result["crop"])
    print("INTENT:", result["intent"])
    print("EXPANDED:", result["expanded_query"])