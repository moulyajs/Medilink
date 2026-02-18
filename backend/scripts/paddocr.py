from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_textline_orientation=True,
    lang="en"
)

def run_ocr(image_path):

    result = ocr.ocr(image_path)

    texts = []
    scores = []

    if not result:
        return [], []

    # New PaddleOCR structure
    if isinstance(result[0], dict):

        texts = result[0].get("rec_texts", [])
        scores = result[0].get("rec_scores", [])

    # Old PaddleOCR structure (fallback)
    elif isinstance(result[0], list):

        for line in result[0]:
            if len(line) >= 2:
                text = line[1][0]
                score = line[1][1]
                texts.append(text)
                scores.append(score)

    return texts, scores
