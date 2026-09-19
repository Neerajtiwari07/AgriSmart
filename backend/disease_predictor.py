from pathlib import Path
import json

import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import mobilenet_v3_small
from PIL import Image


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = (
    BASE_DIR
    / "disease_detection"
    / "models"
)

DISEASE_MODEL_PATH = (
    MODEL_DIR
    / "disease_model.pth"
)

DISEASE_CLASSES_PATH = (
    MODEL_DIR
    / "class_names.json"
)

CROP_MODEL_PATH = (
    MODEL_DIR
    / "crop_model.pth"
)

CROP_CLASSES_PATH = (
    MODEL_DIR
    / "crop_class_names.json"
)


# ============================================================
# SETTINGS
# ============================================================

IMAGE_SIZE = 224

CONFIDENCE_THRESHOLD = 70.0

CROP_CONFIDENCE_THRESHOLD = 70.0


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


# ============================================================
# IMAGE TRANSFORM
# ============================================================

TRANSFORM = transforms.Compose(
    [
        transforms.Resize(
            (IMAGE_SIZE, IMAGE_SIZE)
        ),

        transforms.ToTensor(),

        transforms.Normalize(
            mean=[
                0.485,
                0.456,
                0.406
            ],
            std=[
                0.229,
                0.224,
                0.225
            ]
        )
    ]
)


# ============================================================
# LOAD CLASS NAMES
# ============================================================

