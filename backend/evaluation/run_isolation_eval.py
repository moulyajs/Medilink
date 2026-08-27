import csv
import json
import os

from chatbot.rag.retriever import retrieve


DATASET_PATH = (
    "final_evaluation_datasets/"
    "patient_isolation_dataset.csv"
)

RESULT_DIR = "evaluation/results"

RESULT_FILE = (
    RESULT_DIR +
    "/patient_isolation_results.csv"
)


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

    results = []

    for index, row in enumerate(
        dataset,
        start=1
    ):

        patient_id = row[
            "patient_id"
        ]

        query = row[
            "query"
        ]

        print(
            f"\n[{index}/{len(dataset)}]"
        )

        print(
            "Patient:",
            patient_id
        )

        print(
            "Query:",
            query
        )

        try:

            chunks = retrieve(
                query=query,
                patient_id=patient_id
            )

            wrong_patient_chunks = []

            for chunk in chunks:

                chunk_patient = (
                    chunk.get(
                        "patient_id"
                    )
                )

                # Your current retrieve()
                # does NOT return patient_id.
                #
                # This will expose that issue.

                if (
                    chunk_patient
                    != patient_id
                ):

                    wrong_patient_chunks.append(
                        chunk
                    )

            isolated = (
                len(
                    wrong_patient_chunks
                ) == 0
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

                "retrieved_count":
                    len(chunks),

                "wrong_patient_count":
                    len(
                        wrong_patient_chunks
                    ),

                "isolated":
                    isolated,

                "chunks":
                    json.dumps(
                        chunks,
                        ensure_ascii=False
                    )
            })

        except Exception as e:

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

                "retrieved_count":
                    0,

                "wrong_patient_count":
                    -1,

                "isolated":
                    False,

                "chunks":
                    "",

                "error":
                    str(e)
            })

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
                "patient_id",
                "query",
                "retrieved_count",
                "wrong_patient_count",
                "isolated",
                "chunks"
            ]
        )

        writer.writeheader()

        writer.writerows(
            results
        )

    print(
        "\nSaved:",
        RESULT_FILE
    )


if __name__ == "__main__":
    main()