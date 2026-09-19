from typing import Dict, Any


# Minimum confidence for a prediction to be considered usable.
MIN_CONFIDENCE = 70.0

# If the difference between Top-1 and Top-2 is very small,
# the model is considered ambiguous.
MIN_MARGIN = 15.0


def evaluate_prediction(prediction: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate disease model output and assign a safety status.

    Possible statuses:
        - confirmed
        - uncertain
        - review_required
    """

    if not prediction:
        return {
            "status": "review_required",
            "reason": "No prediction was returned by the disease model."
        }

    confidence = float(prediction.get("confidence", 0.0))

    top_predictions = prediction.get("top_predictions", [])

    if not top_predictions:
        return {
            "status": "review_required",
            "reason": "Top predictions are unavailable."
        }

    top1 = top_predictions[0]
    top1_confidence = float(top1.get("confidence", confidence))

    if len(top_predictions) >= 2:
        top2 = top_predictions[1]
        top2_confidence = float(top2.get("confidence", 0.0))
    else:
        top2_confidence = 0.0

    margin = top1_confidence - top2_confidence

    # Very low confidence
    if confidence < MIN_CONFIDENCE:
        return {
            "status": "uncertain",
            "reason": (
                f"Model confidence is below the safety threshold "
                f"of {MIN_CONFIDENCE:.0f}%."
            ),
            "confidence": confidence,
            "margin": round(margin, 2)
        }

    # High confidence but competing prediction is too close
    if margin < MIN_MARGIN:
        return {
            "status": "review_required",
            "reason": (
                "Top predictions are too close to each other, "
                "so the result requires additional review."
            ),
            "confidence": confidence,
            "margin": round(margin, 2)
        }

    # Prediction passes the basic safety checks
    return {
        "status": "confirmed",
        "reason": "Prediction passed the basic confidence and margin checks.",
        "confidence": confidence,
        "margin": round(margin, 2)
    }