# evaluation/run_retrieval_eval.py

import csv
import json
import os
import time

from chatbot.rag.retriever import retrieve

from evaluation.evaluation_utils import (
    parse_expected_chunks,
    get_retrieved_texts,
    build_relevant_set,
)

from evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    hit_at_k,
    reciprocal_rank,
    mean,
)


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_PATH = (
    "final_evaluation_datasets/"
    "retrieval_dataset.csv"
)

RESULT_DIR = (
    "evaluation/results"
)

RESULT_FILE = (
    RESULT_DIR +
    "/retrieval_results.csv"
)

SUMMARY_FILE = (
    RESULT_DIR +
    "/retrieval_summary.json"
)


# Evaluate these values of K
K_VALUES = [
    1,
    3,
    5,
    10,
    20
]


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        return list(reader)


# ============================================================
# EVALUATE ONE QUERY
# ============================================================

def evaluate_query(row):

    query = row[
        "query"
    ]

    patient_id = row[
        "patient_id"
    ]

    expected_chunks = (
        parse_expected_chunks(
            row[
                "expected_chunk_texts"
            ]
        )
    )

    expected_set = (
        build_relevant_set(
            expected_chunks
        )
    )

    # --------------------------------------------------------
    # Retrieval
    # --------------------------------------------------------

    start_time = time.perf_counter()

    retrieved_chunks = retrieve(
        query=query,
        patient_id=patient_id,
    )

    end_time = time.perf_counter()

    latency = (
        end_time - start_time
    )

    # --------------------------------------------------------
    # Retrieved texts
    # --------------------------------------------------------

    retrieved_texts = (
        get_retrieved_texts(
            retrieved_chunks
        )
    )

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    result = {

        "query_id":
            row["query_id"],

        "patient_id":
            patient_id,

        "query":
            query,

        "intent":
            row.get(
                "intent",
                ""
            ),

        "expected_count":
            len(expected_chunks),

        "retrieved_count":
            len(retrieved_chunks),

        "latency_seconds":
            latency,
    }

    # --------------------------------------------------------
    # K metrics
    # --------------------------------------------------------

    for k in K_VALUES:

        result[
            f"precision@{k}"
        ] = precision_at_k(
            retrieved_texts,
            expected_set,
            k
        )

        result[
            f"recall@{k}"
        ] = recall_at_k(
            retrieved_texts,
            expected_set,
            k
        )

        result[
            f"hit@{k}"
        ] = hit_at_k(
            retrieved_texts,
            expected_set,
            k
        )

    # --------------------------------------------------------
    # MRR
    # --------------------------------------------------------

    result[
        "reciprocal_rank"
    ] = reciprocal_rank(
        retrieved_texts,
        expected_set
    )

    # --------------------------------------------------------
    # Top retrieved chunks
    # --------------------------------------------------------

    top_chunks = []

    for rank, chunk in enumerate(
        retrieved_chunks,
        start=1
    ):

        text = chunk.get(
            "text",
            ""
        )

        normalized = (
            text.strip().lower()
        )

        top_chunks.append({

            "rank":
                rank,

            "text":
                text,

            "chunk_type":
                chunk.get(
                    "chunk_type"
                ),

            "document_id":
                chunk.get(
                    "document_id"
                ),

            "report_date":
                chunk.get(
                    "report_date"
                ),

            "is_relevant":
                normalized
                in expected_set
        })

    result[
        "retrieved_chunks"
    ] = json.dumps(
        top_chunks,
        ensure_ascii=False
    )

    # --------------------------------------------------------
    # Relevant ranks
    # --------------------------------------------------------

    relevant_ranks = []

    for rank, text in enumerate(
        retrieved_texts,
        start=1
    ):

        if text in expected_set:

            relevant_ranks.append(
                rank
            )

    result[
        "relevant_ranks"
    ] = json.dumps(
        relevant_ranks
    )

    return result


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
        "RETRIEVAL EVALUATION"
    )

    print(
        "=" * 70
    )

    print(
        f"Total queries: {len(dataset)}"
    )

    results = []

    # --------------------------------------------------------
    # Run every query
    # --------------------------------------------------------

    for index, row in enumerate(
        dataset,
        start=1
    ):

        print(
            f"\n[{index}/{len(dataset)}]"
        )

        print(
            "Query:",
            row["query"]
        )

        print(
            "Patient:",
            row["patient_id"]
        )

        try:

            result = evaluate_query(
                row
            )

            results.append(
                result
            )

            print(
                "MRR:",
                f"{result['reciprocal_rank']:.4f}"
            )

            print(
                "Recall@5:",
                f"{result['recall@5']:.4f}"
            )

            print(
                "Hit@5:",
                f"{result['hit@5']:.0f}"
            )

            print(
                "Latency:",
                f"{result['latency_seconds']:.3f}s"
            )

        except Exception as e:

            print(
                "ERROR:",
                e
            )

            results.append({

                "query_id":
                    row["query"],

                "patient_id":
                    row["patient_id"],

                "query":
                    row["query"],

                "error":
                    str(e)
            })

    # ========================================================
    # SUMMARY
    # ========================================================

    successful = [
        r
        for r in results
        if "error" not in r
    ]

    summary = {

        "total_queries":
            len(dataset),

        "successful_queries":
            len(successful),

        "failed_queries":
            len(dataset)
            - len(successful),
    }

    # --------------------------------------------------------
    # Calculate aggregate metrics
    # --------------------------------------------------------

    for k in K_VALUES:

        summary[
            f"precision@{k}"
        ] = mean([
            r[
                f"precision@{k}"
            ]
            for r in successful
        ])

        summary[
            f"recall@{k}"
        ] = mean([
            r[
                f"recall@{k}"
            ]
            for r in successful
        ])

        summary[
            f"hit@{k}"
        ] = mean([
            r[
                f"hit@{k}"
            ]
            for r in successful
        ])

    summary[
        "MRR"
    ] = mean([
        r[
            "reciprocal_rank"
        ]
        for r in successful
    ])

    summary[
        "mean_latency_seconds"
    ] = mean([
        r[
            "latency_seconds"
        ]
        for r in successful
    ])

    # ========================================================
    # BY INTENT
    # ========================================================

    intents = sorted(
        set(
            r.get(
                "intent",
                ""
            )
            for r in successful
        )
    )

    summary[
        "by_intent"
    ] = {}

    for intent in intents:

        if not intent:
            continue

        intent_rows = [
            r
            for r in successful
            if r.get(
                "intent",
                ""
            ) == intent
        ]

        summary[
            "by_intent"
        ][intent] = {

            "queries":
                len(intent_rows),

            "recall@5":
                mean([
                    r["recall@5"]
                    for r in intent_rows
                ]),

            "hit@5":
                mean([
                    r["hit@5"]
                    for r in intent_rows
                ]),

            "MRR":
                mean([
                    r["reciprocal_rank"]
                    for r in intent_rows
                ]),

            "mean_latency":
                mean([
                    r[
                        "latency_seconds"
                    ]
                    for r in intent_rows
                ])
        }

    # ========================================================
    # SAVE QUERY RESULTS
    # ========================================================

    if results:

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
    # PRINT FINAL RESULTS
    # ========================================================

    print(
        "\n"
        + "=" * 70
    )

    print(
        "FINAL RETRIEVAL RESULTS"
    )

    print(
        "=" * 70
    )

    for k in K_VALUES:

        print(
            f"\nK = {k}"
        )

        print(
            f"Precision@{k}: "
            f"{summary[f'precision@{k}']:.4f}"
        )

        print(
            f"Recall@{k}:    "
            f"{summary[f'recall@{k}']:.4f}"
        )

        print(
            f"Hit@{k}:       "
            f"{summary[f'hit@{k}']:.4f}"
        )

    print(
        "\nMRR:",
        f"{summary['MRR']:.4f}"
    )

    print(
        "Mean latency:",
        f"{summary['mean_latency_seconds']:.4f}s"
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