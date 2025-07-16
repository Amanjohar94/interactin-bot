# bot_core/utils/image_detector.py

try:
    import imghdr
except ImportError:
    imghdr = None

from PIL import Image

def detect_image_type(path: str) -> str:
    """
    Return image type, e.g. "jpeg", "png".
    First try stdlib imghdr, then Pillow if imghdr is missing or inconclusive.
    """
    if imghdr:
        img_type = imghdr.what(path)
        if img_type:
            return img_type

    # Fallback to Pillow
    with Image.open(path) as img:
        return img.format.lower()