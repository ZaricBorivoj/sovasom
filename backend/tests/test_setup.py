import os
import subprocess
import sys
from pathlib import Path

from dotenv import dotenv_values, set_key
from fastapi.testclient import TestClient


def test_setup_is_atomic_and_reruns_never_change_credentials(database_url, tmp_path):
    from office.app import create_app
    from office.config import Settings

    secret = tmp_path / ".env"
    repository = Path(__file__).resolve().parents[2]
    working = tmp_path / "operator"
    working.mkdir()
    (working / "alembic.ini").write_text(
        f"[alembic]\nscript_location = {repository}/backend/migrations\n"
        f"prepend_sys_path = {repository}/backend\n"
    )

    def setup(email, name, password):
        secret.write_text("# Runtime configuration stays after setup\n")
        for key, value in {
            "DATABASE_URL": database_url,
            "INITIAL_EMAIL": email,
            "INITIAL_DISPLAY_NAME": name,
            "INITIAL_PASSWORD": password,
        }.items():
            set_key(secret, key, value)
        return subprocess.run(
            [sys.executable, "-m", "office.setup", "--env-file", str(secret)],
            env={
                **{
                    key: value
                    for key, value in os.environ.items()
                    if not key.startswith("INITIAL_") and key != "DATABASE_URL"
                },
                "PYTHONPATH": str(repository / "backend"),
            },
            cwd=working,
            capture_output=True,
            text=True,
        )

    invalid = setup("bad email", "First colleague", "a synthetic long password")
    assert invalid.returncode != 0
    assert secret.exists()
    assert (
        dotenv_values(secret, interpolate=False)["INITIAL_PASSWORD"] == "a synthetic long password"
    )
    assert "a synthetic long password" not in invalid.stdout + invalid.stderr
    first = setup("first@example.com", "First colleague", "a synthetic long password")
    assert first.returncode == 0, first.stderr
    assert dotenv_values(secret) == {"DATABASE_URL": database_url}
    assert secret.stat().st_mode & 0o777 == 0o600
    again = setup("changed@example.com", "Changed colleague", "a changed synthetic password")
    assert again.returncode == 0, again.stderr
    assert dotenv_values(secret) == {"DATABASE_URL": database_url}
    client = TestClient(
        create_app(Settings(_env_file=None, database_url=database_url)),
        base_url="https://testserver",
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
