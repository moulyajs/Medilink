# evaluation/run_ablation.py

import csv
import json
import os
import time

from chatbot.rag.embeddings import get_embedding

from chatbot.vector_store import (
    search_qdrant,
    keyword_search_qdrant,
)

from chatbot.keyword_search import extract_keywords

from chatbot.rrf import rrf_fusion

from chatbot.hybrid_search import apply_recency

from chatbot.reranker import rerank

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
    "/ablation_results.csv"
)

SUMMARY_FILE = (
    RESULT_DIR +
    "/ablation_summary.json"
)


# ============================================================
# CONFIGURATIONS
# ============================================================

CONFIGURATIONS = {

    # --------------------------------------------------------
    # Dense retrieval only
    # --------------------------------------------------------

    "DENSE_ONLY": {

        "vector": True,

        "keyword": False,

        "rrf": False,

        "recency": False,

        "reranker": False,
    },

    # --------------------------------------------------------
    # Keyword retrieval only
    # --------------------------------------------------------

    "KEYWORD_ONLY": {

        "vector": False,

        "keyword": True,

        "rrf": False,

        "recency": False,

        "reranker": False,
    },

    # --------------------------------------------------------
    # Dense + Keyword + RRF
    # --------------------------------------------------------

    "HYBRID_RRF": {

        "vector": True,

        "keyword": True,

        "rrf": True,

        "recency": False,

        "reranker": False,
    },

    # --------------------------------------------------------
    # Hybrid + Recency
    # --------------------------------------------------------

    "HYBRID_RRF_RECENCY": {

        "vector": True,

        "keyword": True,

        "rrf": True,

        "recency": True,

        "reranker": False,
    },

    # --------------------------------------------------------
    # Full retrieval pipeline
    # --------------------------------------------------------

    "FULL_SYSTEM": {

        "vector": True,

        "keyword": True,

        "rrf": True,

        "recency": True,

        "reranker": True,
    },
}


# ============================================================
# SEARCH CONFIG
# ============================================================

VECTOR_LIMIT = 30

KEYWORD_LIMIT = 10

FINAL_LIMIT = 20

RERANK_LIMIT = 5


# ============================================================
# BUILD VECTOR CHUNKS
# ============================================================

def convert_vector_results(
    results
):

    chunks = []

    for r in results:

        chunks.append({

            "chunk_id":
                r.payload.get(
                    "chunk_id"
                ),

            "text":
                r.payload.get(
                    "text"
                ),

            "patient_id":
                r.payload.get(
                    "patient_id"
                ),

            "chunk_type":
                r.payload.get(
                    "chunk_type"
                ),

            "chunk_level":
                r.payload.get(
                    "chunk_level"
                ),

            "report_type":
                r.payload.get(
                    "report_type"
                ),

            "document_id":
                r.payload.get(
                    "document_id"
                ),

            "report_date":
                r.payload.get(
                    "report_date"
                ),

            "metadata":
                r.payload.get(
                    "metadata",
                    {}
                ),

            "score":
                r.score,
        })

    return chunks


# ============================================================
# BUILD KEYWORD CHUNKS
# ============================================================

def get_keyword_chunks(
    query,
    patient_id,
    chunk_types=None
):

    keywords = extract_keywords(
        query
    )

    print(
        "KEYWORDS:",
        keywords
    )

    chunks = []

    for keyword in keywords:

        matches = keyword_search_qdrant(

            patient_id,

            keyword,

            chunk_types=
                chunk_types,

            limit=
                KEYWORD_LIMIT,
        )

        for r in matches:

            chunks.append({

                "chunk_id":
                    r.payload.get(
                        "chunk_id"
                    ),

                "text":
                    r.payload.get(
                        "text"
                    ),

                "patient_id":
                    r.payload.get(
                        "patient_id"
                    ),

                "chunk_type":
                    r.payload.get(
                        "chunk_type"
                    ),

                "chunk_level":
                    r.payload.get(
                        "chunk_level"
                    ),

                "report_type":
                    r.payload.get(
                        "report_type"
                    ),

                "document_id":
                    r.payload.get(
                        "document_id"
                    ),

                "report_date":
                    r.payload.get(
                        "report_date"
                    ),

                "metadata":
                    r.payload.get(
                        "metadata",
                        {}
                    ),

                "score":
                    1.0,
            })

    return chunks


# ============================================================
# EVALUATION RETRIEVER
# ============================================================

