# evaluation/run_handler_eval.py

import csv
import json
import os
import re

from evaluation.metrics import mean

from chatbot.rag.handlers.latest import handle_latest
from chatbot.rag.handlers.trend import handle_trend
from chatbot.rag.handlers.abnormal import handle_abnormal
from chatbot.rag.handlers.definition import handle_definition
from chatbot.rag.handlers.rag import handle_rag


# ============================================================
# CONFIG
# ============================================================

DATASET_PATH = (
    "final_evaluation_datasets/"
    "handler_dataset.csv"
)

RESULT_DIR = (
    "evaluation/results"
)

RESULT_FILE = (
    RESULT_DIR +
    "/handler_results.csv"
)

SUMMARY_FILE = (
    RESULT_DIR +
    "/handler_summary.json"
)


# ============================================================
# NORMALIZATION
# ============================================================

def normalize(text):

    if text is None:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# PARSE JSON LIST
# ============================================================

def parse_json_list(value):

    if not value:
        return []

    try:

        result = json.loads(
            value
        )

        if isinstance(
            result,
            list
        ):
            return result

    except Exception:
        pass

    return []


# ============================================================
# HANDLER DISPATCH
# ============================================================

def execute_handler(
    intent,
    task,
    patient_id,
    query
):

    if intent == "LATEST_VALUE":

        return handle_latest(
            task,
            patient_id,
            query
        )

    if intent == "TREND":

        return handle_trend(
            task,
            patient_id,
            query
        )

    if intent == "ABNORMAL_LABS":

        return handle_abnormal(
            task,
            patient_id,
            query
        )

    if intent == "MEDICAL_DEFINITION":

        return handle_definition(
            task,
            patient_id,
            query
        )

    if intent == "GENERAL_RAG":

        return handle_rag(
            task,
            patient_id,
            query
        )

    raise ValueError(
        f"Unsupported intent: {intent}"
    )


# ============================================================
# LATEST VALUE EVALUATION
# ============================================================

def evaluate_latest(
    row,
    response
):

    content = normalize(
        response.get(
            "content",
            ""
        )
    )

    expected_value = normalize(
        row.get(
            "expected_value",
            ""
        )
    )

    expected_date = normalize(
        row.get(
            "expected_date",
            ""
        )
    )

    value_correct = (
        expected_value != ""
        and expected_value in content
    )

    date_correct = (
        expected_date == ""
        or expected_date in content
    )

    return {

        "value_correct":
            value_correct,

        "date_correct":
            date_correct,

        "correct":
            value_correct
            and date_correct
    }


# ============================================================
# TREND EVALUATION
# ============================================================

def evaluate_trend(
    row,
    response
):

    content = normalize(
        response.get(
            "content",
            ""
        )
    )

    expected_trend = normalize(
        row.get(
            "expected_trend",
            ""
        )
    )

    expected_value = normalize(
        row.get(
            "expected_value",
            ""
        )
    )

    expected_status = normalize(
        row.get(
            "expected_status",
            ""
        )
    )

    trend_correct = (
        expected_trend != ""
        and expected_trend in content
    )

    value_correct = (
        expected_value == ""
        or expected_value in content
    )

    status_correct = (
        expected_status == ""
        or expected_status in content
    )

    return {

        "trend_correct":
            trend_correct,

        "value_correct":
            value_correct,

        "status_correct":
            status_correct,

        "correct":
            trend_correct
            and value_correct
            and status_correct
    }


# ============================================================
# ABNORMAL LAB EVALUATION
# ============================================================

def evaluate_abnormal(
    row,
    response
):

    content = normalize(
        response.get(
            "content",
            ""
        )
    )

    expected_tests = (
        parse_json_list(
            row.get(
                "expected_tests",
                ""
            )
        )
    )

    if not expected_tests:

        return {
            "correct": False,
            "tests_found": 0
        }

    found = 0

    for test in expected_tests:

        if normalize(test) in content:

            found += 1

    accuracy = (
        found / len(expected_tests)
    )

    return {

        "tests_found":
            found,

        "total_expected":
            len(expected_tests),

        "test_coverage":
            accuracy,

        "correct":
            found == len(expected_tests)
    }


