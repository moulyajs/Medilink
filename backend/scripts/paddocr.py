from paddleocr import PaddleOCR

ocr = PaddleOCR(
    lang="en",
    use_angle_cls=True
)


def run_ocr(image_path):
    
    result = ocr.ocr(image_path)

    blocks = []

    if not result:
        return blocks

    # NEW FORMAT (PaddleOCR v5 / PaddleX style)
    if isinstance(result, list) and isinstance(result[0], dict):

        data = result[0]

        texts = data.get("rec_texts", [])
        scores = data.get("rec_scores", [])
        boxes = data.get("rec_polys", [])

        for i in range(len(texts)):

            text = texts[i]
            score = float(scores[i]) if i < len(scores) else 1.0
            bbox = boxes[i] if i < len(boxes) else None

            blocks.append({
                "text": str(text).strip(),
                "confidence": score,
                "bbox": bbox
            })

        return blocks


    # OLD FORMAT (fallback)
    for page in result:

        for line in page:

            bbox = line[0]

            text = ""
            score = 1.0

            if len(line) >= 2 and isinstance(line[1], (list, tuple)):
                text = line[1][0]
                try:
                    score = float(line[1][1])
                except:
                    pass
            else:
                if len(line) >= 2:
                    text = line[1]

                if len(line) >= 3:
                    try:
                        score = float(line[2])
                    except:
                        pass

            blocks.append({
                "text": str(text).strip(),
                "confidence": score,
                "bbox": bbox
            })

    return blocks