def ablation_retrieve(
    query,
    patient_id,
    task,
    config
):

    chunk_types = None

    # --------------------------------------------------------
    # Same routing behaviour as your production retriever
    # --------------------------------------------------------

    if task:

        intent = task.get(
            "intent"
        )

        if intent in [

            "LATEST_VALUE",

            "TREND",

            "ABNORMAL_LABS",
        ]:

            chunk_types = [

                "lab_row",

                "lab_summary",
            ]

    # ========================================================
    # VECTOR SEARCH
    # ========================================================

    vector_chunks = []

    if config["vector"]:

        query_embedding = get_embedding(
            query
        )

        vector_results = search_qdrant(

            query_embedding=
                query_embedding,

            patient_id=
                patient_id,

            chunk_types=
                chunk_types,

            limit=
                VECTOR_LIMIT,
        )

        vector_chunks = (
            convert_vector_results(
                vector_results
            )
        )

    # ========================================================
    # KEYWORD SEARCH
    # ========================================================

    keyword_chunks = []

    if config["keyword"]:

        keyword_chunks = (
            get_keyword_chunks(

                query,

                patient_id,

                chunk_types
            )
        )

    # ========================================================
    # COMBINE
    # ========================================================

    # --------------------------------------------------------
    # Both vector and keyword
    # --------------------------------------------------------

    if (
        config["vector"]
        and config["keyword"]
    ):

        if config["rrf"]:

            fused = rrf_fusion(

                vector_chunks,

                keyword_chunks
            )

        else:

            # ------------------------------------------------
            # No RRF:
            # concatenate and remove duplicate IDs.
            # ------------------------------------------------

            combined = (
                vector_chunks
                + keyword_chunks
            )

            seen = set()

            fused = []

            for chunk in combined:

                chunk_id = (
                    chunk.get(
                        "chunk_id"
                    )
                )

                if chunk_id in seen:
                    continue

                seen.add(
                    chunk_id
                )

                fused.append({

                    "chunk":
                        chunk,

                    "score":
                        chunk.get(
                            "score",
                            0
                        )
                })

    # --------------------------------------------------------
    # Vector only
    # --------------------------------------------------------

    elif config["vector"]:

        fused = [

            {
                "chunk":
                    chunk,

                "score":
                    chunk.get(
                        "score",
                        0
                    )
            }

            for chunk
            in vector_chunks
        ]

    # --------------------------------------------------------
    # Keyword only
    # --------------------------------------------------------

    elif config["keyword"]:

        fused = [

            {
                "chunk":
                    chunk,

                "score":
                    chunk.get(
                        "score",
                        0
                    )
            }

            for chunk
            in keyword_chunks
        ]

    else:

        fused = []

    # ========================================================
    # RECENCY
    # ========================================================

    if config["recency"]:

        final_chunks = apply_recency(
            fused
        )

    else:

        final_chunks = [

            item["chunk"]

            for item
            in fused
        ]

    # ========================================================
    # LIMIT CANDIDATES
    # ========================================================

    final_chunks = (
        final_chunks[:FINAL_LIMIT]
    )

    # ========================================================
    # RERANK
    # ========================================================

    if config["reranker"]:

        final_chunks = rerank(

            query,

            final_chunks,

            top_k=
                RERANK_LIMIT
        )

    return final_chunks


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
# EVALUATE ONE QUERY
# ============================================================

