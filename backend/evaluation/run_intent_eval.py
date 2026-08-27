import csv
import json
import os
import sys
from collections import defaultdict

from chatbot.rag.query_parser import parse_query


# ============================================================
# PATHS
# ============================================================

DATASET_PATH = (
    "final_evaluation_datasets/"
    "intent_classification_dataset.csv"
)

RESULT_DIR = "evaluation/results"

RESULT_FILE = (
    RESULT_DIR +
    "/intent_classification_results.csv"
)

SUMMARY_FILE = (
    RESULT_DIR +
    "/intent_classification_summary.json"
)


# ============================================================
# SUPPORTED INTENTS
# ============================================================

SUPPORTED_INTENTS = {
    "LATEST_VALUE",
    "TREND",
    "ABNORMAL_LABS",
    "MEDICAL_DEFINITION",
    "GENERAL_RAG",
}


# ============================================================
# EXTRACT PREDICTED INTENTS
# ============================================================

def get_predicted_intents(result):

    intents = []

    tasks = result.get(
        "tasks",
        []
    )

    if not isinstance(tasks, list):
        return intents

    for task in tasks:

        if not isinstance(task, dict):
            continue

        intent = task.get("intent")

        if intent:
            intents.append(
                intent
            )

    return intents


# ============================================================
# CONVERSATIONAL INTENT
# ============================================================

def get_conversational_intent(result):

    if result.get("greeting") is True:
        return "GREETING"

    if result.get("thanks") is True:
        return "THANKS"

    if result.get("bye") is True:
        return "GOODBYE"

    return None


# ============================================================
# GET PRIMARY PREDICTION
# ============================================================

def get_primary_prediction(result):

    conversational = (
        get_conversational_intent(result)
    )

    if conversational:
        return conversational

    intents = get_predicted_intents(
        result
    )

    if not intents:
        return "NO_INTENT"

    return intents[0]


# ============================================================
# EVALUATE ONE QUERY
# ============================================================

def evaluate_query(
    query,
    expected_intent
):

    try:

        result = parse_query(
            query
        )

        if not isinstance(result, dict):

            return {
                "predicted_intent": "INVALID_RESPONSE",
                "predicted_intents": [],
                "correct": False,
                "raw_response": str(result),
                "error": "Parser did not return a dictionary"
            }

        predicted_intents = (
            get_predicted_intents(
                result
            )
        )

        conversational = (
            get_conversational_intent(
                result
            )
        )

        # ----------------------------------------------------
        # Conversational queries
        # ----------------------------------------------------

        if expected_intent in {
            "GREETING",
            "THANKS",
            "GOODBYE"
        }:

            predicted = (
                conversational
                if conversational
                else "NO_INTENT"
            )

            correct = (
                predicted == expected_intent
            )

        # ----------------------------------------------------
        # Medical intents
        # ----------------------------------------------------

        else:

            predicted = (
                predicted_intents[0]
                if predicted_intents
                else "NO_INTENT"
            )

            correct = (
                expected_intent
                in predicted_intents
            )

        return {
            "predicted_intent": predicted,
            "predicted_intents": predicted_intents,
            "correct": correct,
            "raw_response": json.dumps(
                result,
                ensure_ascii=False
            ),
            "error": ""
        }

    except Exception as e:

        return {
            "predicted_intent":
                "ERROR",

            "predicted_intents":
                [],

            "correct":
                False,

            "raw_response":
                "",

            "error":
                str(e)
        }


# ============================================================
# CONFUSION MATRIX
# ============================================================

def build_confusion_matrix(
    rows,
    labels
):

    matrix = {
        expected: {
            predicted: 0
            for predicted in labels
        }
        for expected in labels
    }

    for row in rows:

        expected = row[
            "expected_intent"
        ]

        predicted = row[
            "predicted_intent"
        ]

        if expected not in matrix:
            continue

        if predicted not in matrix[expected]:
            continue

        matrix[
            expected
        ][
            predicted
        ] += 1

    return matrix


# ============================================================
# PER-CLASS METRICS
# ============================================================

def calculate_class_metrics(
    rows,
    labels
):

    metrics = {}

    for label in labels:

        tp = 0
        fp = 0
        fn = 0

        for row in rows:

            expected = row[
                "expected_intent"
            ]

            predicted = row[
                "predicted_intent"
            ]

            if (
                expected == label
                and predicted == label
            ):
                tp += 1

            elif (
                expected != label
                and predicted == label
            ):
                fp += 1

            elif (
                expected == label
                and predicted != label
            ):
                fn += 1

        precision = (
            tp / (tp + fp)
            if tp + fp > 0
            else 0
        )

        recall = (
            tp / (tp + fn)
            if tp + fn > 0
            else 0
        )

        f1 = (
            2 * precision * recall
            / (precision + recall)
            if precision + recall > 0
            else 0
        )

        metrics[label] = {
            "true_positive": tp,
            "false_positive": fp,
            "false_negative": fn,
            "precision": precision,
            "recall": recall,
            "f1": f1
        }

    return metrics


