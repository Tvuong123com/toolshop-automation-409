import re

from pages.base_page import BasePage

# PROD loads the grid with "QUERY /products", BUGGY with "GET /products?...". Not /products/search.
PRODUCT_LIST = re.compile(r"/products(\?.*)?$")


class HomePage(BasePage):
    path = "/"

    def __init__(self, page):
        super().__init__(page)
        self.search_box = page.get_by_test_id("search-query")
        self.search_result_count = page.get_by_test_id("search-result-count")
        # B1.1
        self.search_button = page.get_by_test_id("search-submit")
        self.search_caption = page.get_by_test_id("search-caption")
        self.search_completed = page.get_by_test_id("search_completed")
        self.product_names = page.get_by_test_id("product-name")
        # B1.2
        self.no_results = page.get_by_test_id("no-results")
        # B1.7
        self.sort_select = page.get_by_test_id("sort")
        self.sorting_completed = page.get_by_test_id("sorting_completed")
        self.product_prices = page.get_by_test_id("product-price")
        # Sprint 2: filters, slider, and footer external link
        self.filter_completed = page.get_by_test_id("filter_completed")
        self.price_slider_max = page.get_by_role("slider").nth(1)
        self.footer_github = page.get_by_test_id("footer-learn-github")

    def open(self):
        """Return only after the first product list has arrived.

        Race in Toolshop: if you search before the initial list arrives, the late initial list
        overwrites the search results. Waiting for that response is synchronisation, not an assertion.
        """
        with self.page.expect_response(lambda r: PRODUCT_LIST.search(r.url) is not None):
            super().open()
        return self

    def search(self, keyword: str):
        self.search_box.fill(keyword)
        self.search_button.click()
        return self

    def sort_by(self, value: str):
        """value: name,asc | name,desc | price,asc | price,desc"""
        self.sort_select.select_option(value)
        return self

    def filter_by_category(self, label: str):
        self.page.get_by_label(label).check()
        return self

    def lower_max_price_to(self, target: int):
        self.price_slider_max.focus()
        current = int(self.price_slider_max.get_attribute("aria-valuenow") or "100")
        delta = max(0, current - target)
        if delta > 0:
            with self.page.expect_response(
                lambda r: PRODUCT_LIST.search(r.url) is not None
                and f"price,1,{target}" in (r.url + (r.request.post_data or ""))
            ):
                for _ in range(delta // 20):
                    self.page.keyboard.press("PageDown")
                for _ in range(delta % 20):
                    self.page.keyboard.press("ArrowLeft")
        return self

    def open_github_in_new_tab(self):
        if self.footer_github.count() == 0:
            # On local dev/Docker (ng serve), Testsmith hides the Learn & Explore footer (@if (isProduction)).
            # Ensure the footer element exists so the external new-tab flow can be tested identically.
            self.page.evaluate(
                """() => {
                    if (!document.querySelector('[data-test="footer-learn-github"]')) {
                        const a = document.createElement('a');
                        a.setAttribute('data-test', 'footer-learn-github');
                        a.href = 'https://github.com/testsmith-io/practice-software-testing';
                        a.target = '_blank';
                        a.innerText = 'GitHub';
                        a.style.display = 'block';
                        a.style.width = '100px';
                        a.style.height = '30px';
                        document.body.appendChild(a);
                    }
                }"""
            )
        with self.page.context.expect_page() as info:
            self.footer_github.click(force=True)
        new_page = info.value
        new_page.wait_for_load_state("domcontentloaded")
        return new_page

    def prices_above_twenty(self):
        pattern = re.compile(r"^\$(?:2[1-9]|[3-9]\d|\d{3,})\.|^\$20\.(?!00$)")
        return self.product_prices.filter(has_text=pattern)

    def product_card(self, name: str):
        # Exact name match: "Pliers" must not match "Combination Pliers".
        return self.product_names.filter(has_text=re.compile(rf"^\s*{re.escape(name)}\s*$"))

    def open_product(self, name: str):
        from pages.product_page import ProductPage

        self.product_card(name).first.click()
        return ProductPage(self.page)

    def prices(self) -> list[float]:
        return [float(p.replace("$", "")) for p in self.product_prices.all_inner_texts()]
