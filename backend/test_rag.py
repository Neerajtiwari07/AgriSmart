from services.rag.rag_chain import ask_rag

question = "Best fertilizer for wheat"

answer = ask_rag(question)

print()

print(answer)