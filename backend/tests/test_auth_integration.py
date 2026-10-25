
import os
import uuid

if os.getenv("DB_SCHEMA") != "integration_test":
    raise RuntimeError(
        "Refusing to run tests: DB_SCHEMA must be integration_test."
    )

import pytest
from fastapi.testclient import TestClient

from database import Base, SessionLocal, get_db, engine
from main import app
from models.patient import Patient
from models.device import Device


@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    schema_map = engine.get_execution_options().get(
        "schema_translate_map", {}
    )
    if schema_map.get(None) != "integration_test":
        raise RuntimeError(
            "Engine is not configured for integration_test."
        )

    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def test_email():
    return f"inttest_{uuid.uuid4().hex[:16]}@example.com"


@pytest.fixture
def cleanup_patient():
    emails = []
    yield emails

    db = SessionLocal()
    try:
        for email in emails:
            patient = (
                db.query(Patient)
                .filter(Patient.email == email)
                .first()
            )

            if patient:
                # Delete dependent device records first.
                db.query(Device).filter(
                    Device.patient_id == patient.patient_id
                ).delete(synchronize_session=False)

                # Delete the patient after dependent records.
                db.delete(patient)

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def signup_payload(email):
    return {
        "name": "Integration Test Patient",
        "email": email,
        "password": "TestPassword123!",
    }


def register_patient(client, email, cleanup_patient):
    cleanup_patient.append(email)

    response = client.post(
        "/auth/signup",
        json=signup_payload(email),
    )

    assert response.status_code == 201, response.text


def login_patient(client, email):
    return client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "TestPassword123!",
        },
    )


def extract_token(response):
    data = response.json()

    token = data.get("access_token") or data.get("token")

    if not token and isinstance(data.get("data"), dict):
        token = (
            data["data"].get("access_token")
            or data["data"].get("token")
        )

    assert token, (
        "Login response did not contain an access token. "
        f"Response keys: {list(data.keys())}"
    )

    return token


def test_int_auth_01_signup_persists_patient_and_profile(
    client, test_email, cleanup_patient
):
    register_patient(client, test_email, cleanup_patient)

    db = SessionLocal()
    try:
        patient = (
            db.query(Patient)
            .filter(Patient.email == test_email)
            .first()
        )

        assert patient is not None
        assert patient.password_hash != "TestPassword123!"
        assert patient.profile is not None
        assert patient.profile.name == "Integration Test Patient"
    finally:
        db.close()


def test_int_auth_02_duplicate_signup_is_rejected(
    client, test_email, cleanup_patient
):
    register_patient(client, test_email, cleanup_patient)

    second = client.post(
        "/auth/signup",
        json=signup_payload(test_email),
    )

    assert second.status_code == 400
    assert second.json()["detail"] == "Email already registered."

    db = SessionLocal()
    try:
        count = (
            db.query(Patient)
            .filter(Patient.email == test_email)
            .count()
        )

        assert count == 1
    finally:
        db.close()


def test_int_auth_03_login_with_valid_credentials(
    client, test_email, cleanup_patient
):
    register_patient(client, test_email, cleanup_patient)

    response = login_patient(client, test_email)

    assert response.status_code == 200, response.text
    extract_token(response)


def test_int_auth_04_login_with_wrong_password(
    client, test_email, cleanup_patient
):
    register_patient(client, test_email, cleanup_patient)

    response = client.post(
        "/auth/login",
        json={
            "email": test_email,
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code in (400, 401, 403), response.text


def test_int_auth_05_protected_endpoint_with_valid_token(
    client, test_email, cleanup_patient
):
    register_patient(client, test_email, cleanup_patient)

    login_response = login_patient(client, test_email)
    assert login_response.status_code == 200, login_response.text

    token = extract_token(login_response)

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200, response.text


def test_int_auth_06_protected_endpoint_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code in (401, 403), response.text


def test_int_auth_07_protected_endpoint_with_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid.test.token"},
    )

    assert response.status_code in (401, 403), response.text
