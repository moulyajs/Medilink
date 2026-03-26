def create_chunks(parsed_data, patient_id, document_id, report_date):
    chunks = []

    for lab in parsed_data.get("lab_results", []):
        low, high = lab.get("reference_range", (None, None))

        text = (
            f"{lab['test_name']} value is {lab['value']} {lab.get('unit', '')} "
            f"with reference range {low}-{high}"
        )

        chunks.append({
            "text": text,
            "patient_id": patient_id,
            "document_id": document_id,
            "report_date": report_date,
            "chunk_type": "lab_result"
        })

    return chunks