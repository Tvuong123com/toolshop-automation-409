"""Sprint 2b - BDD shopping cart flow with pytest-bdd."""
import pytest
from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from pages.home_page import HomePage

pytestmark = [pytest.mark.bdd, pytest.mark.ui]

scenarios("cart_flow.feature")


@given("I am on the home page", target_fixture="home")
def home(page):
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    return home


@when(parsers.parse('I search for "{keyword}"'))
def search_product(home, keyword):
    home.search(keyword)
    expect(home.search_completed).to_be_visible()


@when(parsers.parse('I open product "{product}"'), target_fixture="product_page")
def open_product(home, product):
    product_page = home.open_product(product)
    expect(product_page.unit_price).to_be_visible()
    return product_page


@when(parsers.parse('I add the product to the cart with quantity {quantity:d}'), target_fixture="cart_data")
def add_to_cart(product_page, quantity):
    unit_price = product_page.price()
    product_page.add_to_cart(quantity=quantity)
    expect(product_page.cart_quantity).to_have_text(str(quantity))
    return {"product_page": product_page, "unit_price": unit_price, "quantity": quantity}


@when("I navigate to the shopping cart", target_fixture="cart_page")
def navigate_to_cart(cart_data):
    cart_page = cart_data["product_page"].go_to_cart()
    expect(cart_page.product_titles.first).to_be_visible()
    return cart_page


@then(parsers.parse('the cart displays product "{product}"'))
def verify_cart_product(cart_page, product):
    expect(cart_page.product_titles.first).to_have_text(product)


@then(parsers.parse("the line price matches the unit price multiplied by {quantity:d}"))
def verify_line_price(cart_page, cart_data, quantity):
    expected = cart_data["unit_price"] * quantity
    assert cart_page.line_totals() == [pytest.approx(expected)]


@then("the cart total equals the sum of line prices")
def verify_cart_total(cart_page):
    assert cart_page.total_value() == pytest.approx(sum(cart_page.line_totals()))
