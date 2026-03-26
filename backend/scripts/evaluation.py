import os
import json
import sys

# ============================================================
# SYSTEM PATH SETUP
# ============================================================

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# ============================================================
# IMPORT REAL PIPELINE MODULES
# ============================================================

from lab_extraction import extract_lab_results
from lab_normalizer import normalize_lab_results

# ============================================================
# CONFIG
# ============================================================

DATA_FOLDER = "../data"
GT_FOLDER = "../ground_truth"
PDF_NAME = "drlogylab.pdf"   # change if needed


# ============================================================
# GET ABNORMAL FROM PIPELINE OUTPUT
# ============================================================

def get_abnormal_from_pipeline(normalized_labs):
    abnormal = []

    for lab in normalized_labs:
        if lab.get("status") in ["HIGH", "LOW"]:
            abnormal.append(
                (lab.get("test"), lab.get("status"))
            )

    return set(abnormal)


# ============================================================
# GET ABNORMAL FROM GROUND TRUTH JSON
# ============================================================

def get_abnormal_from_ground_truth(gt_json):
    abnormal = []

    for test in gt_json["tests"]:
        if test["status"] in ["HIGH", "LOW"]:
            abnormal.append(
                (test["test"], test["status"])
            )

    return set(abnormal)


# ============================================================
# EVALUATION METRICS
# ============================================================

def evaluate(pred_set, gt_set):

    TP = len(pred_set & gt_set)
    FP = len(pred_set - gt_set)
    FN = len(gt_set - pred_set)

    precision = TP / (TP + FP) if (TP + FP) else 0
    recall = TP / (TP + FN) if (TP + FN) else 0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall)
        else 0
    )

    return TP, FP, FN, precision, recall, f1


# ============================================================
# MAIN
# ============================================================

def main():

    pdf_path = os.path.join(DATA_FOLDER, PDF_NAME)
    gt_path = os.path.join(
        GT_FOLDER,
        PDF_NAME.replace(".pdf", ".json")
    )

    print("\n======================================")
    print("🔎 EVALUATING:", PDF_NAME)
    print("======================================")

    # ---------------------------------------
    # Run pipeline
    # ---------------------------------------

    raw_labs = extract_lab_results(pdf_path, is_pdf=True)
    normalized_labs = normalize_lab_results(raw_labs)

    pred_set = get_abnormal_from_pipeline(normalized_labs)

    print("\n🔴 PREDICTED ABNORMAL:")
    print(pred_set)

    # ---------------------------------------
    # Load Ground Truth
    # ---------------------------------------

    with open(gt_path, "r") as f:
        gt_json = json.load(f)

    gt_set = get_abnormal_from_ground_truth(gt_json)

    print("\n🟢 GROUND TRUTH ABNORMAL:")
    print(gt_set)

    # ---------------------------------------
    # Compute Metrics
    # ---------------------------------------

    TP, FP, FN, precision, recall, f1 = evaluate(
        pred_set,
        gt_set
    )

    print("\n======================================")
    print("📊 METRICS")
    print("======================================")
    print("TP:", TP)
    print("FP:", FP)
    print("FN:", FN)
    print("Precision:", round(precision, 3))
    print("Recall:", round(recall, 3))
    print("F1 Score:", round(f1, 3))
    print("======================================\n")


if __name__ == "__main__":
    main()