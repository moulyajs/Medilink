import pandas as pd
import statistics
import json
import matplotlib.pyplot as plt
import seaborn as sns



THRESHOLD = 20  # percentage


# ============================================================
# MEDILINK PERSONAL BASELINE ANOMALY DETECTION
# ============================================================

def detect_anomaly(historical_values, current_value):

    # Need history to establish baseline
    if len(historical_values) < 2:
        return {
            "alert": 0,
            "personal_average": None,
            "percent_change": None,
            "reason": "Insufficient history"
        }

    # Patient-specific baseline
    personal_average = statistics.mean(historical_values)

    # Avoid division by zero
    if personal_average == 0:
        return {
            "alert": 0,
            "personal_average": personal_average,
            "percent_change": None,
            "reason": "Baseline is zero"
        }

    # Calculate deviation
    deviation = current_value - personal_average

    percent_change = (
        deviation / personal_average
    ) * 100

    # Your current anomaly rule
    if abs(percent_change) >= THRESHOLD:

        direction = (
            "INCREASE"
            if percent_change > 0
            else "DECREASE"
        )

        return {
            "alert": 1,
            "personal_average": personal_average,
            "percent_change": percent_change,
            "reason": f"{direction} >= {THRESHOLD}%"
        }

    return {
        "alert": 0,
        "personal_average": personal_average,
        "percent_change": percent_change,
        "reason": f"Change below {THRESHOLD}%"
    }


# ============================================================
# CONVENTIONAL POPULATION REFERENCE RANGE METHOD
# ============================================================

def conventional_detection(
    current_value,
    ref_low,
    ref_high
):

    # Outside population reference range = abnormal
    if current_value < ref_low:
        return 1

    if current_value > ref_high:
        return 1

    return 0


# ============================================================
# METRICS
# ============================================================

