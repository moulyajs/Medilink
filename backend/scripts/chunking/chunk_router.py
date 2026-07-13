from .lab_chunker import build_lab_chunks
from .lab_summary_chunker import (
    build_lab_summary_chunk
)
from .clinical_chunker import (
    build_clinical_chunks
)


def build_chunks(
    doc_type,
    extracted_data,
    patient_id,
    document_id
):

    if doc_type == "LAB_REPORT":

        row_chunks = build_lab_chunks(
            extracted_data,
            patient_id,
            document_id
        )

        summary_chunks = build_lab_summary_chunk(
            extracted_data,
            patient_id,
            document_id
        )

        return row_chunks + summary_chunks

    elif doc_type == "CLINICAL_NOTE":

        return build_clinical_chunks(
            extracted_data,
            patient_id,
            document_id
        )

    return []