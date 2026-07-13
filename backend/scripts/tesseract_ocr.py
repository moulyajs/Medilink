import pytesseract
from pytesseract import Output
from PIL import Image


def run_ocr(image_path):
    """Return OCR text and confidence scores in the existing pipeline format."""
    data = pytesseract.image_to_data(
        Image.open(image_path),
        lang="eng",
        config="--oem 3 --psm 6",
        output_type=Output.DICT,
    )

    texts = []
    scores = []

    for text, confidence in zip(data["text"], data["conf"]):
        text = text.strip()
        confidence = float(confidence)

        if text and confidence >= 0:
            texts.append(text)
            scores.append(confidence / 100)

    return texts, scores
