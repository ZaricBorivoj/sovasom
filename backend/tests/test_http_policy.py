import pytest
from fastapi.testclient import TestClient
from office.app import create_app
from office.config import Settings


def test_login_csrf_is_rejected_before_database_access():
    app = create_app(Settings(database_url="postgresql+psycopg://unused:unused@localhost/unused"))
    client = TestClient(app, base_url="https://testserver")
    response = client.post("/api/auth/login", json={"email": "a@example.com", "password": "secret"})
    assert response.status_code == 403
    assert "secret" not in response.text


@pytest.mark.parametrize("origin", ["http://office.example.com", "https://office.example.com/path"])
def test_insecure_or_ambiguous_origin_is_rejected(origin):
    with pytest.raises(ValueError, match="HTTPS origin"):
        Settings(database_url="unused", public_origin=origin)
