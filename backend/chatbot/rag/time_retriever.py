from .vector_store import (
    get_lab_chunks,
    get_all_patient_chunks
)
def get_latest_lab(
    patient_id,
    test_name
):

    chunks = get_lab_chunks(
        patient_id,
        test_name
    )

    if not chunks:
        return None

    chunks.sort(
        key=lambda c:
            c.payload.get(
                "report_date",
                ""
            ),
        reverse=True
    )

    return chunks[0]

def get_lab_history(
    patient_id,
    test_name
):

    chunks = get_lab_chunks(
        patient_id,
        test_name
    )

    history = []

    for c in chunks:

        md = c.payload.get(
            "metadata",
            {}
        )

        history.append({
            "date":
                c.payload.get(
                    "report_date"
                ),

            "value":
                md.get("value"),

            "status":
                md.get("status")
        })

    history.sort(
        key=lambda x:
            x["date"]
    )

    return history
def get_abnormal_labs(
    patient_id
):

    chunks = get_all_patient_chunks(
        patient_id
    )

    abnormal = []

    for c in chunks:

        md = c.payload.get(
            "metadata",
            {}
        )

        status = (
            md.get(
                "status",
                ""
            )
            .upper()
        )

        if status in [
            "HIGH",
            "LOW",
            "ABNORMAL"
        ]:

            abnormal.append(c)

    return abnormal

