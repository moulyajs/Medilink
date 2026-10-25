
import os
import uuid
from datetime import date

import pytest
from sqlalchemy import text

if os.getenv("DB_SCHEMA") != "integration_test":
    raise RuntimeError(
        "Refusing to run trend tests: DB_SCHEMA must be integration_test"
    )

from database import SessionLocal
from scripts.trend_engine import (
    calculate_delta,
    calculate_slope,
    determine_trend,
    update_patient_trends,
)


def new_id():
    return str(uuid.uuid4())


@pytest.fixture
def trend_patient():
    """Create a synthetic patient and clean up its test records."""
    patient_id = new_id()
    db = SessionLocal()

    try:
        db.execute(
            text("""
                INSERT INTO patients (
                    patient_id, email, password_hash, is_email_verified
                )
                VALUES (
                    :pid, :email, 'synthetic-test-hash', TRUE
                )
            """),
            {
                "pid": patient_id,
                "email": f"trend-test-{patient_id}@example.test",
            },
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    yield patient_id

    db = SessionLocal()
    try:
        # Delete only rows belonging to this synthetic patient.
        for table in (
            "lab_trends",
            "patient_anomalies",
            "personal_baseline",
            "timeline_events",
            "lab_results",
            "documents",
            "profiles",
        ):
            db.execute(
                text(f"DELETE FROM {table} WHERE patient_id = :pid"),
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


def add_document(db, patient_id):
    document_id = new_id()
    db.execute(
        text("""
            INSERT INTO documents (
                document_id, patient_id, document_type, report_date
            )
            VALUES (:docid, :pid, 'LAB_REPORT', :report_date)
        """),
        {
            "docid": document_id,
            "pid": patient_id,
            "report_date": date(2026, 1, 1),
        },
    )
    return document_id


def add_lab(
    db,
    patient_id,
    document_id,
    test_name,
    value,
    result_date,
    abnormal=True,
    reference_low=10.0,
    reference_high=20.0,
):
    db.execute(
        text("""
            INSERT INTO lab_results (
                result_id, patient_id, document_id, test_name,
                test_category, value, unit, reference_low,
                reference_high, abnormal_flag, result_date
            )
            VALUES (
                :rid, :pid, :docid, :test, 'LAB', :value,
                'unit', :low, :high, :abnormal, :result_date
            )
        """),
        {
            "rid": new_id(),
            "pid": patient_id,
            "docid": document_id,
            "test": test_name,
            "value": value,
            "low": reference_low,
            "high": reference_high,
            "abnormal": abnormal,
            "result_date": result_date,
        },
    )


# INT-TR-01: PostgreSQL -> trend engine
def test_int_tr_01_postgres_to_trend_engine(trend_patient):
    patient_id = trend_patient
    db = SessionLocal()

    try:
        document_id = add_document(db, patient_id)
        add_lab(
            db, patient_id, document_id, "TEST_TREND",
            12.0, date(2026, 1, 1)
        )
        add_lab(
            db, patient_id, document_id, "TEST_TREND",
            15.0, date(2026, 2, 1)
        )
        db.commit()
    finally:
        db.close()

    # Exercise the trend engine's real database retrieval path.
    update_patient_trends(patient_id)

    db = SessionLocal()
    try:
        row = db.execute(
            text("""
                SELECT latest_value, delta, data_points
                FROM lab_trends
                WHERE patient_id = :pid AND test_name = 'TEST_TREND'
            """),
            {"pid": patient_id},
        ).one()

        assert row.latest_value == pytest.approx(15.0)
        assert row.delta == pytest.approx(3.0)
        assert row.data_points == 2
    finally:
        db.close()


# INT-TR-02: Structured extraction -> trend engine
def test_int_tr_02_new_lab_result_reaches_trend_engine(trend_patient):
    patient_id = trend_patient
    db = SessionLocal()

    try:
        document_id = add_document(db, patient_id)
        add_lab(
            db, patient_id, document_id, "TEST_NEW_RESULT",
            12.0, date(2026, 1, 1)
        )
        add_lab(
            db, patient_id, document_id, "TEST_NEW_RESULT",
            14.0, date(2026, 2, 1)
        )
        # The latest extracted result is saved to PostgreSQL.
        add_lab(
            db, patient_id, document_id, "TEST_NEW_RESULT",
            17.0, date(2026, 3, 1)
        )
        db.commit()
    finally:
        db.close()

    update_patient_trends(patient_id)

    db = SessionLocal()
    try:
        row = db.execute(
            text("""
                SELECT latest_value, delta, data_points
                FROM lab_trends
                WHERE patient_id = :pid
                  AND test_name = 'TEST_NEW_RESULT'
            """),
            {"pid": patient_id},
        ).one()

        assert row.latest_value == pytest.approx(17.0)
        assert row.delta == pytest.approx(3.0)
        assert row.data_points == 3
    finally:
        db.close()


# INT-TR-03: Trend engine -> delta calculation
def test_int_tr_03_delta_calculation():
    assert calculate_delta([10.0, 12.5]) == pytest.approx(2.5)
    assert calculate_delta([10.0, 12.0, 9.0]) == pytest.approx(-3.0)
    assert calculate_delta([10.0]) is None


# INT-TR-06: Trend engine -> direction classification
@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([1.0, 2.0, 3.0], "Increasing"),
        ([3.0, 2.0, 1.0], "Decreasing"),
        ([2.0, 2.0, 2.0], "Stable"),
    ],
)
def test_int_tr_06_direction_classification(values, expected):
    slope = calculate_slope(values)
    assert determine_trend(slope) == expected


