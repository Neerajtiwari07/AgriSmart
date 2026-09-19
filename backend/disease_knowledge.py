import csv
from pathlib import Path
from typing import Optional, Dict, Any


BASE_DIR = Path(__file__).resolve().parent

KNOWLEDGE_FILE = (
    BASE_DIR
    / "disease_detection"
    / "datasets"
    / "disease_knowledge.csv"
)

# If your multilingual CSV is copied over the existing file,
# this loader will use it automatically.
REQUIRED_COLUMNS = {
    "disease_class",
    "crop",
    "disease_name",
    "symptoms",
    "management",
    "prevention",
    "source",
}


def _load_knowledge():
    if not KNOWLEDGE_FILE.exists():
        raise FileNotFoundError(
            f"Disease knowledge file not found: {KNOWLEDGE_FILE}"
        )

    with open(
        KNOWLEDGE_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError(
                "Disease knowledge CSV has no header."
            )

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)

        if missing:
            raise ValueError(
                f"Missing disease knowledge columns: {sorted(missing)}"
            )

        return list(reader)


_KNOWLEDGE = None


def _ensure_loaded():
    global _KNOWLEDGE

    if _KNOWLEDGE is None:
        _KNOWLEDGE = _load_knowledge()


def get_disease_knowledge(
    disease_class: str,
    language: str = "en"
) -> Optional[Dict[str, Any]]:

    _ensure_loaded()

    target = (
        str(disease_class or "")
        .strip()
        .lower()
    )

    language = (
        str(language or "en")
        .strip()
        .lower()
    )

    if language not in {"en", "hi", "hinglish"}:
        language = "en"

    for row in _KNOWLEDGE:

        current = (
            str(row.get("disease_class", ""))
            .strip()
            .lower()
        )

        if current != target:
            continue

        symptoms_key = "symptoms"
        management_key = "management"
        prevention_key = "prevention"

        if language == "hi":
            symptoms_key = "symptoms_hi"
            management_key = "management_hi"
            prevention_key = "prevention_hi"

        elif language == "hinglish":
            symptoms_key = "symptoms_hinglish"
            management_key = "management_hinglish"
            prevention_key = "prevention_hinglish"

        # Safe fallback to English if a translated column is
        # missing or empty.
        symptoms = (
            row.get(symptoms_key, "").strip()
            or row.get("symptoms", "").strip()
        )

        management = (
            row.get(management_key, "").strip()
            or row.get("management", "").strip()
        )

        prevention = (
            row.get(prevention_key, "").strip()
            or row.get("prevention", "").strip()
        )

        return {
            "disease_class": row.get(
                "disease_class", ""
            ),

            "crop": row.get(
                "crop", ""
            ),

            "disease_name": row.get(
                "disease_name", ""
            ),

            "symptoms": symptoms,

            "management": management,

            "prevention": prevention,

            "source": row.get(
                "source", ""
            ),

            "language": language,
        }

    return None
