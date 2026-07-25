from .chunk_schema import create_chunk


def build_lab_summary_chunk(
    labs,
    patient_id,
    document_id
):

    abnormal = []
    normal = []

    report_date = None

    for lab in labs:

        report_date = lab.get("date")

        status = lab.get("abnormal") or "NORMAL"

        line = (
            f"{lab['test_name']} "
            f"({lab['value']} {lab.get('unit', '')})"
        )

        if status in ["LOW", "HIGH", "ABNORMAL"]:
            abnormal.append(line)
        else:
            normal.append(line)

    text = "Laboratory Report Summary\n\n"

    if abnormal:
        text += "Abnormal Findings:\n"
        text += "\n".join(
            f"- {x}" for x in abnormal
        )
        text += "\n\n"

    if normal:
        text += "Normal Findings:\n"
        text += "\n".join(
            f"- {x}" for x in normal
        )

    return [
        create_chunk(
            text=text,

            patient_id=patient_id,
            document_id=document_id,

            report_type="LAB_REPORT",

            chunk_type="lab_summary",

            chunk_level=2,

            report_date=report_date,

            metadata={
                "abnormal_count": len(abnormal),
                "normal_count": len(normal)
            }
        )
    ]
