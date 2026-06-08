from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_textline_orientation=True,
    lang="en"
)

def run_ocr(image_input, return_raw=False):
    result = ocr.ocr(image_input, cls=False)

    texts = []
    scores = []

    if not result or result[0] is None:
        return (texts, scores, result) if return_raw else (texts, scores)

    for line in result[0]:
        text = line[1][0]
        score = line[1][1]
        texts.append(text)
        scores.append(score)

    if return_raw:
        return texts, scores, result

    return texts, scores