def load_class_names(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# CREATE DISEASE MODEL
# ============================================================

def create_disease_model(
    number_of_classes
):

    model = mobilenet_v3_small(
        weights=None
    )

    in_features = (
        model.classifier[-1].in_features
    )

    model.classifier[-1] = nn.Linear(
        in_features,
        number_of_classes
    )

    return model


# ============================================================
# CREATE CROP MODEL
# ============================================================

def create_crop_model(
    number_of_classes
):

    model = mobilenet_v3_small(
        weights=None
    )

    in_features = (
        model.classifier[-1].in_features
    )

    model.classifier[-1] = nn.Linear(
        in_features,
        number_of_classes
    )

    return model


# ============================================================
# LOAD DISEASE MODEL
# ============================================================

def load_disease_model():

    checkpoint = torch.load(
        DISEASE_MODEL_PATH,
        map_location=DEVICE
    )

    # --------------------------------------------------------
    # Checkpoint format
    # --------------------------------------------------------

    if (
        isinstance(checkpoint, dict)
        and "model_state_dict" in checkpoint
    ):

        class_names = checkpoint.get(
            "class_names"
        )

        if not class_names:

            class_names = load_class_names(
                DISEASE_CLASSES_PATH
            )

        number_of_classes = checkpoint.get(
            "num_classes",
            len(class_names)
        )

        model = create_disease_model(
            number_of_classes
        )

        model.load_state_dict(
            checkpoint[
                "model_state_dict"
            ]
        )

    # --------------------------------------------------------
    # Direct state_dict fallback
    # --------------------------------------------------------

    else:

        class_names = load_class_names(
            DISEASE_CLASSES_PATH
        )

        model = create_disease_model(
            len(class_names)
        )

        model.load_state_dict(
            checkpoint
        )

    model = model.to(
        DEVICE
    )

    model.eval()

    return model, class_names


# ============================================================
# LOAD CROP MODEL
# ============================================================

def load_crop_model():

    checkpoint = torch.load(
        CROP_MODEL_PATH,
        map_location=DEVICE
    )

    # --------------------------------------------------------
    # Checkpoint format
    # --------------------------------------------------------

    if (
        isinstance(checkpoint, dict)
        and "model_state_dict" in checkpoint
    ):

        class_names = checkpoint.get(
            "class_names"
        )

        if not class_names:

            class_names = load_class_names(
                CROP_CLASSES_PATH
            )

        number_of_classes = checkpoint.get(
            "num_classes",
            len(class_names)
        )

        model = create_crop_model(
            number_of_classes
        )

        model.load_state_dict(
            checkpoint[
                "model_state_dict"
            ]
        )

    # --------------------------------------------------------
    # Direct state_dict fallback
    # --------------------------------------------------------

    else:

        class_names = load_class_names(
            CROP_CLASSES_PATH
        )

        model = create_crop_model(
            len(class_names)
        )

        model.load_state_dict(
            checkpoint
        )

    model = model.to(
        DEVICE
    )

    model.eval()

    return model, class_names


# ============================================================
# LOAD BOTH MODELS
# ============================================================

print(
    "Loading disease detection models..."
)

DISEASE_MODEL, DISEASE_CLASS_NAMES = (
    load_disease_model()
)

CROP_MODEL, CROP_CLASS_NAMES = (
    load_crop_model()
)

print(
    "Disease classes:",
    len(DISEASE_CLASS_NAMES)
)

print(
    "Crop classes:",
    len(CROP_CLASS_NAMES)
)

print(
    "Disease detection device:",
    DEVICE
)


# ============================================================
# PREDICT CROP
# ============================================================

def predict_crop(image):

    image_tensor = TRANSFORM(
        image
    ).unsqueeze(
        0
    ).to(
        DEVICE
    )

    with torch.no_grad():

        outputs = CROP_MODEL(
            image_tensor
        )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        top_count = min(
            3,
            len(CROP_CLASS_NAMES)
        )

        values, indices = torch.topk(
            probabilities,
            k=top_count,
            dim=1
        )

    top_crops = []

    for value, index in zip(
        values[0],
        indices[0]
    ):

        top_crops.append(
            {
                "crop": CROP_CLASS_NAMES[
                    index.item()
                ],

                "confidence": round(
                    value.item() * 100,
                    2
                )
            }
        )

    top_crop = top_crops[0]

    return {
        "crop": top_crop[
            "crop"
        ],

        "confidence": top_crop[
            "confidence"
        ],

        "top_crops": top_crops
    }


# ============================================================
# PREDICT DISEASE
# ============================================================

def predict_disease(image_path):

    image = Image.open(
        image_path
    ).convert(
        "RGB"
    )

    # ========================================================
    # CROP PREDICTION
    # ========================================================

    crop_prediction = predict_crop(
        image
    )

    predicted_crop = (
        crop_prediction[
            "crop"
        ]
    )

    crop_confidence = (
        crop_prediction[
            "confidence"
        ]
    )

    top_crops = (
        crop_prediction[
            "top_crops"
        ]
    )

    # ========================================================
    # DISEASE PREDICTION
    # ========================================================

    image_tensor = TRANSFORM(
        image
    ).unsqueeze(
        0
    ).to(
        DEVICE
    )

    with torch.no_grad():

        outputs = DISEASE_MODEL(
            image_tensor
        )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        top_count = min(
            3,
            len(DISEASE_CLASS_NAMES)
        )

        values, indices = torch.topk(
            probabilities,
            k=top_count,
            dim=1
        )

    top_predictions = []

    for value, index in zip(
        values[0],
        indices[0]
    ):

        class_name = (
            DISEASE_CLASS_NAMES[
                index.item()
            ]
        )

        confidence = (
            value.item() * 100
        )

        top_predictions.append(
            {
                "class_name": class_name,

                "confidence": round(
                    confidence,
                    2
                )
            }
        )

    # ========================================================
    # TOP DISEASE
    # ========================================================

    top_prediction = (
        top_predictions[0]
    )

    disease_class = (
        top_prediction[
            "class_name"
        ]
    )

    disease_confidence = (
        top_prediction[
            "confidence"
        ]
    )

    # ========================================================
    # EXTRACT CROP FROM DISEASE CLASS
    # ========================================================

    if "___" in disease_class:

        disease_crop = (
            disease_class.split(
                "___",
                1
            )[0]
        )

    else:

        disease_crop = disease_class

    # ========================================================
    # CROP / DISEASE CONSISTENCY
    # ========================================================

    crop_matches_disease = (
        predicted_crop.lower()
        == disease_crop.lower()
    )

    # ========================================================
    # FINAL CONFIDENCE
    # ========================================================

    is_confident = (
        disease_confidence
        >= CONFIDENCE_THRESHOLD

        and

        crop_confidence
        >= CROP_CONFIDENCE_THRESHOLD

        and

        crop_matches_disease
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {

        "class_name": disease_class,

        "confidence": disease_confidence,

        "is_confident": is_confident,

        "top_predictions": top_predictions,

        "predicted_crop": predicted_crop,

        "crop_confidence": crop_confidence,

        "top_crops": top_crops,

        "disease_crop": disease_crop,

        "crop_matches_disease": (
            crop_matches_disease
        ),

        "confidence_threshold": (
            CONFIDENCE_THRESHOLD
        ),

        "crop_confidence_threshold": (
            CROP_CONFIDENCE_THRESHOLD
        )
    }