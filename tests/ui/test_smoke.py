"""Sprint 1 smoke tests using Page Object Model."""
import re

import pytest
from playwright.sync_api import expect

from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.ui
def test_search_pliers_shows_matching_products(page):
    """Goal: verify search filters products by keyword.
    Precondition: Toolshop home page is reachable.
    Expected: search completes and every displayed product name contains 'pliers'."""
    home = HomePage(page).open().search("pliers")
    expect(home.search_completed).to_be_visible()
    expect(home.search_caption).to_contain_text("pliers")
    names = home.product_names.all_inner_texts()
    assert names, "search returned no products"
    assert all("pliers" in name.lower() for name in names), names


@pytest.mark.smoke
@pytest.mark.ui
def test_cart_add_claw_hammer_quantity_three_updates_badge(page):
    """Goal: verify adding a product updates the cart badge with the selected quantity.
    Precondition: product 'Claw Hammer' exists in the catalogue.
    Expected: cart badge in the header displays '3'."""
    product = HomePage(page).open().open_product("Claw Hammer")
    expect(product.name).to_have_text("Claw Hammer")
    product.add_to_cart(quantity=3)
    expect(product.toast).to_contain_text("Product added to shopping cart")
    expect(product.cart_quantity).to_have_text("3")


@pytest.mark.smoke
@pytest.mark.ui
def test_login_invalid_credentials_shows_error(page):
    """Goal: verify login rejects a non-existent email and arbitrary password.
    Precondition: email has no registered account (never use shared accounts).
    Expected: 'Invalid email or password' is shown and URL still ends with /auth/login."""
    login = LoginPage(page).open().login("nobody-here@example.com", "Wrong-Password-123")
    expect(login.error).to_contain_text("Invalid email or password")
    expect(page).to_have_url(re.compile(r"/auth/login$"))


@pytest.mark.smoke
@pytest.mark.ui
def test_contact_empty_form_shows_required_errors(page):
    """Goal: verify required field validation on an empty contact form submission.
    Precondition: none.
    Expected: 'Subject is required' and 'Message is required' validation errors are visible."""
    contact = ContactPage(page).open().submit()
    expect(contact.errors.filter(has_text="Subject is required")).to_be_visible()
    expect(contact.errors.filter(has_text="Message is required")).to_be_visible()

