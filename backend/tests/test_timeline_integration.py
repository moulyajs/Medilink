import os
import uuid
from datetime import datetime, timezone
from unittest.mock import patch

import pytest
from sqlalchemy import text
from fastapi.testclient import TestClient

if os.getenv("DB_SCHEMA") != "integration_test":
    raise RuntimeError("Tests require DB_SCHEMA=integration_test")

from database import SessionLocal
from scripts.timeline_saver import add_timeline_event
from scripts.timeline_service import get_timeline


def get_patient_ids():
    db = SessionLocal()
    try:
        rows = db.execute(
            text("SELECT patient_id FROM patients LIMIT 2")
        ).fetchall()
        return [str(row[0]) for row in rows]
    finally:
        db.close()


def insert_document(patient_id):
    """Create a document row for a timeline event."""
    document_id = None
    db = SessionLocal()
    try:
        row = db.execute(
            text("""
                INSERT INTO documents
                    (patient_id, document_type, upload_date, file_path)
                VALUES
                    (:pid, 'LAB_REPORT', NOW(), :path)
                RETURNING document_id
            """),
            {
                "pid": patient_id,
                "path": f"pytest-timeline-{uuid.uuid4().hex}.pdf",
            },
        ).fetchone()
        document_id = str(row[0])
        db.commit()
        return document_id
    finally:
        db.close()


def delete_test_data(document_id):
    """Delete test-created timeline events and their document."""
    if not document_id:
        return

    db = SessionLocal()
    try:
        db.execute(
            text("""
                DELETE FROM timeline_events
                WHERE source_document = :did
            """),
            {"did": document_id},
        )
        db.execute(
            text("""
                DELETE FROM lab_results
                WHERE document_id = :did
            """),
            {"did": document_id},
        )
        db.execute(
            text("""
                DELETE FROM documents
                WHERE document_id = :did
            """),
            {"did": document_id},
        )
        db.commit()
    finally:
        db.close()


# INT-TL-01: PostgreSQL -> Timeline service
def test_int_tl_01_postgres_to_timeline():
    patients = get_patient_ids()
    if not patients:
        pytest.skip("Seed a patient in integration_test first")

    patient_id = patients[0]
    document_id = insert_document(patient_id)

    try:
        add_timeline_event(
            patient_id=patient_id,
            document_id=document_id,
            event_type="LAB_REPORT",
            summary="Integration test timeline event",
            event_date="2026-01-10",
        )

        results = get_timeline(patient_id)

        assert any(
            item["source_document"] == document_id
            and item["summary"] == "Integration test timeline event"
            for item in results
        )
    finally:
        delete_test_data(document_id)


# INT-TL-02: Structured record -> Timeline
def test_int_tl_02_saved_record_appears_in_timeline():
    patients = get_patient_ids()
    if not patients:
        pytest.skip("Seed a patient in integration_test first")

    patient_id = patients[0]
    document_id = insert_document(patient_id)

    try:
        add_timeline_event(
            patient_id=patient_id,
            document_id=document_id,
            event_type="LAB_REPORT",
            summary="Haemoglobin test",
            event_date="2026-02-15",
        )

        results = get_timeline(patient_id)
        event = next(
            (
                item for item in results
                if item["source_document"] == document_id
            ),
            None,
        )

        assert event is not None
        assert event["type"] == "LAB_REPORT"
        assert event["summary"] == "Haemoglobin test"
    finally:
        delete_test_data(document_id)


# INT-TL-03: Timeline events are sorted newest first
def test_int_tl_03_timeline_date_sorting():
    patients = get_patient_ids()
    if not patients:
        pytest.skip("Seed a patient in integration_test first")

    patient_id = patients[0]
    document_ids = []

    try:
        for date, summary in [
            ("2026-01-05", "Older test event"),
            ("2026-03-05", "Newer test event"),
        ]:
            document_id = insert_document(patient_id)
            document_ids.append(document_id)

            add_timeline_event(
                patient_id=patient_id,
                document_id=document_id,
                event_type="LAB_REPORT",
                summary=summary,
                event_date=date,
            )

        results = get_timeline(patient_id)
        test_events = [
            item for item in results
            if item["source_document"] in document_ids
        ]

        assert len(test_events) == 2
        assert test_events[0]["summary"] == "Newer test event"
        assert test_events[1]["summary"] == "Older test event"
    finally:
        for document_id in document_ids:
            delete_test_data(document_id)


# INT-TL-05: Timeline entry links to the corresponding report
def test_int_tl_05_timeline_report_linkage():
    patients = get_patient_ids()
    if not patients:
        pytest.skip("Seed a patient in integration_test first")

    patient_id = patients[0]
    document_id = insert_document(patient_id)

    try:
        add_timeline_event(
            patient_id=patient_id,
            document_id=document_id,
            event_type="LAB_REPORT",
            summary="Report linkage test",
            event_date="2026-04-01",
        )

        results = get_timeline(patient_id)
        event = next(
            (
                item for item in results
                if item["source_document"] == document_id
            ),
            None,
        )

        assert event is not None
        assert event["document_id"] == document_id
    finally:
        delete_test_data(document_id)


# INT-TL-08: Patient filter prevents cross-patient timeline records
def test_int_tl_08_patient_isolation():
    patients = get_patient_ids()
    if len(patients) < 2:
        pytest.skip(
            "At least two patients are required in integration_test"
        )

    patient_a, patient_b = patients
    document_a = insert_document(patient_a)
    document_b = insert_document(patient_b)

    try:
        add_timeline_event(
            patient_id=patient_a,
            document_id=document_a,
            event_type="LAB_REPORT",
            summary="Patient A private test event",
            event_date="2026-05-01",
        )
        add_timeline_event(
            patient_id=patient_b,
            document_id=document_b,
            event_type="LAB_REPORT",
            summary="Patient B private test event",
            event_date="2026-05-02",
        )

        timeline_a = get_timeline(patient_a)
        timeline_b = get_timeline(patient_b)

        assert any(
            item["source_document"] == document_a
            for item in timeline_a
        )
        assert not any(
            item["source_document"] == document_b
            for item in timeline_a
        )

        assert any(
            item["source_document"] == document_b
            for item in timeline_b
        )
        assert not any(
            item["source_document"] == document_a
            for item in timeline_b
        )
    finally:
        delete_test_data(document_a)
        delete_test_data(document_b)