from datetime import datetime
import math


def calculate_recency_score(report_date):

    if not report_date:
        return 0.0

    report_date = str(report_date).strip()

    report_dt = None

    for fmt in (
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%Y/%m/%d"
    ):
        try:
            report_dt = datetime.strptime(
                report_date,
                fmt
            )
            break
        except ValueError:
            pass

    if report_dt is None:
        return 0.0

    days_old = (
        datetime.now() - report_dt
    ).days

    # Future date protection
    if days_old < 0:
        days_old = 0

    # Exponential decay
    score = math.exp(
        -days_old / 365
    )

    return round(score, 4)