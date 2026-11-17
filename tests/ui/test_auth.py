"""Sprint 2 - Authentication and account tests."""
import pytest
from playwright.sync_api import expect

from pages.account_page import AccountPage
from pages.login_page import LoginPage

pytestmark = pytest.mark.ui


def test_login_empty_form_shows_required_errors(page):
    """Goal: verify client-side validation on empty login form submission.
    Precondition: user is on login page.
    Expected: error messages 'Email is required' and 'Password is required' appear."""
    login = LoginPage(page).open()
    login.submit_button.click()
    expect(login.email_error).to_contain_text("Email is required")
    expect(login.password_error).to_contain_text("Password is required")


def test_account_page_logged_in_shows_user_menu(logged_in_page):
    """Goal: verify navigating to account page with pre-authenticated storage state.
    Precondition: user is authenticated once per session via storage_state.
    Expected: account title displays 'My account' and user navigation shows 'QA Bot'."""
    account = AccountPage(logged_in_page).open()
    expect(account.title).to_have_text("My account")
    expect(account.nav_menu).to_contain_text("QA Bot")
