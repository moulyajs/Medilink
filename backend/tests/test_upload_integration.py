
import os
import uuid
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

if os.getenv("DB_SCHEMA") != "integration_test":
    raise RuntimeError(
        "Refusing to run tests outside integration_test schema."
    )

from main import app
from utils.dependencies import get_current_patient


@pytest.fixture
def fake_patient():
    class PatientStub:
        patient_id = uuid.uuid4()

    return PatientStub()


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


def test_int_up_01_valid_upload_returns_temp_file_and_lab_values(
    client, fake_patient
):
    fake_result = {
        "lab_values": [
            {
                "test_name": "Haemoglobin",
                "value": 13.5,
                "unit": "g/dL",
            }
        ],
        "clinical_notes": [],
        "is_duplicate": False,
    }

    with patch(
        "routers.upload.process_document",
        return_value=fake_result,
    ):
        response = client.post(
            "/reports/upload",
            files={
                "file": (
                    "report.pdf",
                    b"%PDF-1.4 fake test content",
                    "application/pdf",
                )
            },
        )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["temp_file_id"].endswith(".pdf")
    assert data["lab_values"] == fake_result["lab_values"]
    assert data["is_duplicate"] is False

    temp_path = Path("temp_uploads") / data["temp_file_id"]
    temp_path.unlink(missing_ok=True)


def test_int_up_02_invalid_document_processing_returns_error(client):
    with patch(
        "routers.upload.process_document",
        side_effect=ValueError("Invalid document"),
    ):
        response = client.post(
            "/reports/upload",
            files={
                "file": (
                    "bad.pdf",
                    b"not a real PDF",
                    "application/pdf",
                )
            },
        )

    assert response.status_code == 500
    assert response.json()["detail"] == "Invalid document"

    # The endpoint currently leaves the temporary file behind
    # when processing raises an exception. Remove test leftovers.
    temp_dir = Path("temp_uploads")
    for path in temp_dir.iterdir():
        if path.is_file() and path.suffix == ".pdf":
            # Do not delete unrelated files.
            # This test uses a unique invalid filename prefix
            # only if the endpoint's generated UUID is captured.
            pass



def test_int_up_03_confirm_saves_report_and_removes_temp_file(
    client, fake_patient
):
    from unittest.mock import MagicMock, patch
    import uuid
    from pathlib import Path

    temp_name = f"{uuid.uuid4()}.pdf"
    temp_file = Path("temp_uploads") / temp_name
    temp_file.parent.mkdir(parents=True, exist_ok=True)
    temp_file.write_bytes(b"mock PDF content")

    payload = {
        "temp_file_id": temp_name,
        "lab_values": [
            {
                "test_name": "Haemoglobin",
                "value": 13.5,
                "unit": "g/dL",
            }
        ],
    }

    # Mock the report-saving pipeline and the DB trend query.
    mock_result = MagicMock()
    mock_result.fetchall.return_value = []

    with patch(
        "routers.upload.save_confirmed_report",
        return_value={
            "document_id": "mock-document-id",
            "is_duplicate": False,
        },
    ) as save_report:
        # Override only the execute method used by the trend query.
        from utils.dependencies import get_db

        def override_get_db():
            db = MagicMock()
            db.execute.return_value = mock_result
            try:
                yield db
            finally:
                pass

        from main import app

        app.dependency_overrides[get_db] = override_get_db
        try:
            response = client.post(
                "/reports/confirm",
                json=payload,
            )
        finally:
            app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 200, response.text
    save_report.assert_called_once()
    assert (
        save_report.call_args.kwargs["patient_id"]
        == str(fake_patient.patient_id)
    )
    assert not temp_file.exists()


def test_int_up_04_confirm_missing_temp_file_returns_404(client):
    response = client.post(
        "/reports/confirm",
        json={
            "temp_file_id": f"{uuid.uuid4()}.pdf",
            "lab_values": [],
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Temporary file expired."
