# document_ocr.py

import os
from ocr_pipeline import ocr_process
from pdf_processor import pdf_to_images


def run_document_ocr(path):

    pages = []

    if path.lower().endswith(".pdf"):

        images = pdf_to_images(path)

        for i, img in enumerate(images, 1):

            data = ocr_process(img)

            data["page"] = i

            pages.append(data)

    else:

        data = ocr_process(path)
        data["page"] = 1

        pages.append(data)

    return pages
