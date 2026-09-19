import os
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, Form, UploadFile

from disease_predictor import predict_disease
from disease_knowledge import get_disease_knowledge
from services.disease_quality import check_image_quality
from services.disease_safety import evaluate_prediction


router = APIRouter(
    prefix="/detect-disease",
    tags=["Disease Detection"]
)


@router.post("")
async def detect_disease(
    file: UploadFile = File(...),
    language: str = Form("en")
):

    temp_path = None

    try:
        language = (
            language or "en"
        ).lower().strip()

        if language not in {
            "en",
            "hi",
            "hinglish"
        }:
            language = "en"

        suffix = (
            Path(file.filename).suffix
            or ".jpg"
        )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(
                await file.read()
            )

            temp_path = temp_file.name

        quality = check_image_quality(
            temp_path
        )

        if not quality["valid"]:
            return {
                "success": True,
                "status": "invalid_image",
                "message": quality["message"],
                "recommendation": (
                    "Please upload a clear, well-lit "
                    "image showing a plant leaf."
                )
            }

        prediction = predict_disease(
            temp_path
        )

        disease_class = prediction["class_name"]
        confidence = prediction["confidence"]
        top_predictions = prediction["top_predictions"]

        predicted_crop = prediction["predicted_crop"]
        crop_confidence = prediction["crop_confidence"]
        top_crops = prediction["top_crops"]

        disease_crop = prediction["disease_crop"]
        crop_matches_disease = prediction[
            "crop_matches_disease"
        ]

        safety = evaluate_prediction(
            prediction
        )

        safety_status = safety["status"]

        # Crop/disease mismatch must always stop
        # before showing a confirmed disease result.
        if not crop_matches_disease:

            return {
                "success": True,
                "status": "review_required",
                "disease": disease_class,
                "confidence": f"{confidence:.2f}%",
                "crop": predicted_crop,
                "crop_confidence": (
                    f"{crop_confidence:.2f}%"
                ),
                "disease_crop": disease_crop,
                "crop_matches_disease": False,
                "message": (
                    "The crop and disease predictions "
                    "do not match. The AI result requires "
                    "additional review."
                ),
                "reason": (
                    "The crop recognition model and "
                    "disease recognition model produced "
                    "different crop classifications."
                ),
                "recommendation": (
                    "Please upload a clear close-up "
                    "image showing a single plant leaf."
                ),
                "top_predictions": top_predictions,
                "top_crops": top_crops,
                "margin": safety.get("margin", 0.0)
            }

        if safety_status == "uncertain":

            return {
                "success": True,
                "status": "uncertain",
                "disease": disease_class,
                "confidence": f"{confidence:.2f}%",
                "crop": predicted_crop,
                "crop_confidence": (
                    f"{crop_confidence:.2f}%"
                ),
                "disease_crop": disease_crop,
                "crop_matches_disease": True,
                "message": (
                    "The AI could not confidently "
                    "identify this plant disease."
                ),
                "reason": safety["reason"],
                "recommendation": (
                    "Please upload a clear close-up "
                    "image of a single affected leaf."
                ),
                "top_predictions": top_predictions,
                "top_crops": top_crops,
                "margin": safety["margin"]
            }

        if safety_status == "review_required":

            return {
                "success": True,
                "status": "review_required",
                "disease": disease_class,
                "confidence": f"{confidence:.2f}%",
                "crop": predicted_crop,
                "crop_confidence": (
                    f"{crop_confidence:.2f}%"
                ),
                "disease_crop": disease_crop,
                "crop_matches_disease": True,
                "message": (
                    "The AI prediction requires "
                    "additional review."
                ),
                "reason": safety["reason"],
                "recommendation": (
                    "Please upload a clear close-up "
                    "image showing the affected leaf."
                ),
                "top_predictions": top_predictions,
                "top_crops": top_crops,
                "margin": safety["margin"]
            }

        knowledge = get_disease_knowledge(
            disease_class,
            language
        )

        if knowledge is None:
            return {
                "success": True,
                "status": "confirmed",
                "language": language,
                "disease": disease_class,
                "confidence": f"{confidence:.2f}%",
                "crop": predicted_crop,
                "crop_confidence": (
                    f"{crop_confidence:.2f}%"
                ),
                "disease_name": disease_class,
                "symptoms": (
                    "Disease information is not available."
                ),
                "management": (
                    "Disease-specific management "
                    "information is not available."
                ),
                "prevention": (
                    "Disease-specific prevention "
                    "information is not available."
                ),
                "source": "",
                "top_predictions": top_predictions,
                "top_crops": top_crops,
                "safety_status": safety_status,
                "safety_reason": safety["reason"],
                "margin": safety["margin"],
                "crop_matches_disease": True
            }

        return {
            "success": True,
            "status": "confirmed",
            "language": language,
            "disease": disease_class,
            "confidence": f"{confidence:.2f}%",
            "crop": predicted_crop,
            "crop_confidence": (
                f"{crop_confidence:.2f}%"
            ),
            "disease_name": knowledge["disease_name"],
            "symptoms": knowledge["symptoms"],
            "management": knowledge["management"],
            "prevention": knowledge["prevention"],
            "source": knowledge["source"],
            "top_predictions": top_predictions,
            "top_crops": top_crops,
            "safety_status": safety_status,
            "safety_reason": safety["reason"],
            "margin": safety["margin"],
            "crop_matches_disease": True
        }

    except Exception as e:

        print(
            "DISEASE DETECTION ERROR:",
            e
        )

        return {
            "success": False,
            "status": "error",
            "error": str(e)
        }

    finally:

        if (
            temp_path
            and os.path.exists(temp_path)
        ):
            os.remove(temp_path)
