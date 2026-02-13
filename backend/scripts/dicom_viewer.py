import pydicom
import matplotlib.pyplot as plt
import numpy as np


def load_dicom(file_path):
    """
    Loads DICOM file and returns dataset
    """
    ds = pydicom.dcmread(file_path)
    return ds


def normalize_image(img):
    """
    Normalize image for display (0–255)
    """
    img = img.astype(np.float32)
    img -= np.min(img)
    img /= np.max(img)
    img *= 255.0
    return img.astype(np.uint8)


def show_dicom_image(ds):
    """
    Display DICOM image (supports 2D and 3D volumes)
    """

    if not hasattr(ds, "pixel_array"):
        print("No pixel data found in DICOM.")
        return

    img = ds.pixel_array

    print(f"Pixel array shape: {img.shape}")

    # Case 1: 2D image
    if len(img.shape) == 2:
        img_display = normalize_image(img)

    # Case 2: 3D volume (e.g., CT/MRI)
    elif len(img.shape) == 3:
        middle_slice = img.shape[0] // 2
        print(f"Displaying middle slice: {middle_slice}")
        img_display = normalize_image(img[middle_slice])

    else:
        print("Unsupported DICOM format.")
        return

    plt.imshow(img_display, cmap="gray")
    plt.title("DICOM Image")
    plt.axis("off")
    plt.show()


def extract_dicom_metadata(ds):
    """
    Extract useful patient metadata
    """
    metadata = {
        "patient_name": str(getattr(ds, "PatientName", "Unknown")),
        "patient_id": getattr(ds, "PatientID", "Unknown"),
        "modality": getattr(ds, "Modality", "Unknown"),
        "study_date": getattr(ds, "StudyDate", "Unknown"),
        "study_description": getattr(ds, "StudyDescription", "Unknown"),
        "rows": getattr(ds, "Rows", "Unknown"),
        "columns": getattr(ds, "Columns", "Unknown"),
        "number_of_frames": getattr(ds, "NumberOfFrames", 1)
    }

    return metadata
