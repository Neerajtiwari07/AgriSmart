import csv
import os


INPUT_FILE = "datasets/agri_faq.csv"
OUTPUT_FILE = "datasets/agri_faq_clean.csv"


def clean_row(row):

    # Spaces remove
    row = [x.strip() for x in row]

    # Empty row
    if not any(row):
        return None

    # Header skip
    if row[0].lstrip("\ufeff").strip().lower() == "question":
        return None

    # --------------------------------------------------
    # OLD 4-COLUMN FORMAT
    # Question, Answer, Category, Language
    # --------------------------------------------------

    if len(row) == 4:

        question = row[0]
        answer = row[1]
        category = row[2]
        language = row[3]

        return [
            question,
            "",
            answer,
            category,
            language,
            ""
        ]

    # --------------------------------------------------
    # OLD 2-COLUMN FORMAT
    # Question, Answer
    # --------------------------------------------------

    if len(row) == 2:

        question = row[0]
        answer = row[1]

        return [
            question,
            "",
            answer,
            "General",
            "",
            "general"
        ]

    # --------------------------------------------------
    # BROKEN 6+ COLUMN FORMAT
    #
    # Intended:
    # Question
    # Keywords
    # Answer
    # Category
    # Language
    # Topic
    #
    # Answer may contain commas, creating extra columns.
    # --------------------------------------------------

    if len(row) >= 6:

        question = row[0]
        keywords = row[1]

        # Last 3 fields are fixed
        category = row[-3]
        language = row[-2]
        topic = row[-1]

        # Everything between keywords and last 3 fields
        # belongs to Answer.
        answer_parts = row[2:-3]

        answer = ", ".join(
            part.strip()
            for part in answer_parts
            if part.strip()
        )

        return [
            question,
            keywords,
            answer,
            category,
            language,
            topic
        ]

    # Unknown format
    print("WARNING: Skipping malformed row:", row)
    return None


def main():

    if not os.path.exists(INPUT_FILE):

        raise FileNotFoundError(
            f"Dataset not found: {INPUT_FILE}"
        )

    clean_rows = []

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.reader(file)

        for row_number, row in enumerate(reader, start=1):

            cleaned = clean_row(row)

            if cleaned:
                clean_rows.append(cleaned)

    # --------------------------------------------------
    # WRITE CLEAN DATASET
    # --------------------------------------------------

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Question",
            "Keywords",
            "Answer",
            "Category",
            "Language",
            "Topic"
        ])

        writer.writerows(clean_rows)

    # --------------------------------------------------
    # RESULT
    # --------------------------------------------------

    print()
    print("=" * 70)
    print("DATASET NORMALIZATION SUCCESSFUL")
    print("=" * 70)

    print("INPUT FILE :", INPUT_FILE)
    print("OUTPUT FILE:", OUTPUT_FILE)
    print("ROWS       :", len(clean_rows))

    print("=" * 70)

    # --------------------------------------------------
    # SHOW SAMPLE
    # --------------------------------------------------

    print()
    print("--- FIRST 10 CLEAN RECORDS ---")

    for i, row in enumerate(clean_rows[:10], start=1):

        print()
        print(f"--- Record {i} ---")

        print("Question :", row[0])
        print("Keywords :", row[1])
        print("Answer   :", row[2])
        print("Category :", row[3])
        print("Language :", row[4])
        print("Topic    :", row[5])


if __name__ == "__main__":
    main()