"""
from .chunk_schema import create_chunk


def build_prescription_chunks(
    medications,
    patient_id,
    document_id
):
    chunks = []

    for med in medications:

        text = (
            f"Medication: {med.get('drug','')}. "
            f"Dose: {med.get('dose','Unknown')}. "
            f"Frequency: {med.get('frequency','Unknown')}."
        )

        chunks.append(
            create_chunk(
                text=text,

                patient_id=patient_id,
                document_id=document_id,

                report_type="PRESCRIPTION",

                chunk_type="medication",
                chunk_level=1,

                metadata=med
            )
        )

    return chunks
"""
##not being used