# ============================================================
# DEFINITION
# ============================================================

def evaluate_definition(
    row,
    response
):

    content = normalize(
        response.get(
            "content",
            ""
        )
    )

    # --------------------------------------------------------
    # Definition answers are NOT evaluated by exact text.
    #
    # We only perform basic response validity here.
    # Full answer quality is evaluated later.
    # --------------------------------------------------------

    non_empty = (
        len(content) > 0
    )

    return {

        "non_empty":
            non_empty,

        "correct":
            non_empty
    }


# ============================================================
# GENERAL RAG
# ============================================================

def evaluate_rag(
    row,
    response
):

    chunks = response.get(
        "chunks",
        []
    )

    content = normalize(
        response.get(
            "content",
            ""
        )
    )

    expected_chunks = (
        parse_json_list(
            row.get(
                "expected_chunk_texts",
                ""
            )
        )
    )

    # --------------------------------------------------------
    # Check whether expected chunk text appears
    # in returned chunks.
    # --------------------------------------------------------

    retrieved_texts = [

        normalize(
            c.get(
                "text",
                ""
            )
        )

        for c in chunks
    ]

    matched = 0

    for expected in expected_chunks:

        expected_normalized = normalize(
            expected
        )

        if expected_normalized in retrieved_texts:

            matched += 1

    retrieval_coverage = (
        matched / len(expected_chunks)
        if expected_chunks
        else 0
    )

    return {

        "chunks_retrieved":
            len(chunks),

        "expected_chunks":
            len(expected_chunks),

        "retrieval_coverage":
            retrieval_coverage,

        "answer_non_empty":
            len(content) > 0,

        "correct":
            (
                retrieval_coverage > 0
                and len(content) > 0
            )
    }


# ============================================================
# MAIN EVALUATION
# ============================================================

def evaluate_row(row):

    intent = row[
        "intent"
    ]

    query = row[
        "query"
    ]

    patient_id = row[
        "patient_id"
    ]

    entity = row.get(
        "entity",
        ""
    )

    task = {

        "intent":
            intent,

        "entity":
            entity
    }

    # --------------------------------------------------------
    # Execute actual production handler
    # --------------------------------------------------------

    response = execute_handler(
        intent,
        task,
        patient_id,
        query
    )

    # --------------------------------------------------------
    # Evaluate according to handler
    # --------------------------------------------------------

    if intent == "LATEST_VALUE":

        evaluation = evaluate_latest(
            row,
            response
        )

    elif intent == "TREND":

        evaluation = evaluate_trend(
            row,
            response
        )

    elif intent == "ABNORMAL_LABS":

        evaluation = evaluate_abnormal(
            row,
            response
        )

    elif intent == "MEDICAL_DEFINITION":

        evaluation = evaluate_definition(
            row,
            response
        )

    elif intent == "GENERAL_RAG":

        evaluation = evaluate_rag(
            row,
            response
        )

    else:

        evaluation = {
            "correct": False
        }

    return {

        "query_id":
            row.get(
                "query_id",
                ""
            ),

        "patient_id":
            patient_id,

        "query":
            query,

        "intent":
            intent,

        "response_type":
            response.get(
                "type",
                ""
            ),

        "content":
            response.get(
                "content",
                ""
            ),

        "correct":
            evaluation.get(
                "correct",
                False
            ),

        **evaluation
    }


# ============================================================
# MAIN
# ============================================================

