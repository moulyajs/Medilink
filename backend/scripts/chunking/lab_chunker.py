from .chunk_schema import create_chunk


def build_lab_chunks(
    labs,
    patient_id,
    document_id
):
    chunks = []

    for lab in labs:

        text = (
            f"Lab Test: {lab['test']}. "
            f"Value: {lab['value']} {lab.get('unit','')}. "
            f"Status: {lab['status']}. "
            f"Collected on {lab.get('date','unknown')}."
        )

        low, high = lab.get(
            "reference_range",
            (None, None)
        )

        if low or high:
            text += (
                f" Reference range "
                f"{low}-{high}."
            )

        chunks.append(
            create_chunk(
                text=text,
                patient_id=patient_id,
                document_id=document_id,

                report_type="LAB_REPORT",

                chunk_type="lab_row",
                chunk_level=1,

                report_date=lab.get("date"),

                metadata={
                     "test_name": lab["test"],
                    "value": lab["value"],
                    "unit": lab.get("unit"),
                    "status": lab["status"]
                }
            )
        )

    return chunks