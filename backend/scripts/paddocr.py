from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_textline_orientation=True,
    lang="en"
)

def run_ocr(image_path):
    result = ocr.predict(image_path)

    texts = result[0]["rec_texts"]
    scores = result[0]["rec_scores"]

    return texts, scores
