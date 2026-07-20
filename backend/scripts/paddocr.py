#
## PaddleOCR is temporarily disabled. The original implementation is retained below.
# PaddleOCR code follows:
#import os
#
## Keep Paddle's native inference path conservative inside Docker.
#os.environ.setdefault("FLAGS_enable_pir_api", "0")
#os.environ.setdefault("FLAGS_use_mkldnn", "0")
#os.environ.setdefault("OMP_NUM_THREADS", "1")
#
#from paddleocr import PaddleOCR
#
#ocr = PaddleOCR(
#    lang="en",
#    use_doc_orientation_classify=False,
#    use_doc_unwarping=False,
#    use_textline_orientation=False
#)
#
#def run_ocr(image_path):
#    result = ocr.ocr(image_path, cls=False)
#
#    texts = []
#    scores = []
#
#    for line in result[0]:
#        text = line[1][0]
#        score = line[1][1]
#        texts.append(text)
#        scores.append(score)
#
#    return texts, scores
