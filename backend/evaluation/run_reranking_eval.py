# evaluation/run_reranking_eval.py

import csv
import json
import os
import time

from chatbot.rag.retriever import retrieve
from chatbot.rag.reranker import rerank

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

RESULT_DIR = "evaluation/results"

RESULT_FILE = (
    RESULT_DIR +
    "/reranking_results.csv"
)

SUMMARY_FILE = (
    RESULT_DIR +
    "/reranking_summary.json"
)


# ============================================================
# EVALUATION SETTINGS
# ============================================================

# Your retriever returns up to 20 chunks.
RETRIEVAL_K = 20

# Your reranker currently returns top 5.
RERANK_K = 5

# We compare both systems at top 5.
COMPARE_K = 5


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

    query = row["query"]

    patient_id = row["patient_id"]

    expected_chunks = (
        parse_expected_chunks(
            row["expected_chunk_texts"]
        )
    )

    expected_set = (
        build_relevant_set(
            expected_chunks
        )
    )

    # ========================================================
    # STEP 1 — HYBRID RETRIEVAL
    # ========================================================

    retrieval_start = (
        time.perf_counter()
    )

    retrieved_chunks = retrieve(
        query=query,
        patient_id=patient_id,
    )

    retrieval_end = (
        time.perf_counter()
    )

    retrieval_latency = (
        retrieval_end
        - retrieval_start
    )

    # --------------------------------------------------------
    # Normalize retrieved text
    # --------------------------------------------------------

    retrieved_texts = (
        get_retrieved_texts(
            retrieved_chunks
        )
    )

    # ========================================================
    # STEP 2 — RERANK
    # ========================================================

    rerank_start = (
        time.perf_counter()
    )

    reranked_chunks = rerank(
        query=query,
        chunks=retrieved_chunks,
        top_k=RERANK_K,
    )

    rerank_end = (
        time.perf_counter()
    )

    rerank_latency = (
        rerank_end
        - rerank_start
    )

    # --------------------------------------------------------
    # Normalize reranked text
    # --------------------------------------------------------

    reranked_texts = (
        get_retrieved_texts(
            reranked_chunks
        )
    )

    # ========================================================
    # RESULT OBJECT
    # ========================================================

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

        "retrieval_latency_seconds":
            retrieval_latency,

        "reranking_latency_seconds":
            rerank_latency,

        "total_latency_seconds":
            retrieval_latency
            + rerank_latency,

        "retrieved_count":
            len(retrieved_chunks),

        "reranked_count":
            len(reranked_chunks),
    }

    # ========================================================
    # BEFORE RERANKING
    # ========================================================

    for k in [1, 3, 5]:

        result[
            f"before_precision@{k}"
        ] = precision_at_k(
            retrieved_texts,
            expected_set,
            k
        )

        result[
            f"before_recall@{k}"
        ] = recall_at_k(
            retrieved_texts,
            expected_set,
            k
        )

        result[
            f"before_hit@{k}"
        ] = hit_at_k(
            retrieved_texts,
            expected_set,
            k
        )

    result[
        "before_mrr"
    ] = reciprocal_rank(
        retrieved_texts,
        expected_set
    )

    # ========================================================
    # AFTER RERANKING
    # ========================================================

    for k in [1, 3, 5]:

        result[
            f"after_precision@{k}"
        ] = precision_at_k(
            reranked_texts,
            expected_set,
            k
        )

        result[
            f"after_recall@{k}"
        ] = recall_at_k(
            reranked_texts,
            expected_set,
            k
        )

        result[
            f"after_hit@{k}"
        ] = hit_at_k(
            reranked_texts,
            expected_set,
            k
        )

    result[
        "after_mrr"
    ] = reciprocal_rank(
        reranked_texts,
        expected_set
    )

    # ========================================================
    # RANK INFORMATION
    # ========================================================

    before_relevant_ranks = []

    for rank, text in enumerate(
        retrieved_texts,
        start=1
    ):

        if text in expected_set:

            before_relevant_ranks.append(
                rank
            )

    after_relevant_ranks = []

    for rank, text in enumerate(
        reranked_texts,
        start=1
    ):

        if text in expected_set:

            after_relevant_ranks.append(
                rank
            )

    result[
        "before_relevant_ranks"
    ] = json.dumps(
        before_relevant_ranks
    )

    result[
        "after_relevant_ranks"
    ] = json.dumps(
        after_relevant_ranks
    )

    # ========================================================
    # STORE TOP CHUNKS
    # ========================================================

    before_chunks = []

    for rank, chunk in enumerate(
        retrieved_chunks[:COMPARE_K],
        start=1
    ):

        text = chunk.get(
            "text",
            ""
        )

        normalized = (
            text.strip().lower()
        )

        before_chunks.append({

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
                in expected_set,
        })

    after_chunks = []

    for rank, chunk in enumerate(
        reranked_chunks[:COMPARE_K],
        start=1
    ):

        text = chunk.get(
            "text",
            ""
        )

        normalized = (
            text.strip().lower()
        )

        after_chunks.append({

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
                in expected_set,
        })

    result[
        "before_top5"
    ] = json.dumps(
        before_chunks,
        ensure_ascii=False
    )

    result[
        "after_top5"
    ] = json.dumps(
        after_chunks,
        ensure_ascii=False
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
        "RERANKING EVALUATION"
    )

    print(
        "=" * 70
    )

    print(
        f"Total queries: {len(dataset)}"
    )

    print(
        "\nPipeline:"
    )

    print(
        "Hybrid Retrieval → "
        "20 candidates → "
        "CrossEncoder → Top 5"
    )

    results = []

    # ========================================================
    # RUN ALL QUERIES
    # ========================================================

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

        try:

            result = evaluate_query(
                row
            )

            results.append(
                result
            )

            print(
                "Before MRR:",
                f"{result['before_mrr']:.4f}"
            )

            print(
                "After MRR:",
                f"{result['after_mrr']:.4f}"
            )

            print(
                "Before Recall@5:",
                f"{result['before_recall@5']:.4f}"
            )

            print(
                "After Recall@5:",
                f"{result['after_recall@5']:.4f}"
            )

            print(
                "Rerank latency:",
                f"{result['reranking_latency_seconds']:.3f}s"
            )

        except Exception as e:

            print(
                "ERROR:",
                e
            )

            results.append({

                "query_id":
                    row["query_id"],

                "patient_id":
                    row["patient_id"],

                "query":
                    row["query"],

                "error":
                    str(e)
            })

    # ========================================================
    # SUCCESSFUL RESULTS
    # ========================================================

    successful = [

        r
        for r in results
        if "error" not in r
    ]

    # ========================================================
    # SUMMARY
    # ========================================================

    summary = {

        "total_queries":
            len(dataset),

        "successful_queries":
            len(successful),

        "failed_queries":
            len(dataset)
            - len(successful),

        "retrieval_k":
            RETRIEVAL_K,

        "reranking_k":
            RERANK_K,
    }

    # ========================================================
    # AGGREGATE BEFORE / AFTER
    # ========================================================

    for k in [1, 3, 5]:

        summary[
            f"before_precision@{k}"
        ] = mean([
            r[
                f"before_precision@{k}"
            ]
            for r in successful
        ])

        summary[
            f"after_precision@{k}"
        ] = mean([
            r[
                f"after_precision@{k}"
            ]
            for r in successful
        ])

        summary[
            f"before_recall@{k}"
        ] = mean([
            r[
                f"before_recall@{k}"
            ]
            for r in successful
        ])

        summary[
            f"after_recall@{k}"
        ] = mean([
            r[
                f"after_recall@{k}"
            ]
            for r in successful
        ])

        summary[
            f"before_hit@{k}"
        ] = mean([
            r[
                f"before_hit@{k}"
            ]
            for r in successful
        ])

        summary[
            f"after_hit@{k}"
        ] = mean([
            r[
                f"after_hit@{k}"
            ]
            for r in successful
        ])

    summary[
        "before_MRR"
    ] = mean([
        r["before_mrr"]
        for r in successful
    ])

    summary[
        "after_MRR"
    ] = mean([
        r["after_mrr"]
        for r in successful
    ])

    summary[
        "mean_retrieval_latency_seconds"
    ] = mean([
        r[
            "retrieval_latency_seconds"
        ]
        for r in successful
    ])

    summary[
        "mean_reranking_latency_seconds"
    ] = mean([
        r[
            "reranking_latency_seconds"
        ]
        for r in successful
    ])

    summary[
        "mean_total_latency_seconds"
    ] = mean([
        r[
            "total_latency_seconds"
        ]
        for r in successful
    ])

    # ========================================================
    # IMPROVEMENT
    # ========================================================

    summary[
        "MRR_improvement"
    ] = (
        summary["after_MRR"]
        - summary["before_MRR"]
    )

    summary[
        "MRR_improvement_percent"
    ] = (
        (
            summary["after_MRR"]
            - summary["before_MRR"]
        )
        / summary["before_MRR"]
        * 100
        if summary["before_MRR"] > 0
        else 0
    )

    summary[
        "recall@5_improvement"
    ] = (
        summary["after_recall@5"]
        - summary["before_recall@5"]
    )

    summary[
        "precision@5_improvement"
    ] = (
        summary["after_precision@5"]
        - summary["before_precision@5"]
    )

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

            "before_MRR":
                mean([
                    r["before_mrr"]
                    for r in intent_rows
                ]),

            "after_MRR":
                mean([
                    r["after_mrr"]
                    for r in intent_rows
                ]),

            "before_recall@5":
                mean([
                    r["before_recall@5"]
                    for r in intent_rows
                ]),

            "after_recall@5":
                mean([
                    r["after_recall@5"]
                    for r in intent_rows
                ]),

            "before_precision@5":
                mean([
                    r["before_precision@5"]
                    for r in intent_rows
                ]),

            "after_precision@5":
                mean([
                    r["after_precision@5"]
                    for r in intent_rows
                ]),
        }

    # ========================================================
    # SAVE CSV
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
    # PRINT RESULTS
    # ========================================================

    print(
        "\n"
        + "=" * 70
    )

    print(
        "FINAL RERANKING RESULTS"
    )

    print(
        "=" * 70
    )

    print(
        "\nBefore reranking:"
    )

    print(
        f"MRR: "
        f"{summary['before_MRR']:.4f}"
    )

    print(
        f"Recall@5: "
        f"{summary['before_recall@5']:.4f}"
    )

    print(
        f"Precision@5: "
        f"{summary['before_precision@5']:.4f}"
    )

    print(
        "\nAfter reranking:"
    )

    print(
        f"MRR: "
        f"{summary['after_MRR']:.4f}"
    )

    print(
        f"Recall@5: "
        f"{summary['after_recall@5']:.4f}"
    )

    print(
        f"Precision@5: "
        f"{summary['after_precision@5']:.4f}"
    )

    print(
        "\nImprovement:"
    )

    print(
        f"MRR improvement: "
        f"{summary['MRR_improvement']:.4f}"
    )

    print(
        f"MRR improvement %: "
        f"{summary['MRR_improvement_percent']:.2f}%"
    )

    print(
        f"Recall@5 improvement: "
        f"{summary['recall@5_improvement']:.4f}"
    )

    print(
        f"Precision@5 improvement: "
        f"{summary['precision@5_improvement']:.4f}"
    )

    print(
        "\nLatency:"
    )

    print(
        f"Retrieval: "
        f"{summary['mean_retrieval_latency_seconds']:.4f}s"
    )

    print(
        f"Reranking: "
        f"{summary['mean_reranking_latency_seconds']:.4f}s"
    )

    print(
        f"Total: "
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