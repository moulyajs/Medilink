# evaluation/evaluation_utils.py

import json
import re


def normalize_text(text):
    """
    Normalize chunk text so that tiny formatting
    differences do not cause a false mismatch.
    """

    if text is None:
        return ""

    text = str(text)

    text = text.strip()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.lower()


def parse_expected_chunks(
    value
):
    """
    Convert expected_chunk_texts from CSV
    into a Python list.
    """

    if value is None:
        return []

    if isinstance(value, list):
        return value

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


def get_retrieved_texts(
    chunks
):

    return [
        normalize_text(
            chunk.get("text")
        )
        for chunk in chunks
        if chunk.get("text")
    ]


def build_relevant_set(
    expected_chunks
):

    return {
        normalize_text(
            chunk
        )
        for chunk in expected_chunks
        if chunk
    }


def calculate_ranked_metrics(
    retrieved_chunks,
    expected_chunks,
    k_values
):

    retrieved = get_retrieved_texts(
        retrieved_chunks
    )

    relevant = build_relevant_set(
        expected_chunks
    )

    metrics = {}

    for k in k_values:

        metrics[
            f"precision@{k}"
        ] = precision_at_k_local(
            retrieved,
            relevant,
            k
        )

        metrics[
            f"recall@{k}"
        ] = recall_at_k_local(
            retrieved,
            relevant,
            k
        )

        metrics[
            f"hit@{k}"
        ] = hit_at_k_local(
            retrieved,
            relevant,
            k
        )

    metrics[
        "reciprocal_rank"
    ] = reciprocal_rank_local(
        retrieved,
        relevant
    )

    return metrics


def precision_at_k_local(
    retrieved,
    relevant,
    k
):

    if k <= 0:
        return 0.0

    top_k = retrieved[:k]

    if not top_k:
        return 0.0

    count = sum(
        1
        for item in top_k
        if item in relevant
    )

    return count / k


def recall_at_k_local(
    retrieved,
    relevant,
    k
):

    if not relevant:
        return 0.0

    top_k = retrieved[:k]

    count = sum(
        1
        for item in top_k
        if item in relevant
    )

    return count / len(relevant)


def hit_at_k_local(
    retrieved,
    relevant,
    k
):

    for item in retrieved[:k]:

        if item in relevant:
            return 1.0

    return 0.0


def reciprocal_rank_local(
    retrieved,
    relevant
):

    for rank, item in enumerate(
        retrieved,
        start=1
    ):

        if item in relevant:
            return 1.0 / rank

    return 0.0