import os

from selenium.webdriver.common.by import By


class AmazonHome(object):
    """Amazon home page"""

    input_field = (
        By.XPATH,
        '''//*[@id="twotabsearchtextbox"]'''
    )

    search_input_button = (
        By.XPATH,
        '''//input[@type="submit" and @class="nav-input"]'''
    )


class AmazonSearchResults(object):
    """Amazon search result page"""

    result_list = (
        By.XPATH,
        '''//*[@class="s-result-list s-search-results sg-row"]
        //*[@class="a-section aok-relative s-image-fixed-height"]'''
        # '''//*[@class="s-result-list s-search-results sg-row"]/div'''
    )

    prices_list = (
        By.XPATH,
        '''//*[@class="s-result-list s-search-results sg-row"]//*[@class="a-price-whole"]'''
    )

    name_list = (
        By.XPATH,
        '''//*[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"]/a'''
    )


class AmazonProductPage(object):
    """Product Page"""

    product_tittle = (
        By.ID,
        '''productTitle'''
    )
    product_price = (
        By.ID,
        '''priceblock_ourprice'''
    )
