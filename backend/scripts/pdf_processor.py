# pdf_processor.py

import fitz  # PyMuPDF
import os
import tempfile
import cv2
import numpy as np


def pdf_to_images(pdf_path, dpi=150):

    doc = fitz.open(pdf_path)

    temp_dir = tempfile.mkdtemp()

    image_paths = []

    zoom = dpi / 72  # 72 is default PDF DPI
    mat = fitz.Matrix(zoom, zoom)

    for i, page in enumerate(doc, start=1):

        pix = page.get_pixmap(matrix=mat)

        path = os.path.join(temp_dir, f"page_{i}.png")

        pix.save(path)

        print("Saved image:", path)

        image_paths.append(path)

    return image_paths

