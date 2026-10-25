import os
import sys
import uuid
from types import ModuleType
from unittest.mock import patch

import pytest

if os.getenv("DB_SCHEMA") != "integration_test":
    raise RuntimeError(
        "Tests require DB_SCHEMA=integration_test"
    )

from scripts import app as pipeline


# INT-OCR-01: PDF parser output flows through process_document.
def test_int_ocr_01_pdf_processing(tmp_path):
    pdf = tmp_path / "report.pdf"
    pdf.write_bytes(b"mock PDF fixture")

    parser_result = {
        "lines": [{"text": "Haemoglobin 13.5 g/dL"}],
        "tables": [],
        "full_text": "Haemoglobin 13.5 g/dL",
        "doc_type": "LAB_REPORT",
    }

    labs = [
        {
            "test_name": "Haemoglobin",
            "value": 13.5,
            "unit": "g/dL",
        }
    ]

    with (
        patch.object(
            pipeline,
            "parse_pdf_with_docling",
            return_value=parser_result,
        ),
        patch.object(
            pipeline, "extract_demographics", return_value={}
        ),
        patch.object(pipeline, "verify_patient"),
        patch.object(pipeline, "extract_date", return_value=None),
        patch.object(pipeline, "normalize_date", return_value=None),
        patch.object(
            pipeline, "extract_lab_results", return_value=labs
        ),
        patch.object(
            pipeline,
            "normalize_lab_results",
            return_value=[dict(labs[0])],
        ),
        patch.object(
            pipeline, "is_duplicate_report", return_value=False
        ),
    ):
        result = pipeline.process_document(
            str(pdf), str(uuid.uuid4())
        )

    assert result["lab_values"][0]["test_name"] == "Haemoglobin"
    assert result["lab_values"][0]["value"] == 13.5
    assert result["is_duplicate"] is False


# INT-OCR-03: OCR output flows through process_document.
def test_int_ocr_03_image_processing(tmp_path):
    image = tmp_path / "report.png"
    image.write_bytes(b"mock image fixture")

    labs = [
        {
            "test_name": "Haemoglobin",
            "value": 13.5,
            "unit": "g/dL",
        }
    ]

    ocr_pages = [
        {
            "lines": [{"text": "Haemoglobin 13.5 g/dL"}],
            "doc_type": "LAB_REPORT",
        }
    ]

    # process_document imports ocr_pipeline inside the function.
    # Register a fake module so the test doesn't require the real OCR
    # package or model to load.
    fake_ocr_module = ModuleType("ocr_pipeline")
    fake_ocr_module.ocr_process = lambda file_path: ocr_pages

    with (
        patch.dict(
            sys.modules,
            {"ocr_pipeline": fake_ocr_module},
        ),
        patch.object(
            pipeline,
            "group_by_date",
            return_value={"2026-01-01": ocr_pages},
        ),
        patch.object(
            pipeline, "extract_demographics", return_value={}
        ),
        patch.object(pipeline, "verify_patient"),
        patch.object(
            pipeline, "extract_lab_results", return_value=labs
        ),
        patch.object(
            pipeline,
            "normalize_lab_results",
            return_value=[dict(labs[0])],
        ),
        patch.object(
            pipeline, "is_duplicate_report", return_value=False
        ),
    ):
        result = pipeline.process_document(
            str(image), str(uuid.uuid4())
        )

    assert result["lab_values"][0]["test_name"] == "Haemoglobin"
    assert result["lab_values"][0]["value"] == 13.5
    assert result["is_duplicate"] is False


# INT-OCR-06: Verify structured lab output.
def test_int_ocr_06_structured_lab_values(tmp_path):
    pdf = tmp_path / "labs.pdf"
    pdf.write_bytes(b"mock PDF fixture")

    raw_labs = [
        {
            "test_name": "Haemoglobin",
            "value": 13.5,
            "unit": "g/dL",
        },
        {
            "test_name": "WBC",
            "value": 7500,
            "unit": "cells/uL",
        },
    ]

    with (
        patch.object(
            pipeline,
            "parse_pdf_with_docling",
            return_value={
                "lines": [],
                "tables": [],
                "full_text": "Lab report",
                "doc_type": "LAB_REPORT",
            },
        ),
        patch.object(
            pipeline, "extract_demographics", return_value={}
        ),
        patch.object(pipeline, "verify_patient"),
        patch.object(pipeline, "extract_date", return_value=None),
        patch.object(pipeline, "normalize_date", return_value=None),
        patch.object(
            pipeline, "extract_lab_results", return_value=raw_labs
        ),
        patch.object(
            pipeline,
            "normalize_lab_results",
            side_effect=lambda values: values,
        ),
        patch.object(
            pipeline, "is_duplicate_report", return_value=False
        ),
    ):
        result = pipeline.process_document(
            str(pdf), str(uuid.uuid4())
        )

    assert len(result["lab_values"]) == 2

    by_name = {
        lab["test_name"]: lab
        for lab in result["lab_values"]
    }

    assert by_name["Haemoglobin"]["value"] == 13.5
    assert by_name["Haemoglobin"]["unit"] == "g/dL"
    assert by_name["WBC"]["value"] == 7500
    assert by_name["WBC"]["unit"] == "cells/uL"


