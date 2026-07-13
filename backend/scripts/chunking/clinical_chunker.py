from .chunk_schema import create_chunk


def build_clinical_chunks(
    extracted_data,
    patient_id,
    document_id,
    report_date=None
):
    chunks = []

    for doc in extracted_data:

        report_date = doc["report_date"]
        facts = doc["facts"]

        # =====================================
        # DIAGNOSES CHUNK
        # =====================================

        diagnoses = facts.get("diagnoses", [])

        if diagnoses:

            text = (
                f"Date: {report_date}\n\n"
                f"Diagnoses:\n- "
                + "\n- ".join(diagnoses)
            )

            chunks.append(
                create_chunk(
                    text=text,
                    patient_id=patient_id,
                    document_id=document_id,
                    report_type="CLINICAL_NOTE",
                    chunk_type="diagnosis",
                    chunk_level=1,
                    report_date=report_date,
                    metadata={
                        "category": "diagnosis",
                        "count": len(diagnoses)
                    }
                )
            )

        # =====================================
        # MEDICATIONS CHUNK
        # =====================================

        medications = facts.get("medications", [])

        if medications:

            text = (
                f"Date: {report_date}\n\n"
                f"Medications:\n- "
                + "\n- ".join(medications)
            )

            chunks.append(
                create_chunk(
                    text=text,
                    patient_id=patient_id,
                    document_id=document_id,
                    report_type="CLINICAL_NOTE",
                    chunk_type="medication",
                    chunk_level=1,
                    report_date=report_date,
                    metadata={
                        "category": "medication",
                        "count": len(medications)
                    }
                )
            )

        # =====================================
        # SYMPTOMS CHUNK
        # =====================================

        symptoms = facts.get("symptoms", [])

        if symptoms:

            text = (
                f"Date: {report_date}\n\n"
                f"Symptoms:\n- "
                + "\n- ".join(symptoms)
            )

            chunks.append(
                create_chunk(
                    text=text,
                    patient_id=patient_id,
                    document_id=document_id,
                    report_type="CLINICAL_NOTE",
                    chunk_type="symptom",
                    chunk_level=1,
                    report_date=report_date,
                    metadata={
                        "category": "symptom",
                        "count": len(symptoms)
                    }
                )
            )

        # =====================================
        # FINDINGS CHUNK
        # =====================================

        findings = facts.get("findings", [])

        if findings:

            text = (
                f"Date: {report_date}\n\n"
                f"Findings:\n- "
                + "\n- ".join(findings)
            )

            chunks.append(
                create_chunk(
                    text=text,
                    patient_id=patient_id,
                    document_id=document_id,
                    report_type="CLINICAL_NOTE",
                    chunk_type="finding",
                    chunk_level=1,
                    report_date=report_date,
                    metadata={
                        "category": "finding",
                        "count": len(findings)
                    }
                )
            )

        # =====================================
        # PROCEDURES CHUNK
        # =====================================

        procedures = facts.get("procedures", [])

        if procedures:

            text = (
                f"Date: {report_date}\n\n"
                f"Procedures:\n- "
                + "\n- ".join(procedures)
            )

            chunks.append(
                create_chunk(
                    text=text,
                    patient_id=patient_id,
                    document_id=document_id,
                    report_type="CLINICAL_NOTE",
                    chunk_type="procedure",
                    chunk_level=1,
                    report_date=report_date,
                    metadata={
                        "category": "procedure",
                        "count": len(procedures)
                    }
                )
            )

    return chunks