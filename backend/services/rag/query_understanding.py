import re


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text: str) -> str:

    if not text:
        return ""

    return " ".join(
        text.lower().strip().split()
    )


# ============================================================
# TOKENIZE
# ============================================================

def tokenize(text: str):

    text = normalize_text(text)

    if not text:
        return []

    text = re.sub(
        r"[,\.\?\!\:\;\(\)/]",
        " ",
        text
    )

    return [
        token
        for token in text.split()
        if token
    ]


# ============================================================
# CROP ALIASES
# ============================================================

CROP_ALIASES = {

    "tomato": [
        "tomato",
        "tamatar",
        "टमाटर",
    ],

    "wheat": [
        "wheat",
        "गेहूं",
        "गेंहू",
    ],

    "rice": [
        "rice",
        "paddy",
        "धान",
        "चावल",
    ],

    "potato": [
        "potato",
        "aloo",
        "आलू",
    ],

    "mustard": [
        "mustard",
        "sarson",
        "सरसों",
    ],

    "soybean": [
        "soybean",
        "soya",
        "सोयाबीन",
    ],

    "maize": [
        "maize",
        "corn",
        "मक्का",
    ],

    "guava": [
        "guava",
        "amrud",
        "अमरूद",
    ],

    "onion": [
        "onion",
        "pyaz",
        "प्याज",
    ],

    "papaya": [
        "papaya",
        "papita",
        "पपीता",
    ],

    "chickpea": [
        "chickpea",
        "gram",
        "चना",
    ],
}


# ============================================================
# INTENT / TOPIC ALIASES
# ============================================================

INTENT_ALIASES = {

    "sowing": [
        "sowing",
        "sow",
        "plant",
        "planting",
        "lagaye",
        "lagayen",
        "lagana",
        "बुवाई",
        "बोना",
        "लगाएं",
        "लगाये",
        "कब लगाएं",
    ],

    "fertilizer": [
        "fertilizer",
        "fertiliser",
        "fertilize",
        "khad",
        "खाद",
        "उर्वरक",
    ],

    "weed": [
        "weed",
        "weeds",
        "weeding",
        "weed control",
        "khap",
        "khpatwar",
        "खरपतवार",
        "निराई",
        "खरपतवारनाशी",
    ],

    "disease": [
        "disease",
        "diseases",
        "rog",
        "रोग",
        "बीमारी",
        "झुलसा",
        "blight",
        "virus",
    ],

    "irrigation": [
        "irrigation",
        "water",
        "pani",
        "सिंचाई",
        "पानी",
    ],

    "cultivation": [
        "cultivation",
        "cultivate",
        "grow",
        "growing",
        "kaise ugaye",
        "kaise ugayen",
        "ugana",
        "उगाएं",
        "उगाये",
        "खेती",
    ],

    "season": [
        "season",
        "samay",
        "मौसम",
        "ऋतु",
        "कब",
    ],

    "pest": [
        "pest",
        "insect",
        "कीट",
        "कीड़ा",
        "माहू",
    ],

    "harvest": [
        "harvest",
        "harvesting",
        "khudai",
        "खुदाई",
        "कटाई",
        "निकालना",
    ],

    "management": [
        "management",
        "care",
        "देखभाल",
        "प्रबंधन",
    ],

    "crop": [
        "what is",
        "kya hai",
        "क्या है",
    ],
}


# ============================================================
# INTENT → RELATED DATASET TOPICS
# ============================================================

INTENT_TOPIC_MAP = {

    # User asks when to plant/sow
    "sowing": [
        "sowing",
        "season",
        "cultivation",
        "transplanting",
    ],

    # User asks how to grow
    "cultivation": [
        "cultivation",
        "season",
        "management",
        "land",
        "soil",
    ],

    # Fertilizer questions
    "fertilizer": [
        "fertilizer",
    ],

    # Weed questions
    "weed": [
        "weed",
    ],

    # Disease questions
    "disease": [
        "disease",
        "problem",
    ],

    # Water questions
    "irrigation": [
        "irrigation",
        "water",
    ],

    # Pest questions
    "pest": [
        "pest",
        "disease",
    ],

    # Harvest questions
    "harvest": [
        "harvest",
    ],

    # General crop management
    "management": [
        "management",
    ],

    # Season questions
    "season": [
        "season",
        "sowing",
        "cultivation",
    ],

    # Basic crop information
    "crop": [
        "crop",
        "basic",
    ],
}


# ============================================================
# DETECT CROP
# ============================================================

def detect_crop(query: str):

    query = normalize_text(query)

    matches = []

    for crop, aliases in CROP_ALIASES.items():

        for alias in aliases:

            alias = normalize_text(alias)

            if alias and alias in query:

                matches.append(
                    (
                        crop,
                        len(alias)
                    )
                )

    if not matches:
        return None

    # Prefer longest matching alias
    matches.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return matches[0][0]


# ============================================================
# DETECT INTENT
# ============================================================

def detect_intent(query: str):

    query = normalize_text(query)

    scores = {}

    for intent, aliases in INTENT_ALIASES.items():

        score = 0

        for alias in aliases:

            alias = normalize_text(alias)

            if alias and alias in query:

                score += len(alias)

        if score > 0:

            scores[intent] = score

    if not scores:
        return None

    return max(
        scores,
        key=scores.get
    )


# ============================================================
# GET RELATED TOPICS
# ============================================================

def get_related_topics(intent: str):

    if not intent:
        return []

    return INTENT_TOPIC_MAP.get(
        intent,
        [intent]
    )


# ============================================================
# QUERY UNDERSTANDING
# ============================================================

def understand_query(query: str):

    query = query.strip()

    if not query:

        return {
            "original_query": "",
            "crop": None,
            "intent": None,
            "related_topics": [],
            "expanded_query": "",
        }

    # --------------------------------------------------------
    # Detect crop
    # --------------------------------------------------------

    crop = detect_crop(query)

    # --------------------------------------------------------
    # Detect intent
    # --------------------------------------------------------

    intent = detect_intent(query)

    # --------------------------------------------------------
    # Related dataset topics
    # --------------------------------------------------------

    related_topics = get_related_topics(
        intent
    )

    # --------------------------------------------------------
    # Build expanded query
    # --------------------------------------------------------

    parts = [
        query
    ]

    if crop:
        parts.append(crop)

    if intent:
        parts.append(intent)

    # Add related topics for semantic retrieval
    for topic in related_topics:

        if topic not in parts:

            parts.append(topic)

    expanded_query = " ".join(
        parts
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    return {

        "original_query": query,

        "crop": crop,

        "intent": intent,

        "related_topics": related_topics,

        "expanded_query": expanded_query,
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_queries = [

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

    for query in test_queries:

        result = understand_query(
            query
        )

        print("\n" + "=" * 70)

        print(
            "QUERY :",
            result["original_query"]
        )

        print(
            "CROP  :",
            result["crop"]
        )

        print(
            "INTENT:",
            result["intent"]
        )

        print(
            "TOPICS:",
            result["related_topics"]
        )

        print(
            "EXPANDED:",
            result["expanded_query"]
        )