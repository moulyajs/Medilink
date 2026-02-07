
#paddocr.py
from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_textline_orientation=True,
    lang="en"
)

def run_ocr(image_path):
    result = ocr.ocr(image_path, cls=False)

    texts = []
    scores = []

    for line in result[0]:
        text = line[1][0]
        score = line[1][1]
        texts.append(text)
        scores.append(score)

    return texts, scores
