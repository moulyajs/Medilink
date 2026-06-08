import cv2

# scanned docs (lab reports)
def preprocess_printed(image_path):
    img = cv2.imread(image_path)

    # Scaling (Image Resizing)
    # Increases resolution → helps OCR detect small printed text more accurately
    img = cv2.resize(img, None, fx=1.2, fy=1.2)

    # Grayscale Conversion
    # Removes color information → simplifies image for text extraction
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    # Enhances local contrast → improves visibility of faint printed text
    # Prevents over-amplification of noise (unlike global histogram equalization)
    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Final enhanced image for OCR
    return enhanced


# Handwritten docs


def preprocess_handwritten(image_path):
    img = cv2.imread(image_path)

    # Grayscale Conversion
    # Standard preprocessing step to simplify input
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Adaptive Thresholding (Binarization)
    # Converts image to black & white
    # Works well for uneven lighting and handwritten text
    # Gaussian method considers neighborhood pixels → better edge detection
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    # Median Filtering (Noise Removal)
    # Removes salt-and-pepper noise while preserving edges
    # Important for handwritten strokes
    denoised = cv2.medianBlur(thresh, 3)

    # Final cleaned image for OCR
    return denoised