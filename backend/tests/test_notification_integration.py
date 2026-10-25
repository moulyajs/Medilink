
import os
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

if os.getenv("DB_SCHEMA") != "integration_test":
    raise RuntimeError(
        "Refusing to run tests outside integration_test schema."
    )

from main import app
from database import SessionLocal
from models.notification import Notification
from models.patient import Patient
from utils.dependencies import get_current_patient, get_db



@pytest.fixture
def test_patient_ids():
    """Get patient IDs through the ORM in the integration-test schema."""
    db = SessionLocal()
    try:
        patients = (
            db.query(Patient)
            .order_by(Patient.patient_id)
            .limit(2)
            .all()
        )

        if len(patients) < 2:
            pytest.skip(
                "Two ORM-visible patients are required for isolation testing."
            )

        return [patient.patient_id for patient in patients]
    finally:
        db.close()



@pytest.fixture
def fake_patient(test_patient_ids):
    return SimpleNamespace(patient_id=test_patient_ids[0])


@pytest.fixture
def client(fake_patient):
    async def override_current_patient():
        return fake_patient

    app.dependency_overrides[get_current_patient] = (
        override_current_patient
    )

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_current_patient, None)
        app.dependency_overrides.pop(get_db, None)


def test_int_not_01_upload_generates_notification(client, fake_patient):
    """Report confirmation generates a report-upload notification."""
    temp_name = f"{uuid.uuid4()}.pdf"
    temp_file = Path("temp_uploads") / temp_name
    temp_file.parent.mkdir(parents=True, exist_ok=True)
    temp_file.write_bytes(b"mock PDF content")

    mock_db = MagicMock()
    mock_db.execute.return_value.fetchall.return_value = []

    def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with patch(
            "routers.upload.save_confirmed_report",
            return_value={
                "document_id": str(uuid.uuid4()),
                "is_duplicate": False,
            },
        ):
            response = client.post(
                "/reports/confirm",
                json={
                    "temp_file_id": temp_name,
                    "lab_values": [],
                },
            )
    finally:
        temp_file.unlink(missing_ok=True)

    assert response.status_code == 200, response.text

    added_notifications = [
        call.args[0]
        for call in mock_db.add.call_args_list
        if call.args and isinstance(call.args[0], Notification)
    ]

    assert any(
        n.patient_id == fake_patient.patient_id
        and n.notification_type == "report"
        and n.title == "Report Uploaded"
        for n in added_notifications
    )


def test_int_not_02_anomaly_generates_notification(client, fake_patient):
    """An existing anomaly produces an alert on report confirmation."""
    temp_name = f"{uuid.uuid4()}.pdf"
    temp_file = Path("temp_uploads") / temp_name
    temp_file.parent.mkdir(parents=True, exist_ok=True)
    temp_file.write_bytes(b"mock PDF content")

    mock_db = MagicMock()

    trend_result = MagicMock()
    trend_result.fetchall.return_value = []

    anomaly_result = MagicMock()
    anomaly_result.fetchall.return_value = [
        SimpleNamespace(test_name="HAEMOGLOBIN")
    ]

    mock_db.execute.side_effect = [trend_result, anomaly_result]
    mock_db.query.return_value.filter.return_value.first.return_value = None

    def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with patch(
            "routers.upload.save_confirmed_report",
            return_value={
                "document_id": str(uuid.uuid4()),
                "is_duplicate": False,
            },
        ):
            response = client.post(
                "/reports/confirm",
                json={
                    "temp_file_id": temp_name,
                    "lab_values": [],
                },
            )
    finally:
        temp_file.unlink(missing_ok=True)

    assert response.status_code == 200, response.text

    added_notifications = [
        call.args[0]
        for call in mock_db.add.call_args_list
        if call.args and isinstance(call.args[0], Notification)
    ]

    assert any(
        n.patient_id == fake_patient.patient_id
        and n.notification_type == "anomaly"
        and n.title == "Anomaly Detected"
        and "HAEMOGLOBIN" in n.message
        for n in added_notifications
    )


def test_int_not_04_notification_persists_in_database(fake_patient):
    """A notification created through the service is persisted."""
    from schemas.notification import NotificationCreate
    from services.notification_service import create_notification_service

    db = SessionLocal()
    notification_id = None

    try:
        patient = db.query(Patient).filter(
            Patient.patient_id == fake_patient.patient_id
        ).first()

        assert patient is not None, "Test patient must exist"

        request = NotificationCreate(
            title="Integration test",
            message="Persistence verification",
            notification_type="report",
        )

        notification = create_notification_service(
            request=request,
            current_patient=patient,
            db=db,
        )
        notification_id = notification.notification_id

        # Query again to verify the record was committed.
        db.expire_all()
        saved = db.query(Notification).filter(
            Notification.notification_id == notification_id
        ).first()

        assert saved is not None
        assert saved.patient_id == patient.patient_id
        assert saved.title == "Integration test"
        assert saved.message == "Persistence verification"

    finally:
        if notification_id is not None:
            db.query(Notification).filter(
                Notification.notification_id == notification_id
            ).delete(synchronize_session=False)
            db.commit()
        db.close()


def test_int_not_06_patient_sees_only_own_notifications(
    client, fake_patient, test_patient_ids
):
    """The notification API returns only the authenticated patient's records."""
    own_patient_id, other_patient_id = test_patient_ids
    db = SessionLocal()
    created_ids = []

    try:
        own_notification = Notification(
            patient_id=own_patient_id,
            title="Own test notification",
            message="Belongs to authenticated patient",
            notification_type="report",
        )
        other_notification = Notification(
            patient_id=other_patient_id,
            title="Other test notification",
            message="Must not be visible",
            notification_type="report",
        )

        db.add_all([own_notification, other_notification])
        db.commit()
        db.refresh(own_notification)
        db.refresh(other_notification)

        created_ids = [
            own_notification.notification_id,
            other_notification.notification_id,
        ]

        response = client.get("/notifications/history")

        assert response.status_code == 200, response.text

        returned_ids = {
            item["notification_id"] for item in response.json()
        }

        assert str(own_notification.notification_id) in returned_ids
        assert str(other_notification.notification_id) not in returned_ids

    finally:
        if created_ids:
            db.query(Notification).filter(
                Notification.notification_id.in_(created_ids)
            ).delete(synchronize_session=False)
            db.commit()
        db.close()