# INT-OCR-09: Save and read a real lab row in integration_test.
def test_int_ocr_09_postgres_persistence():
    from sqlalchemy import text
    from database import SessionLocal
    from scripts import record_saver

    # Find an existing patient in the isolated integration schema.
    db = SessionLocal()
    try:
        patient = db.execute(
            text("SELECT patient_id FROM patients LIMIT 1")
        ).fetchone()
    finally:
        db.close()

    if patient is None:
        pytest.skip(
            "Seed a test patient in integration_test before this test"
        )

    patient_id = str(patient[0])
    document_id = None
    test_name = f"TEST_HB_{uuid.uuid4().hex[:8]}".upper()
    file_path = f"pytest-{uuid.uuid4().hex}.pdf"

    try:
        # Create the parent document first to satisfy the foreign key
        # from lab_results.document_id to documents.document_id.
        db = SessionLocal()
        try:
            inserted_document = db.execute(
                text("""
                    INSERT INTO documents (
                        patient_id,
                        document_type,
                        upload_date,
                        file_path
                    )
                    VALUES (
                        :patient_id,
                        'LAB_REPORT',
                        NOW(),
                        :file_path
                    )
                    RETURNING document_id
                """),
                {
                    "patient_id": patient_id,
                    "file_path": file_path,
                },
            ).fetchone()

            document_id = str(inserted_document[0])
            db.commit()
        finally:
            db.close()

        # Keep analytics side effects outside the scope of this test.
        with (
            patch.object(
                record_saver, "detect_patient_anomalies"
            ),
            patch.object(
                record_saver, "update_patient_baselines"
            ),
            patch.object(
                record_saver, "update_patient_trends"
            ),
            patch.object(
                record_saver, "save_patient_anomalies"
            ),
        ):
            record_saver.save_medical_record(
                patient_id=patient_id,
                file_id=document_id,
                document_type="LAB_REPORT",
                labs=[
                    {
                        "test_name": test_name,
                        "value": 13.5,
                        "unit": "g/dL",
                        "reference_range": [12.0, 16.0],
                        "abnormal": False,
                        "date": None,
                    }
                ],
                clinical_facts={},
            )

        # Verify the lab row was persisted in PostgreSQL.
        db = SessionLocal()
        try:
            row = db.execute(
                text("""
                    SELECT
                        patient_id,
                        document_id,
                        test_name,
                        value,
                        unit
                    FROM lab_results
                    WHERE patient_id = :patient_id
                      AND document_id = :document_id
                      AND test_name = :test_name
                """),
                {
                    "patient_id": patient_id,
                    "document_id": document_id,
                    "test_name": test_name,
                },
            ).fetchone()

            assert row is not None
            assert str(row[0]) == patient_id
            assert str(row[1]) == document_id
            assert row[2] == test_name
            assert float(row[3]) == 13.5
            assert row[4] == "g/dL"
        finally:
            db.close()

    finally:
        # Remove child rows before deleting their parent document.
        db = SessionLocal()
        try:
            if document_id is not None:
                db.execute(
                    text("""
                        DELETE FROM lab_results
                        WHERE document_id = :document_id
                    """),
                    {"document_id": document_id},
                )

                db.execute(
                    text("""
                        DELETE FROM documents
                        WHERE document_id = :document_id
                    """),
                    {"document_id": document_id},
                )

            db.commit()
        finally:
            db.close()


# INT-OCR-10: A corrupted PDF must not return fabricated lab values.
def test_int_ocr_10_invalid_pdf_fails_safely(tmp_path):
    pdf = tmp_path / "corrupted.pdf"
    pdf.write_bytes(b"this is not a valid PDF")

    with patch.object(
        pipeline,
        "parse_pdf_with_docling",
        side_effect=ValueError("Invalid PDF"),
    ):
        with pytest.raises(ValueError, match="Invalid PDF"):
            pipeline.process_document(
                str(pdf), str(uuid.uuid4())
            )