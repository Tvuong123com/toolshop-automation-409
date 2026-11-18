"""Sprint 2 - Users API tests."""
import pytest

pytestmark = pytest.mark.api


def test_register_empty_body_returns_422_with_field_errors(api):
    """Goal: server-side validation on user registration.
    Precondition: none.
    Expected: status 422 and field error lists for 'email' and 'password'."""
    response = api.post("/users/register", data={})
    assert response.status == 422, response.text()
    errors = response.json()
    assert "email" in errors and "password" in errors, errors


def test_users_me_with_token_returns_own_profile(api, auth_headers, test_user):
    """Goal: bearer token grants access to personal profile.
    Precondition: user registered and logged in via auth_headers fixture.
    Expected: status 200 and email matches registered account."""
    response = api.get("/users/me", headers=auth_headers)
    assert response.status == 200, response.text()
    assert response.json()["email"] == test_user["email"]
