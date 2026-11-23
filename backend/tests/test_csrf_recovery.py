from conftest import sign_in


def test_session_recovers_after_anonymous_csrf_navigation_replaces_its_cookie(office):
    client, _, _ = office
    assert sign_in(client).status_code == 200
    original = dict(client.cookies)
    # SameSite=Strict omits both cookies on a cross-site top-level navigation.
    client.cookies.clear()
    replacement = client.get("/api/auth/csrf").json()["csrf_token"]
    client.cookies.clear()
    original["__Host-office_csrf"] = replacement
    client.cookies.update(original)
    identity = client.get("/api/auth/session")
    assert identity.status_code == 200
    assert (
        client.post(
            "/api/auth/logout",
            headers={
                "Origin": "https://testserver",
                "X-CSRF-Token": identity.json()["csrf_token"],
            },
        ).status_code
        == 204
    )
