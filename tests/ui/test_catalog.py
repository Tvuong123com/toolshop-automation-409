"""Sprint 2 - Catalog, search, and sorting tests."""
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage

pytestmark = pytest.mark.ui


def test_search_unknown_keyword_shows_no_results_message(page):
    """Goal: verify empty search state when no products match keyword.
    Precondition: home page reachable.
    Expected: 'There are no products found.' message and 0 product cards."""
    home = HomePage(page).open().search("zzz-no-such-tool")
    expect(home.no_results).to_have_text("There are no products found.")
    expect(home.product_names).to_have_count(0)


@pytest.mark.parametrize("order", ["price,asc", "price,desc"])
def test_sort_by_price_orders_products(page, order):
    """Goal: verify sorting products by price in ascending and descending order.
    Precondition: home page has multiple products with prices.
    Expected: prices on the first page match the requested order."""
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    home.sort_by(order)
    expect(home.sorting_completed).to_be_visible()
    prices = home.prices()
    assert prices == sorted(prices, reverse=order.endswith("desc")), prices


def test_product_detail_shows_correct_name_and_price(page):
    """Goal: verify opening a product navigates to detail page with matching name.
    Precondition: 'Combination Pliers' exists in catalogue.
    Expected: product detail page displays correct title and positive unit price."""
    product = HomePage(page).open().open_product("Combination Pliers")
    expect(product.name).to_have_text("Combination Pliers")
    assert product.price() > 0