# INT-TR-07: Trend engine -> insufficient history
def test_int_tr_07_insufficient_history(trend_patient):
    patient_id = trend_patient
    db = SessionLocal()

    try:
        document_id = add_document(db, patient_id)
        add_lab(
            db, patient_id, document_id, "TEST_SINGLE_POINT",
            15.0, date(2026, 1, 1)
        )
        db.commit()
    finally:
        db.close()

    update_patient_trends(patient_id)

    db = SessionLocal()
    try:
        row = db.execute(
            text("""
                SELECT delta, slope, trend, data_points
                FROM lab_trends
                WHERE patient_id = :pid
                  AND test_name = 'TEST_SINGLE_POINT'
            """),
            {"pid": patient_id},
        ).one()

        assert row.delta is None
        assert row.slope is None
        assert row.trend == "Insufficient Data"
        assert row.data_points == 1
    finally:
        db.close()


# INT-TR-12: Trend engine -> database update
def test_int_tr_12_new_observation_updates_saved_trend(trend_patient):
    patient_id = trend_patient
    db = SessionLocal()

    try:
        document_id = add_document(db, patient_id)
        add_lab(
            db, patient_id, document_id, "TEST_UPDATE",
            11.0, date(2026, 1, 1)
        )
        add_lab(
            db, patient_id, document_id, "TEST_UPDATE",
            13.0, date(2026, 2, 1)
        )
        db.commit()
    finally:
        db.close()

    update_patient_trends(patient_id)

    db = SessionLocal()
    try:
        first = db.execute(
            text("""
                SELECT latest_value, data_points
                FROM lab_trends
                WHERE patient_id = :pid AND test_name = 'TEST_UPDATE'
            """),
            {"pid": patient_id},
        ).one()
        assert first.latest_value == pytest.approx(13.0)
        assert first.data_points == 2
    finally:
        db.close()

    db = SessionLocal()
    try:
        document_id = add_document(db, patient_id)
        add_lab(
            db, patient_id, document_id, "TEST_UPDATE",
            16.0, date(2026, 3, 1)
        )
        db.commit()
    finally:
        db.close()

    update_patient_trends(patient_id)

    db = SessionLocal()
    try:
        rows = db.execute(
            text("""
                SELECT latest_value, delta, data_points
                FROM lab_trends
                WHERE patient_id = :pid AND test_name = 'TEST_UPDATE'
            """),
            {"pid": patient_id},
        ).fetchall()

        assert len(rows) == 1
        assert rows[0].latest_value == pytest.approx(16.0)
        assert rows[0].delta == pytest.approx(3.0)
        assert rows[0].data_points == 3
    finally:
        db.close()
