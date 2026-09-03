import csv
import os

from langchain_core.documents import Document


def load_documents():

    file_path = "datasets/agri_faq_clean.csv"

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    documents = []

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=2):

            question = (row.get("Question") or "").strip()
            keywords = (row.get("Keywords") or "").strip()
            answer = (row.get("Answer") or "").strip()
            category = (row.get("Category") or "").strip()
            language = (row.get("Language") or "").strip()
            topic = (row.get("Topic") or "").strip()

            if not question and not answer:
                continue

            page_content = f"""
Question: {question}
Keywords: {keywords}
Answer: {answer}
Category: {category}
Language: {language}
Topic: {topic}
""".strip()

            metadata = {
    "question": question,
    "keywords": keywords,
    "answer": answer,
    "category": category,
    "language": language,
    "topic": topic,
    "row": row_number,
}

            documents.append(
                Document(
                    page_content=page_content,
                    metadata=metadata
                )
            )

    print(f"Loaded {len(documents)} clean documents")

    return documents