# ============================================================
# MAIN
# ============================================================

def main():

    os.makedirs(
        RESULT_DIR,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Load dataset
    # --------------------------------------------------------

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        dataset = list(reader)

    print(
        f"\nLoaded {len(dataset)} queries"
    )

    # --------------------------------------------------------
    # Evaluate
    # --------------------------------------------------------

    results = []

    for index, row in enumerate(
        dataset,
        start=1
    ):

        query = row[
            "query"
        ].strip()

        expected = row[
            "expected_intent"
        ].strip()

        print(
            f"\n[{index}/{len(dataset)}]"
        )

        print(
            "Query:",
            query
        )

        print(
            "Expected:",
            expected
        )

        evaluation = evaluate_query(
            query,
            expected
        )

        predicted = evaluation[
            "predicted_intent"
        ]

        correct = evaluation[
            "correct"
        ]

        print(
            "Predicted:",
            predicted
        )

        print(
            "Correct:",
            "YES" if correct else "NO"
        )

        results.append({

            "query_id":
                row.get(
                    "query_id",
                    str(index)
                ),

            "query":
                query,

            "expected_intent":
                expected,

            "predicted_intent":
                predicted,

            "predicted_intents":
                json.dumps(
                    evaluation[
                        "predicted_intents"
                    ]
                ),

            "correct":
                correct,

            "error":
                evaluation[
                    "error"
                ],

            "raw_response":
                evaluation[
                    "raw_response"
                ]
        })

    # ========================================================
    # OVERALL ACCURACY
    # ========================================================

    total = len(results)

    correct = sum(
        1
        for row in results
        if row["correct"]
    )

    accuracy = (
        correct / total
        if total > 0
        else 0
    )

    # ========================================================
    # CLASS METRICS
    # ========================================================

    labels = [
        "LATEST_VALUE",
        "TREND",
        "ABNORMAL_LABS",
        "MEDICAL_DEFINITION",
        "GENERAL_RAG",
        "GREETING",
        "THANKS",
        "GOODBYE",
    ]

    class_metrics = (
        calculate_class_metrics(
            results,
            labels
        )
    )

    confusion_matrix = (
        build_confusion_matrix(
            results,
            labels
        )
    )

    # ========================================================
    # MACRO F1
    # ========================================================

    f1_values = [
        class_metrics[label]["f1"]
        for label in labels
    ]

    macro_f1 = (
        sum(f1_values)
        / len(f1_values)
    )

    # ========================================================
    # SAVE QUERY RESULTS
    # ========================================================

    with open(
        RESULT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "query_id",
                "query",
                "expected_intent",
                "predicted_intent",
                "predicted_intents",
                "correct",
                "error",
                "raw_response"
            ]
        )

        writer.writeheader()

        writer.writerows(
            results
        )

    # ========================================================
    # SAVE SUMMARY
    # ========================================================

    summary = {

        "total_queries":
            total,

        "correct":
            correct,

        "incorrect":
            total - correct,

        "accuracy":
            accuracy,

        "macro_f1":
            macro_f1,

        "per_class":
            class_metrics,

        "confusion_matrix":
            confusion_matrix
    }

    with open(
        SUMMARY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            summary,
            f,
            indent=4
        )

    # ========================================================
    # PRINT SUMMARY
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "INTENT CLASSIFICATION EVALUATION"
    )

    print(
        "=" * 60
    )

    print(
        f"Total Queries : {total}"
    )

    print(
        f"Correct       : {correct}"
    )

    print(
        f"Incorrect     : {total - correct}"
    )

    print(
        f"Accuracy      : {accuracy:.4f}"
    )

    print(
        f"Macro F1      : {macro_f1:.4f}"
    )

    print(
        "\nPER-CLASS METRICS"
    )

    print(
        "-" * 60
    )

    for label in labels:

        m = class_metrics[
            label
        ]

        print(
            f"\n{label}"
        )

        print(
            f"  Precision: {m['precision']:.4f}"
        )

        print(
            f"  Recall:    {m['recall']:.4f}"
        )

        print(
            f"  F1:        {m['f1']:.4f}"
        )

    print(
        "\nResults saved to:"
    )

    print(
        RESULT_FILE
    )

    print(
        SUMMARY_FILE
    )


if __name__ == "__main__":
    main()