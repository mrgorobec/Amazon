import datetime
import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasicPage(object):
    implicit_wait_s = 10  # seconds

    def __init__(self, driver, url, timeout=10):
        """
        :param driver: instance driver
        :param url: host where test will be running
        :param timeout: if need some timeout for action execution
        """
        """BasicPage class contains webpage elements descriptions and the methods to interact with them"""
        self.driver = driver
        self.timeout = timeout
        self.driver.implicitly_wait(self.implicit_wait_s)
        self.driver.get(url)
        """
        Text or notifications which could be on different pages
        """
        self.search_by_area_header_text_result = u'Wedding Venues in the search area'
        self.no_venue_header_text_result = u'No venues found for'

    def quit(self):
        self.driver.quit()

    def wait_and_find_elem(self, locator, timeout=5):
        """Find element with specified locator
        :param timeout:
        :param locator: tuple (method, value, name)
        :return: selenium.webdriver.remote.webelement.WebElement
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator))
            return element
        except NoSuchElementException:
            self.driver.save_screenshot('screenshot-{}.png'.format(datetime.datetime.now().isoformat()))
            raise NoSuchElementException

    def wait_and_find_elems(self, locator):
        """Find elements with specified locator

        :param locator: tuple (method, value, name)
        :return: list of selenium.webdriver.remote.webelement.WebElement
        """
        try:
            elements = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_all_elements_located(locator))
            return elements
        except NoSuchElementException as e:
            raise e

    def open_url(self, url):
        """Open needed url

        :param url:
        """
        self.driver.get(url)

    def type(self, locator, expression):
        """Fill element with provided chars

        :param locator: tuple (method, value, name)
        :param expression: str - expression to type
        """
        field = self.wait_and_find_elem(locator)
        field.send_keys(expression)

    def click(self, locator, wait_element_is_present=None):
        """Find an element by the specified locator and click it
        :param wait_element_is_present:
        :param waiting: time to wait
        :param locator: tuple (method, value, name)
        """
        waiting = 5
        try:
            if wait_element_is_present is None:
                element_present = EC.element_to_be_clickable(locator)
            else:
                element_present = \
                    EC.invisibility_of_element_located((wait_element_is_present[0], wait_element_is_present[1]))
            WebDriverWait(self.driver, waiting).until(element_present)
            self.wait_and_find_elem(locator, waiting).click()
        except:
            self.wait_and_find_elem(locator, waiting).click()

    def highlight_elem(self, locator):
        """Give red frame for element with specified locator
        :param locator: tuple (method, value, name)
        """
        elem = self.wait_and_find_elem(locator)
        original_style = elem.get_attribute('style')

        def apply_style(style):
            self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                       elem, style)

        apply_style('background: yellow; border: 2px solid red;')
        time.sleep(0.5)
        apply_style(original_style)

    def get_text(self, locator):
        """Get text of web element with specified locator

        :param locator: tuple (method, value, name)
        :return: str - element text
        """
        elem = self.wait_and_find_elem(locator)
        return elem.text