def main():

    os.makedirs(
        RESULT_DIR,
        exist_ok=True
    )

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        dataset = list(
            csv.DictReader(f)
        )

    print(
        "\n"
        + "=" * 70
    )

    print(
        "SPECIALIZED HANDLER EVALUATION"
    )

    print(
        "=" * 70
    )

    print(
        f"Total queries: {len(dataset)}"
    )

    results = []

    for index, row in enumerate(
        dataset,
        start=1
    ):

        print(
            f"\n[{index}/{len(dataset)}]"
        )

        print(
            "Intent:",
            row["intent"]
        )

        print(
            "Query:",
            row["query"]
        )

        try:

            result = evaluate_row(
                row
            )

            results.append(
                result
            )

            print(
                "Correct:",
                result["correct"]
            )

        except Exception as e:

            print(
                "ERROR:",
                e
            )

            results.append({

                "query_id":
                    row.get(
                        "query_id"
                    ),

                "patient_id":
                    row.get(
                        "patient_id"
                    ),

                "query":
                    row.get(
                        "query"
                    ),

                "intent":
                    row.get(
                        "intent"
                    ),

                "correct":
                    False,

                "error":
                    str(e)
            })

    # ========================================================
    # SAVE RESULTS
    # ========================================================

    fieldnames = []

    for row in results:

        for key in row:

            if key not in fieldnames:

                fieldnames.append(
                    key
                )

    with open(
        RESULT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            results
        )

    # ========================================================
    # SUMMARY BY HANDLER
    # ========================================================

    summary = {}

    intents = sorted(
        set(
            r.get(
                "intent",
                ""
            )
            for r in results
        )
    )

    for intent in intents:

        rows = [

            r
            for r in results

            if r.get(
                "intent"
            ) == intent
        ]

        correct = sum(
            1
            for r in rows
            if r.get(
                "correct"
            )
        )

        summary[intent] = {

            "total":
                len(rows),

            "correct":
                correct,

            "accuracy":
                (
                    correct / len(rows)
                    if rows
                    else 0
                )
        }

        # ----------------------------------------------------
        # Additional metrics
        # ----------------------------------------------------

        if intent == "LATEST_VALUE":

            summary[intent][
                "value_accuracy"
            ] = mean([
                r.get(
                    "value_correct",
                    False
                )
                for r in rows
            ])

            summary[intent][
                "date_accuracy"
            ] = mean([
                r.get(
                    "date_correct",
                    False
                )
                for r in rows
            ])

        elif intent == "TREND":

            summary[intent][
                "trend_accuracy"
            ] = mean([
                r.get(
                    "trend_correct",
                    False
                )
                for r in rows
            ])

            summary[intent][
                "value_accuracy"
            ] = mean([
                r.get(
                    "value_correct",
                    False
                )
                for r in rows
            ])

        elif intent == "ABNORMAL_LABS":

            summary[intent][
                "test_coverage"
            ] = mean([
                r.get(
                    "test_coverage",
                    0
                )
                for r in rows
            ])

        elif intent == "GENERAL_RAG":

            summary[intent][
                "retrieval_coverage"
            ] = mean([
                r.get(
                    "retrieval_coverage",
                    0
                )
                for r in rows
            ])

    # ========================================================
    # SAVE SUMMARY
    # ========================================================

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
    # PRINT
    # ========================================================

    print(
        "\n"
        + "=" * 70
    )

    print(
        "HANDLER EVALUATION RESULTS"
    )

    print(
        "=" * 70
    )

    for intent, values in summary.items():

        print(
            f"\n{intent}"
        )

        print(
            f"Queries: "
            f"{values['total']}"
        )

        print(
            f"Accuracy: "
            f"{values['accuracy']:.4f}"
        )

        if (
            "value_accuracy"
            in values
        ):

            print(
                f"Value accuracy: "
                f"{values['value_accuracy']:.4f}"
            )

        if (
            "trend_accuracy"
            in values
        ):

            print(
                f"Trend accuracy: "
                f"{values['trend_accuracy']:.4f}"
            )

        if (
            "test_coverage"
            in values
        ):

            print(
                f"Test coverage: "
                f"{values['test_coverage']:.4f}"
            )

        if (
            "retrieval_coverage"
            in values
        ):

            print(
                f"Retrieval coverage: "
                f"{values['retrieval_coverage']:.4f}"
            )

    print(
        "\nSaved:"
    )

    print(
        RESULT_FILE
    )

    print(
        SUMMARY_FILE
    )


if __name__ == "__main__":
    main()