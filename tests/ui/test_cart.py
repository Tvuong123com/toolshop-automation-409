"""Sprint 2 - Cart interactions and calculations tests."""
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage

pytestmark = pytest.mark.ui


def test_cart_line_price_equals_unit_price_times_quantity(page):
    """Goal: verify cart calculations compute correct line total and cart total.
    Precondition: cart is empty on start.
    Expected: line total equals unit price multiplied by 2, and grand total matches."""
    product = HomePage(page).open().open_product("Claw Hammer")
    unit = product.price()
    product.add_to_cart(quantity=2)
    expect(product.cart_quantity).to_have_text("2")
    cart = product.go_to_cart()
    expect(cart.product_titles).to_have_count(1)
    assert cart.line_totals() == [pytest.approx(unit * 2)]
    assert cart.total_value() == pytest.approx(sum(cart.line_totals()))


def test_cart_continue_shopping_returns_to_home(page):
    """Goal: verify 'Continue Shopping' button navigates back to product catalog.
    Precondition: product added to cart and cart page opened.
    Expected: clicking continue shopping returns to home page with product grid visible."""
    cart = HomePage(page).open().open_product("Hammer").add_to_cart().go_to_cart()
    expect(cart.product_titles.first).to_have_text("Hammer")
    cart.continue_shopping.click()
    expect(HomePage(page).product_names.first).to_be_visible()
