from datetime import timedelta

import pytest
from conftest import sign_in
from office.accounts.models import Account, Grant, LoginSession, Membership
from sqlalchemy import select, update


def test_login_survives_new_http_client_and_logout_revokes_copied_cookie(office):
    client, _, _ = office
    response = sign_in(client)
    assert response.status_code == 200
    identity = response.json()
    assert identity["account"]["email"] == "colleague@example.com"
    for value in response.headers.get_list("set-cookie"):
        assert all(flag in value for flag in ["Secure", "HttpOnly", "SameSite=strict", "Path=/"])
    saved = dict(client.cookies)
    client.cookies.clear()
    client.cookies.update(saved)
    assert client.get("/api/office/home").json() == {"active_run": None, "history": []}
    # Fetching a CSRF token in another tab must not break the active session.
    assert client.get("/api/auth/csrf").json()["csrf_token"] == identity["csrf_token"]
    assert (
        client.post(
            "/api/auth/logout",
            headers={
                "Origin": "https://testserver",
                "X-CSRF-Token": identity["csrf_token"],
            },
        ).status_code
        == 204
    )
    client.cookies.update(saved)
    assert client.get("/api/office/home").status_code == 401


def test_session_has_exactly_30_days_absolute_lifetime(office):
    client, now, _ = office
    assert sign_in(client).status_code == 200
    now[0] += timedelta(days=30, microseconds=-1)
    assert client.get("/api/office/home").status_code == 200
    now[0] += timedelta(microseconds=1)
    assert client.get("/api/office/home").status_code == 401
    assert client.get("/api/auth/session").status_code == 401


@pytest.mark.parametrize("change", ["membership", "account", "session"])
def test_current_access_is_checked_on_every_request(office, change):
    client, now, sessions = office
    assert sign_in(client).status_code == 200
    with sessions.begin() as db:
        if change == "membership":
            db.execute(update(Membership).values(active=False))
        elif change == "account":
            db.execute(update(Account).values(enabled=False))
        else:
            db.execute(update(LoginSession).values(revoked_at=now[0]))
    assert client.get("/api/office/home").status_code == (403 if change == "membership" else 401)


def test_anonymous_and_forged_sessions_cannot_read_office(office):
    client, _, _ = office
    assert client.get("/api/office/home").status_code == 401
    client.cookies.set("__Host-office_session", "forged")
    assert client.get("/api/auth/session").status_code == 401


def test_invalid_credentials_are_generic_and_login_is_case_insensitive(office):
    client, _, _ = office
    known = sign_in(client, password="wrong password")
    unknown = sign_in(client, email="unknown@example.com")
    assert known.status_code == unknown.status_code == 401
    assert known.json() == unknown.json()
    assert sign_in(client, email=" COLLEAGUE@EXAMPLE.COM ").status_code == 200


def test_permissions_are_current_and_office_payload_exposes_no_email(office):
    client, _, sessions = office
    assert sign_in(client).status_code == 200
    account_id = client.get("/api/auth/session").json()["account"]["id"]
    with sessions.begin() as db:
        for grant in db.scalars(select(Grant)):
            db.delete(grant)
    account = client.get("/api/auth/session").json()["account"]
    assert account["id"] == account_id
    assert account["is_administrator"] is False
    assert account["is_menu_maintainer"] is False
    assert "email" not in client.get("/api/office/home").text


@pytest.mark.parametrize("attack", ["missing", "wrong-token", "foreign-origin", "missing-origin"])
def test_csrf_denial_does_not_revoke_the_session(office, attack):
    client, _, _ = office
    token = sign_in(client).json()["csrf_token"]
    headers = {"Origin": "https://testserver", "X-CSRF-Token": token}
    if attack == "missing":
        headers.pop("X-CSRF-Token")
    elif attack == "wrong-token":
        headers["X-CSRF-Token"] = "forged"
    elif attack == "foreign-origin":
        headers["Origin"] = "https://attacker.example.com"
    else:
        headers.pop("Origin")
    assert client.post("/api/auth/logout", headers=headers).status_code == 403
    assert client.get("/api/office/home").status_code == 200


def test_session_csrf_is_bound_to_session_even_if_cookie_and_header_match(office):
    client, _, _ = office
    sign_in(client)
    client.cookies.clear()
    # Use a real session with a forged double-submit pair.
    sign_in(client)
    saved = client.cookies.get("__Host-office_session")
    client.cookies.clear()
    client.cookies.set("__Host-office_session", saved)
    client.cookies.set("__Host-office_csrf", "forged")
    assert (
        client.post(
            "/api/auth/logout",
            headers={
                "Origin": "https://testserver",
                "X-CSRF-Token": "forged",
            },
        ).status_code
        == 403
    )
