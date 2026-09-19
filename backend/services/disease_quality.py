from pathlib import Path

from PIL import Image, ImageStat


# ============================================================
# CONFIG
# ============================================================

MIN_WIDTH = 224
MIN_HEIGHT = 224

MIN_BRIGHTNESS = 25
MAX_BRIGHTNESS = 235


# ============================================================
# IMAGE QUALITY CHECK
# ============================================================

def check_image_quality(image_path: str):

    try:

        path = Path(image_path)

        if not path.exists():
            return {
                "valid": False,
                "message": "Image file could not be found."
            }

        # ----------------------------------------------------
        # Open image
        # ----------------------------------------------------

        image = Image.open(path).convert("RGB")

        width, height = image.size


        # ----------------------------------------------------
        # Resolution check
        # ----------------------------------------------------

        if width < MIN_WIDTH or height < MIN_HEIGHT:

            return {
                "valid": False,
                "message": (
                    "Image resolution is too small. "
                    "Please upload a clearer leaf image."
                )
            }


        # ----------------------------------------------------
        # Brightness check
        # ----------------------------------------------------

        stat = ImageStat.Stat(image)

        brightness = sum(stat.mean) / 3


        if brightness < MIN_BRIGHTNESS:

            return {
                "valid": False,
                "message": (
                    "Image is too dark. "
                    "Please upload an image with better lighting."
                )
            }


        if brightness > MAX_BRIGHTNESS:

            return {
                "valid": False,
                "message": (
                    "Image is too bright. "
                    "Please upload a clearly visible leaf image."
                )
            }


        # ----------------------------------------------------
        # Image is acceptable
        # ----------------------------------------------------

        return {
            "valid": True,
            "message": "Image quality is acceptable.",
            "width": width,
            "height": height,
            "brightness": round(brightness, 2)
        }


    except Exception as e:

        return {
            "valid": False,
            "message": f"Unable to process image: {str(e)}"
        }