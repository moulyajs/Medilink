from .rrf import rrf_fusion
from .recency import calculate_recency_score


def apply_recency(
    fused_results
):

    rescored = []

    for item in fused_results:

        chunk = item["chunk"]

        semantic_score = item["score"]

        recency_score = (
            calculate_recency_score(
                chunk.get("report_date")
            )
        )

        final_score = (
            0.8 * semantic_score
            +
            0.2 * recency_score
        )
        """
        print(
    "\nDate:",
    chunk.get("report_date")
)

        print(
    "Semantic:",
    round(semantic_score,4)
)

        print(
    "Recency:",
    round(recency_score,4)
)

        print(
    "Final:",
    round(final_score,4)
)
"""

        chunk["hybrid_score"] = final_score

        rescored.append(chunk)

    rescored.sort(
        key=lambda x: x["hybrid_score"],
        reverse=True
    )
    """
    print("\n" + "="*80)
    print("AFTER RECENCY SORTING")
    print("="*80)

    for i, chunk in enumerate(
    rescored[:20],
    start=1
):

        print(
        f"\n[{i}] "
        f"Score={round(chunk['hybrid_score'],4)}"
    )

        print(
        chunk["report_date"]
    )

        print(
        chunk["text"][:200]
    )
    """
    
    return rescored