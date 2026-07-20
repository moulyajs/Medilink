from uuid import uuid4


def create_chunk(
    text: str,
    patient_id: str,
    document_id: str,
    report_type: str,
    chunk_type: str,
    chunk_level: int,
    report_date=None,
    metadata=None,
):
    return {
        "chunk_id": str(uuid4()),
        "text": text,

        "patient_id": patient_id,
        "document_id": document_id,

        "report_type": report_type,

        "chunk_type": chunk_type,
        "chunk_level": chunk_level,

        "report_date": str(report_date) if report_date else None,

        "metadata": metadata or {}
    }