# visit_grouper.py
from collections import defaultdict


def group_by_date(pages):
    """
    Groups OCR pages into visits based on detected dates.
    Pages without a date inherit the most recent valid date.
    """

    visits = defaultdict(list)
    last_date = None

    for idx, p in enumerate(pages):

        page_date = p.get("date")

        if page_date:
            last_date = page_date
        elif last_date is None:
            # fallback for initial pages without date
            last_date = f"UNKNOWN_VISIT_{idx+1}"

        visits[last_date].append(p)

    return visits