def evaluate_query(
    row,
    config
):

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
    # Query task
    # --------------------------------------------------------

    task = {

        "intent":
            row.get(
                "intent",
                ""
            ),

        "entity":
            row.get(
                "entity",
                ""
            )
    }

    # --------------------------------------------------------
    # Retrieval
    # --------------------------------------------------------

    start = (
        time.perf_counter()
    )

    retrieved = ablation_retrieve(

        query=

            query,

        patient_id=

            patient_id,

        task=

            task,

        config=

            config,
    )

    end = (
        time.perf_counter()
    )

    latency = (
        end - start
    )

    retrieved_texts = (
        get_retrieved_texts(
            retrieved
        )
    )

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    result = {

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
            row.get(
                "intent",
                ""
            ),

        "latency_seconds":
            latency,

        "retrieved_count":
            len(retrieved),

        "precision@1":
            precision_at_k(

                retrieved_texts,

                expected_set,

                1
            ),

        "precision@3":
            precision_at_k(

                retrieved_texts,

                expected_set,

                3
            ),

        "precision@5":
            precision_at_k(

                retrieved_texts,

                expected_set,

                5
            ),

        "recall@1":
            recall_at_k(

                retrieved_texts,

                expected_set,

                1
            ),

        "recall@3":
            recall_at_k(

                retrieved_texts,

                expected_set,

                3
            ),

        "recall@5":
            recall_at_k(

                retrieved_texts,

                expected_set,

                5
            ),

        "hit@1":
            hit_at_k(

                retrieved_texts,

                expected_set,

                1
            ),

        "hit@3":
            hit_at_k(

                retrieved_texts,

                expected_set,

                3
            ),

        "hit@5":
            hit_at_k(

                retrieved_texts,

                expected_set,

                5
            ),

        "MRR":
            reciprocal_rank(

                retrieved_texts,

                expected_set
            ),
    }

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
        + "=" * 80
    )

    print(
        "ABLATION STUDY"
    )

    print(
        "=" * 80
    )

    print(
        f"Queries: {len(dataset)}"
    )

    all_results = []

    summary = {}

    # ========================================================
    # RUN EACH CONFIGURATION
    # ========================================================

    for config_name, config in (
        CONFIGURATIONS.items()
    ):

        print(
            "\n"
            + "=" * 80
        )

        print(
            "CONFIGURATION:",
            config_name
        )

        print(
            "=" * 80
        )

        configuration_results = []

        for index, row in enumerate(
            dataset,
            start=1
        ):

            print(
                f"\n[{index}/{len(dataset)}]"
            )

            print(
                row["query"]
            )

            try:

                result = evaluate_query(

                    row,

                    config
                )

                result[
                    "configuration"
                ] = config_name

                configuration_results.append(
                    result
                )

                all_results.append(
                    result
                )

            except Exception as e:

                print(
                    "ERROR:",
                    e
                )

        # ====================================================
        # AGGREGATE
        # ====================================================

        summary[
            config_name
        ] = {

            "queries":
                len(
                    configuration_results
                ),

            "precision@1":
                mean([
                    r["precision@1"]
                    for r
                    in configuration_results
                ]),

            "precision@3":
                mean([
                    r["precision@3"]
                    for r
                    in configuration_results
                ]),

            "precision@5":
                mean([
                    r["precision@5"]
                    for r
                    in configuration_results
                ]),

            "recall@1":
                mean([
                    r["recall@1"]
                    for r
                    in configuration_results
                ]),

            "recall@3":
                mean([
                    r["recall@3"]
                    for r
                    in configuration_results
                ]),

            "recall@5":
                mean([
                    r["recall@5"]
                    for r
                    in configuration_results
                ]),

            "hit@1":
                mean([
                    r["hit@1"]
                    for r
                    in configuration_results
                ]),

            "hit@3":
                mean([
                    r["hit@3"]
                    for r
                    in configuration_results
                ]),

            "hit@5":
                mean([
                    r["hit@5"]
                    for r
                    in configuration_results
                ]),

            "MRR":
                mean([
                    r["MRR"]
                    for r
                    in configuration_results
                ]),

            "mean_latency_seconds":
                mean([
                    r["latency_seconds"]
                    for r
                    in configuration_results
                ]),
        }

    # ========================================================
    # SAVE QUERY RESULTS
    # ========================================================

    with open(
        RESULT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        fieldnames = [

            "configuration",

            "query_id",

            "patient_id",

            "query",

            "intent",

            "latency_seconds",

            "retrieved_count",

            "precision@1",

            "precision@3",

            "precision@5",

            "recall@1",

            "recall@3",

            "recall@5",

            "hit@1",

            "hit@3",

            "hit@5",

            "MRR",
        ]

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            all_results
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
    # PRINT SUMMARY TABLE
    # ========================================================

    print(
        "\n"
        + "=" * 100
    )

    print(
        "ABLATION SUMMARY"
    )

    print(
        "=" * 100
    )

    print(
        f"{'Configuration':<25}"
        f"{'P@5':>10}"
        f"{'R@5':>10}"
        f"{'Hit@5':>10}"
        f"{'MRR':>10}"
        f"{'Latency':>12}"
    )

    print(
        "-" * 100
    )

    for name, values in (
        summary.items()
    ):

        print(
            f"{name:<25}"
            f"{values['precision@5']:>10.4f}"
            f"{values['recall@5']:>10.4f}"
            f"{values['hit@5']:>10.4f}"
            f"{values['MRR']:>10.4f}"
            f"{values['mean_latency_seconds']:>12.4f}"
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