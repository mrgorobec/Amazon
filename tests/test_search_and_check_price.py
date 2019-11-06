import pytest

from pages.amazon import AmazonHome, AmazonSearchResults, AmazonProductPage
from pages.basic_page import BasicPage


@pytest.mark.web
@pytest.mark.prod
@pytest.mark.parametrize('input_text', ["Playstation 4 pro", "airpods", "hdmi"])
def test_search_and_check_price(driver, host, input_text):
    """Search for on a Amazon"""
    driver = BasicPage(driver, host)
    driver.type(AmazonHome.input_field, input_text)
    driver.click(AmazonHome.search_input_button)
    """Let's take first element price and click on it to check if will the same price will shown for a user"""
    first_element_price = driver.get_text(AmazonSearchResults.prices_list)
    first_element_name = driver.get_text(AmazonSearchResults.name_list)

    """Open first search item"""
    driver.wait_and_find_elems(AmazonSearchResults.result_list)[0].click()

    """Assert price and item name from search page and product page"""
    assert driver.get_text(AmazonProductPage.product_tittle) == first_element_name
    assert first_element_price in driver.get_text(AmazonProductPage.product_price)
