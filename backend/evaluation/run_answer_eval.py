import csv
import json
import os
import time

from chatbot.rag.query_parser import parse_query
from chatbot.rag.orchestrator import orchestrate


# ============================================================
# CONFIG
# ============================================================

DATASET_PATH = (
    "final_evaluation_datasets/"
    "final_answer_evaluation.csv"
)

RESULT_DIR = "evaluation/results"

RESULT_FILE = (
    RESULT_DIR +
    "/answer_results.csv"
)

SUMMARY_FILE = (
    RESULT_DIR +
    "/answer_summary.json"
)


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        return list(
            csv.DictReader(f)
        )


# ============================================================
# MAIN
# ============================================================

def main():

    os.makedirs(
        RESULT_DIR,
        exist_ok=True
    )

    dataset = load_dataset()

    print(
        "\n"
        + "=" * 70
    )

    print(
        "END-TO-END ANSWER EVALUATION"
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

        query = row["query"]

        patient_id = row[
            "patient_id"
        ]

        expected_intent = row.get(
            "intent",
            ""
        )

        print(
            f"\n[{index}/{len(dataset)}]"
        )

        print(
            "Query:",
            query
        )

        try:

            # =================================================
            # STEP 1 — PARSE
            # =================================================

            parse_start = (
                time.perf_counter()
            )

            parsed = parse_query(
                query
            )

            parse_end = (
                time.perf_counter()
            )

            parse_latency = (
                parse_end
                - parse_start
            )

            # =================================================
            # STEP 2 — ORCHESTRATE
            # =================================================

            answer_start = (
                time.perf_counter()
            )

            response = orchestrate(
                parsed=parsed,
                patient_id=patient_id,
                query=query
            )

            answer_end = (
                time.perf_counter()
            )

            answer_latency = (
                answer_end
                - answer_start
            )

            # -------------------------------------------------
            # Extract answer
            # -------------------------------------------------

            if isinstance(
                response,
                dict
            ):

                answer = response.get(
                    "content",
                    ""
                )

            else:

                answer = str(
                    response
                )

            # =================================================
            # STORE RESULT
            # =================================================

            result = {

                "query_id":
                    row.get(
                        "query_id",
                        str(index)
                    ),

                "patient_id":
                    patient_id,

                "query":
                    query,

                "expected_intent":
                    expected_intent,

                "parsed":
                    json.dumps(
                        parsed,
                        ensure_ascii=False
                    ),

                "answer":
                    answer,

                "parse_latency_seconds":
                    parse_latency,

                "answer_latency_seconds":
                    answer_latency,

                "total_latency_seconds":
                    parse_latency
                    + answer_latency,

                "error":
                    ""
            }

            results.append(
                result
            )

            print(
                "Answer:"
            )

            print(
                answer
            )

        except Exception as e:

            print(
                "ERROR:",
                e
            )

            results.append({

                "query_id":
                    row.get(
                        "query_id",
                        str(index)
                    ),

                "patient_id":
                    patient_id,

                "query":
                    query,

                "expected_intent":
                    expected_intent,

                "parsed":
                    "",

                "answer":
                    "",

                "parse_latency_seconds":
                    0,

                "answer_latency_seconds":
                    0,

                "total_latency_seconds":
                    0,

                "error":
                    str(e)
            })

    # ========================================================
    # SAVE CSV
    # ========================================================

    with open(
        RESULT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        fieldnames = [
            "query_id",
            "patient_id",
            "query",
            "expected_intent",
            "parsed",
            "answer",
            "parse_latency_seconds",
            "answer_latency_seconds",
            "total_latency_seconds",
            "error"
        ]

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            results
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    successful = [

        r
        for r in results

        if not r["error"]
    ]

    failed = [

        r
        for r in results

        if r["error"]
    ]

    def avg(
        values
    ):

        if not values:
            return 0

        return (
            sum(values)
            / len(values)
        )

    summary = {

        "total_queries":
            len(dataset),

        "successful_queries":
            len(successful),

        "failed_queries":
            len(failed),

        "mean_parse_latency_seconds":
            avg([
                r[
                    "parse_latency_seconds"
                ]
                for r in successful
            ]),

        "mean_answer_latency_seconds":
            avg([
                r[
                    "answer_latency_seconds"
                ]
                for r in successful
            ]),

        "mean_total_latency_seconds":
            avg([
                r[
                    "total_latency_seconds"
                ]
                for r in successful
            ])
    }

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
        "ANSWER EVALUATION COMPLETE"
    )

    print(
        "=" * 70
    )

    print(
        "Queries:",
        summary["total_queries"]
    )

    print(
        "Successful:",
        summary["successful_queries"]
    )

    print(
        "Failed:",
        summary["failed_queries"]
    )

    print(
        "Mean total latency:",
        f"{summary['mean_total_latency_seconds']:.4f}s"
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