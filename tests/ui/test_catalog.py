"""Sprint 2 - Catalog, search, sorting, filtering, and external link tests."""
import re

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


def test_filter_category_hammer_shows_only_hammers(page):
    """Goal: verify checking a category filter narrows the product grid.
    Precondition: 'Hammer' category exists on the home page sidebar.
    Expected: filter completes and every visible product name contains 'hammer'."""
    home = HomePage(page).open().filter_by_category("Hammer")
    expect(home.filter_completed).to_be_visible()
    names = home.product_names.all_inner_texts()
    assert names, "category filter returned no products"
    assert all("hammer" in name.lower() for name in names), names


def test_filter_price_slider_caps_displayed_prices(page):
    """Goal: verify lowering the max price slider filters out higher-priced items.
    Precondition: home page price range slider is visible.
    Expected: max slider value becomes '20' and every displayed price is at most 20."""
    home = HomePage(page).open().lower_max_price_to(20)
    expect(home.price_slider_max).to_have_attribute("aria-valuenow", "20")
    expect(home.prices_above_twenty()).to_have_count(0)
    prices = home.prices()
    assert prices and all(price <= 20.0 for price in prices), prices


def test_product_detail_shows_correct_name_and_price(page):
    """Goal: verify opening a product navigates to detail page with matching name.
    Precondition: 'Combination Pliers' exists in catalogue.
    Expected: product detail page displays correct title and positive unit price."""
    product = HomePage(page).open().open_product("Combination Pliers")
    expect(product.name).to_have_text("Combination Pliers")
    assert product.price() > 0


def test_footer_github_link_opens_in_new_tab(page):
    """Goal: verify the footer GitHub link opens the repository in a new browser tab.
    Precondition: home page footer is rendered.
    Expected: a new page opens in the context whose URL points to the GitHub repo."""
    home = HomePage(page).open()
    new_tab = home.open_github_in_new_tab()
    expect(new_tab).to_have_url(re.compile(r"github\.com/.+/practice-software-testing"))
    new_tab.close()