def calculate_metrics(y_true, y_pred):

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for actual, predicted in zip(y_true, y_pred):

        if actual == 1 and predicted == 1:
            tp += 1

        elif actual == 0 and predicted == 0:
            tn += 1

        elif actual == 0 and predicted == 1:
            fp += 1

        elif actual == 1 and predicted == 0:
            fn += 1

    total = tp + tn + fp + fn

    accuracy = (
        (tp + tn) / total
        if total > 0
        else 0
    )

    precision = (
        tp / (tp + fp)
        if (tp + fp) > 0
        else 0
    )

    recall = (
        tp / (tp + fn)
        if (tp + fn) > 0
        else 0
    )

    f1 = (
        2 * precision * recall /
        (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    return {
        "TP": tp,
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    }


# ============================================================
# LOAD AND TEST DATASET
# ============================================================

def run_test():

    print("\nLoading dataset...\n")

    df = pd.read_csv(
        "final_evaluation_datasets/medilink_anomaly_test_160_cases.csv"
    )

    print(
        f"Total test cases: {len(df)}"
    )

    results = []

    y_true = []
    y_pred = []

    conventional_pred = []

    # ========================================================
    # RUN EVERY TEST CASE
    # ========================================================

    for _, row in df.iterrows():

        # Convert historical values:
        #
        # "10.0,10.2,9.9,10.1"
        #
        # into:
        #
        # [10.0, 10.2, 9.9, 10.1]

        history_string = str(
            row["historical_values"]
        )

        historical_values = [

            float(value.strip())

            for value in history_string.split(",")

            if value.strip()

        ]

        current_value = float(
            row["current_value"]
        )

        # ----------------------------------------------------
        # RUN MEDILINK PERSONAL BASELINE
        # ----------------------------------------------------

        personal_result = detect_anomaly(
            historical_values,
            current_value
        )

        system_prediction = (
            personal_result["alert"]
        )

        # ----------------------------------------------------
        # RUN CONVENTIONAL METHOD
        # ----------------------------------------------------

        conventional_result = (
            conventional_detection(
                current_value,
                float(row["ref_low"]),
                float(row["ref_high"])
            )
        )

        # ----------------------------------------------------
        # EXPECTED RESULT
        # ----------------------------------------------------

        expected = int(
            row["expected_personal_deviation"]
        )

        # ----------------------------------------------------
        # SAVE FOR METRICS
        # ----------------------------------------------------

        y_true.append(expected)

        y_pred.append(
            system_prediction
        )

        conventional_pred.append(
            conventional_result
        )

        # ----------------------------------------------------
        # SAVE RESULT
        # ----------------------------------------------------

        results.append({

            "case_id":
                row["case_id"],

            "test_name":
                row["test_name"],

            "historical_values":
                history_string,

            "current_value":
                current_value,

            "personal_average":
                personal_result[
                    "personal_average"
                ],

            "percent_change":
                personal_result[
                    "percent_change"
                ],

            "expected_alert":
                expected,

            "medilink_prediction":
                system_prediction,

            "conventional_prediction":
                conventional_result,

            "scenario":
                row["scenario"],

            "population_status":
                row["population_status"],

            "reason":
                personal_result["reason"]
        })

    # ========================================================
    # CALCULATE METRICS
    # ========================================================

    medilink_metrics = calculate_metrics(
        y_true,
        y_pred
    )

    conventional_metrics = calculate_metrics(
        y_true,
        conventional_pred
    )

    # ========================================================
    # PRINT RESULTS
    # ========================================================

    print("\n")
    print("=" * 55)

    print("MEDILINK PERSONAL BASELINE RESULTS")

    print("=" * 55)

    for key, value in medilink_metrics.items():

        if isinstance(value, float):

            print(
                f"{key}: "
                f"{value * 100:.2f}%"
            )

        else:

            print(
                f"{key}: {value}"
            )

    print("\n")
    print("=" * 55)

    print("CONVENTIONAL REFERENCE RANGE RESULTS")

    print("=" * 55)

    for key, value in conventional_metrics.items():

        if isinstance(value, float):

            print(
                f"{key}: "
                f"{value * 100:.2f}%"
            )

        else:

            print(
                f"{key}: {value}"
            )

    # ========================================================
    # SPECIAL ANALYSIS:
    # IN-RANGE BUT PERSONAL DEVIATION
    # ========================================================

    results_df = pd.DataFrame(results)

    in_range_personal_alert = results_df[
        (
            results_df["population_status"]
            == "Normal"
        )
        &
        (
            results_df["medilink_prediction"]
            == 1
        )
    ]

    print("\n")
    print("=" * 55)

    print(
        "IN-RANGE VALUES WITH "
        "PERSONAL DEVIATION ALERT"
    )

    print("=" * 55)

    print(
        f"Cases found: "
        f"{len(in_range_personal_alert)}"
    )

    if len(in_range_personal_alert) > 0:

        print(
            in_range_personal_alert[
                [
                    "case_id",
                    "test_name",
                    "current_value",
                    "personal_average",
                    "percent_change",
                    "population_status"
                ]
            ].to_string(
                index=False
            )
        )

    # ========================================================
    # SAVE RESULTS
    # ========================================================

        # ========================================================
    # SAVE RESULTS AS JSON
    # ========================================================

    output_path = "evaluation/anomaly_test_results.json"

    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)

    print("\n")
    print("=" * 55)
    print("Results saved successfully!")
    print(f"File: {output_path}")
    print("=" * 55)


    # ========================================================
    # SAVE CONFUSION MATRIX
    # ========================================================

    cm = [
        [medilink_metrics["TN"], medilink_metrics["FP"]],
        [medilink_metrics["FN"], medilink_metrics["TP"]]
    ]

    plt.figure(figsize=(6, 5))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Normal", "Anomaly"],
        yticklabels=["Normal", "Anomaly"]
    )

    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Medilink Personal Baseline - Confusion Matrix")

    plt.tight_layout()

    plt.savefig(
        "evaluation/anomaly_confusion_matrix.png",
        dpi=300
    )

    plt.close()

    print(
        "Confusion matrix saved to "
        "evaluation/anomaly_confusion_matrix.png"
    )


if __name__ == "__main__":
    run_test()



if __name__ == "__main__":

    run_test()