import json
import os
import subprocess
import sys
import uuid
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url


@pytest.fixture
def database_url():
    # Never reset a developer/production database. Each test owns a new database.
    server_url = os.environ.get("TEST_DATABASE_URL")
    if not server_url:
        pytest.fail("TEST_DATABASE_URL must point to the isolated test PostgreSQL server")
    name = "office_test_" + uuid.uuid4().hex
    admin = create_engine(server_url, isolation_level="AUTOCOMMIT")
    with admin.connect() as connection:
        connection.execute(text(f'CREATE DATABASE "{name}"'))
    yield make_url(server_url).set(database=name).render_as_string(hide_password=False)
    with admin.connect() as connection:
        connection.execute(text(f'DROP DATABASE "{name}" WITH (FORCE)'))
    admin.dispose()


@pytest.fixture
def office(database_url):
    from office.app import create_app
    from office.config import Settings

    result = subprocess.run(
        [sys.executable, "-m", "office.setup", "--stdin"],
        env={
            **os.environ,
            "DATABASE_URL": database_url,
            "PYTHONPATH": "backend",
        },
        input=json.dumps(
            {
                "email": "colleague@example.com",
                "display_name": "Test colleague",
                "password": "synthetic password only",
            }
        ),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    now = [datetime(2026, 11, 23, 9, 0, tzinfo=UTC)]
    app = create_app(Settings(_env_file=None, database_url=database_url), clock=lambda: now[0])
    with TestClient(app, base_url="https://testserver") as client:
        yield client, now, app.state.sessions


def sign_in(client, password="synthetic password only", email="colleague@example.com"):
    token = client.get("/api/auth/csrf").json()["csrf_token"]
    return client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
        headers={"Origin": "https://testserver", "X-CSRF-Token": token},
    )
