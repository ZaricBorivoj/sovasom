import json
import os
import subprocess
import sys

from fastapi.testclient import TestClient


def test_setup_is_atomic_and_reruns_never_change_credentials(database_url, tmp_path):
    from office.app import create_app
    from office.config import Settings

    secret = tmp_path / "bootstrap.json"

    def setup(email, name, password):
        secret.write_text(json.dumps({"email": email, "display_name": name, "password": password}))
        return subprocess.run(
            [sys.executable, "-m", "office.setup", "--bootstrap-file", str(secret)],
            env={**os.environ, "DATABASE_URL": database_url, "PYTHONPATH": "backend"},
            capture_output=True,
            text=True,
        )

    invalid = setup("bad email", "First colleague", "a synthetic long password")
    assert invalid.returncode != 0
    assert secret.exists()
    assert "a synthetic long password" not in invalid.stdout + invalid.stderr
    first = setup("first@example.com", "First colleague", "a synthetic long password")
    assert first.returncode == 0, first.stderr
    assert not secret.exists()
    again = setup("changed@example.com", "Changed colleague", "a changed synthetic password")
    assert again.returncode == 0, again.stderr
    assert not secret.exists()
    client = TestClient(
        create_app(Settings(database_url=database_url)), base_url="https://testserver"
    )
    token = client.get("/api/auth/csrf").json()["csrf_token"]
    response = client.post(
        "/api/auth/login",
        json={"email": "first@example.com", "password": "a synthetic long password"},
        headers={"Origin": "https://testserver", "X-CSRF-Token": token},
    )
    assert response.status_code == 200
    assert response.json()["account"]["display_name"] == "First colleague"
    assert response.json()["account"]["is_administrator"] is True
    assert response.json()["account"]["is_menu_maintainer"] is True
    assert client.get("/api/office/home").status_code == 200
