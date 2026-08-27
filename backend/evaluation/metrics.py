def accuracy(correct, total):
    if total == 0:
        return 0.0

    return correct / total


def precision_recall_f1(tp, fp, fn):
    precision = (
        tp / (tp + fp)
        if (tp + fp) > 0
        else 0.0
    )

    recall = (
        tp / (tp + fn)
        if (tp + fn) > 0
        else 0.0
    )

    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    return precision, recall, f1

# evaluation/metrics.py


def precision_at_k(
    retrieved,
    relevant,
    k
):
    """
    Precision@K

    retrieved:
        ordered list of retrieved chunk identifiers

    relevant:
        set of relevant chunk identifiers
    """

    if k <= 0:
        return 0.0

    retrieved_at_k = retrieved[:k]

    if not retrieved_at_k:
        return 0.0

    relevant_count = sum(
        1
        for item in retrieved_at_k
        if item in relevant
    )

    return relevant_count / k


def recall_at_k(
    retrieved,
    relevant,
    k
):
    """
    Recall@K
    """

    if not relevant:
        return 0.0

    retrieved_at_k = retrieved[:k]

    relevant_count = sum(
        1
        for item in retrieved_at_k
        if item in relevant
    )

    return relevant_count / len(relevant)


def hit_at_k(
    retrieved,
    relevant,
    k
):
    """
    Hit@K

    Returns 1 if at least one relevant
    item appears in top K.
    """

    retrieved_at_k = retrieved[:k]

    for item in retrieved_at_k:

        if item in relevant:
            return 1.0

    return 0.0


def reciprocal_rank(
    retrieved,
    relevant
):
    """
    Reciprocal Rank
    """

    for rank, item in enumerate(
        retrieved,
        start=1
    ):

        if item in relevant:

            return 1.0 / rank

    return 0.0


def mean(values):

    if not values:
        return 0.0

    return sum(values) / len(values)


def classification_metrics(
    y_true,
    y_pred,
    labels
):

    results = {}

    for label in labels:

        tp = 0
        fp = 0
        fn = 0

        for true, pred in zip(
            y_true,
            y_pred
        ):

            if (
                true == label
                and pred == label
            ):
                tp += 1

            elif (
                true != label
                and pred == label
            ):
                fp += 1

            elif (
                true == label
                and pred != label
            ):
                fn += 1

        precision = (
            tp / (tp + fp)
            if (tp + fp) > 0
            else 0.0
        )

        recall = (
            tp / (tp + fn)
            if (tp + fn) > 0
            else 0.0
        )

        f1 = (
            2 * precision * recall
            / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )

        results[label] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "true_positive": tp,
            "false_positive": fp,
            "false_negative": fn,
        }

    return results