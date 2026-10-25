
import os
import uuid
from datetime import date

import pytest
from sqlalchemy import text

if os.getenv("DB_SCHEMA") != "integration_test":
    raise RuntimeError(
        "Refusing to run baseline tests: "
        "DB_SCHEMA must be integration_test."
    )

from database import SessionLocal
from scripts.baseline_engine import (
    get_history,
    calculate_baseline,
    save_baseline,
    update_patient_baselines,
)
from scripts.anomaly_detection import detect_patient_anomalies


def new_id():
    return str(uuid.uuid4())


@pytest.fixture
def test_patient():
    """Create an isolated synthetic patient and clean up afterward."""
    patient_id = new_id()
    db = SessionLocal()

    try:
        db.execute(
            text("""
                INSERT INTO patients (
                    patient_id, email, password_hash,
                    is_email_verified
                )
                VALUES (
                    :pid, :email, :password_hash, TRUE
                )
            """),
            {
                "pid": patient_id,
                "email": f"baseline-test-{patient_id}@example.test",
                "password_hash": "synthetic-test-hash",
            },
        )
        db.commit()
    except Exception:
        db.rollback()
        db.close()
        raise
    finally:
        # Close the setup session before yielding the fixture.
        if db.is_active:
            db.close()

    yield patient_id

    # Remove only data associated with this synthetic patient.
    db = SessionLocal()
    try:
        for table in (
            "patient_anomalies",
            "personal_baseline",
            "lab_results",
            "timeline_events",
            "documents",
            "profiles",
        ):
            db.execute(
                text(
                    f"DELETE FROM {table} "
                    "WHERE patient_id = :pid"
                ),
                {"pid": patient_id},
            )

        db.execute(
            text("DELETE FROM patients WHERE patient_id = :pid"),
            {"pid": patient_id},
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def insert_document(db, patient_id):
    """Create a synthetic document for lab-result references."""
    document_id = new_id()

    db.execute(
        text("""
            INSERT INTO documents (
                document_id, patient_id, document_type,
                report_date, file_path
            )
            VALUES (
                :docid, :pid, 'LAB_REPORT', :report_date,
                'integration-test/fake-report.pdf'
            )
        """),
        {
            "docid": document_id,
            "pid": patient_id,
            "report_date": date(2026, 1, 10),
        },
    )

    return document_id


def insert_lab(
    db,
    patient_id,
    document_id,
    test_name,
    value,
    result_date,
):
    db.execute(
        text("""
            INSERT INTO lab_results (
                result_id, patient_id, document_id,
                test_name, test_category, value, unit,
                result_date
            )
            VALUES (
                :rid, :pid, :docid, :test_name,
                'LAB', :value, 'g/dL', :result_date
            )
        """),
        {
            "rid": new_id(),
            "pid": patient_id,
            "docid": document_id,
            "test_name": test_name,
            "value": value,
            "result_date": result_date,
        },
    )


# INT-BASE-01
def test_int_base_01_postgres_to_baseline_engine(test_patient):
    """History retrieval returns only this patient's stored values."""
    patient_id = test_patient
    db = SessionLocal()

    try:
        document_id = insert_document(db, patient_id)

        insert_lab(
            db, patient_id, document_id,
            "TEST_HAEMOGLOBIN", 12.0, date(2026, 1, 1)
        )
        insert_lab(
            db, patient_id, document_id,
            "TEST_HAEMOGLOBIN", 13.5, date(2026, 2, 1)
        )
        insert_lab(
            db, patient_id, document_id,
            "TEST_HAEMOGLOBIN", None, date(2026, 3, 1)
        )
        db.commit()
    finally:
        db.close()

    values = get_history(patient_id, "TEST_HAEMOGLOBIN")

    assert values == [12.0, 13.5]


# INT-BASE-02
def test_int_base_02_extracted_lab_to_baseline_workflow(
    test_patient, monkeypatch
):
    """Saving an extracted lab persists it and updates the baseline."""
    import scripts.record_saver as record_saver

    patient_id = test_patient
    db = SessionLocal()

    try:
        document_id = insert_document(db, patient_id)
        db.commit()
    finally:
        db.close()

    # Trend processing is outside this test's scope.
    monkeypatch.setattr(
        record_saver, "update_patient_trends",
        lambda patient_id: None,
    )

    labs = [{
        "test_name": "test_haemoglobin",
        "value": 14.2,
        "unit": "g/dL",
        "date": date(2026, 4, 10),
        "reference_range": [12.0, 16.0],
        "abnormal": False,
    }]

    returned_id = record_saver.save_medical_record(
        patient_id=patient_id,
        file_id=document_id,
        document_type="LAB_REPORT",
        labs=labs,
        clinical_facts=[],
    )

    assert returned_id == document_id

    db = SessionLocal()
    try:
        saved_value = db.execute(
            text("""
                SELECT value
                FROM lab_results
                WHERE patient_id = :pid
                  AND document_id = :docid
                  AND test_name = 'TEST_HAEMOGLOBIN'
            """),
            {"pid": patient_id, "docid": document_id},
        ).scalar_one()

        baseline = db.execute(
            text("""
                SELECT personal_average, sample_count
                FROM personal_baseline
                WHERE patient_id = :pid
                  AND test_name = 'TEST_HAEMOGLOBIN'
            """),
            {"pid": patient_id},
        ).one()

        assert saved_value == pytest.approx(14.2)
        assert baseline.personal_average == pytest.approx(14.2)
        assert baseline.sample_count == 1
    finally:
        db.close()


# INT-BASE-03
def test_int_base_03_patient_records_to_baseline_calculation(
    test_patient,
):
    """Multiple stored results produce the expected baseline statistics."""
    patient_id = test_patient
    db = SessionLocal()

    try:
        document_id = insert_document(db, patient_id)

        for value, result_date in [
            (10.0, date(2026, 1, 1)),
            (12.0, date(2026, 2, 1)),
            (14.0, date(2026, 3, 1)),
        ]:
            insert_lab(
                db, patient_id, document_id,
                "TEST_BASELINE", value, result_date
            )

        db.commit()
    finally:
        db.close()

    update_patient_baselines(patient_id)

    db = SessionLocal()
    try:
        baseline = db.execute(
            text("""
                SELECT personal_average, personal_min,
                       personal_max, personal_variability,
                       sample_count
                FROM personal_baseline
                WHERE patient_id = :pid
                  AND test_name = 'TEST_BASELINE'
            """),
            {"pid": patient_id},
        ).one()

        expected = calculate_baseline([10.0, 12.0, 14.0])

        assert baseline.personal_average == expected["average"]
        assert baseline.personal_min == expected["minimum"]
        assert baseline.personal_max == expected["maximum"]
        assert (
            baseline.personal_variability
            == expected["variability"]
        )
        assert baseline.sample_count == 3
    finally:
        db.close()


# INT-BASE-04
def test_int_base_04_baseline_to_anomaly_classification(test_patient):
    """A 30% increase against a baseline is classified as UP."""
    patient_id = test_patient

    save_baseline(
        patient_id,
        "TEST_ANOMALY",
        {
            "average": 10.0,
            "minimum": 9.0,
            "maximum": 11.0,
            "variability": 1.0,
            "sample_count": 3,
        },
    )

    anomalies = detect_patient_anomalies(
        patient_id,
        [{
            "test": "TEST_ANOMALY",
            "value": 13.0,
            "date": date(2026, 4, 1),
        }],
    )

    assert len(anomalies) == 1
    assert anomalies[0]["test_name"] == "TEST_ANOMALY"
    assert anomalies[0]["baseline"] == pytest.approx(10.0)
    assert anomalies[0]["percent_change"] == pytest.approx(30.0)
    assert anomalies[0]["trend"] == "UP"


# INT-BASE-07
def test_int_base_07_patient_identity_selects_own_baseline(
    test_patient,
):
    """A patient's history must not include another patient's values."""
    patient_a = test_patient
    patient_b = new_id()
    db = SessionLocal()

    try:
        db.execute(
            text("""
                INSERT INTO patients (
                    patient_id, email, password_hash,
                    is_email_verified
                )
                VALUES (
                    :pid, :email, 'synthetic-test-hash', TRUE
                )
            """),
            {
                "pid": patient_b,
                "email": f"baseline-test-{patient_b}@example.test",
            },
        )

        doc_a = insert_document(db, patient_a)
        doc_b = insert_document(db, patient_b)

        insert_lab(
            db, patient_a, doc_a,
            "TEST_ISOLATION", 10.0, date(2026, 1, 1)
        )
        insert_lab(
            db, patient_b, doc_b,
            "TEST_ISOLATION", 99.0, date(2026, 1, 1)
        )

        db.commit()
    finally:
        db.close()

    try:
        assert get_history(patient_a, "TEST_ISOLATION") == [10.0]
        assert get_history(patient_b, "TEST_ISOLATION") == [99.0]
    finally:
        db = SessionLocal()
        try:
            for table in (
                "patient_anomalies",
                "personal_baseline",
                "lab_results",
                "timeline_events",
                "documents",
                "profiles",
            ):
                db.execute(
                    text(
                        f"DELETE FROM {table} "
                        "WHERE patient_id = :pid"
                    ),
                    {"pid": patient_b},
                )

            db.execute(
                text("DELETE FROM patients WHERE patient_id = :pid"),
                {"pid": patient_b},
            )
            db.commit()
        finally:
            db.close()


# INT-BASE-09
def test_int_base_09_baseline_result_persisted_to_postgres(
    test_patient,
):
    """Saving a baseline persists it and updates it on conflict."""
    patient_id = test_patient

    save_baseline(
        patient_id,
        "TEST_PERSISTENCE",
        {
            "average": 10.0,
            "minimum": 8.0,
            "maximum": 12.0,
            "variability": 2.0,
            "sample_count": 2,
        },
    )

    # Exercise the ON CONFLICT update path as well.
    save_baseline(
        patient_id,
        "TEST_PERSISTENCE",
        {
            "average": 11.0,
            "minimum": 9.0,
            "maximum": 13.0,
            "variability": 2.0,
            "sample_count": 3,
        },
    )

    db = SessionLocal()
    try:
        rows = db.execute(
            text("""
                SELECT personal_average, personal_min,
                       personal_max, sample_count
                FROM personal_baseline
                WHERE patient_id = :pid
                  AND test_name = 'TEST_PERSISTENCE'
            """),
            {"pid": patient_id},
        ).fetchall()

        assert len(rows) == 1
        assert rows[0].personal_average == pytest.approx(11.0)
        assert rows[0].personal_min == pytest.approx(9.0)
        assert rows[0].personal_max == pytest.approx(13.0)
        assert rows[0].sample_count == 3
    finally:
        db.close()
