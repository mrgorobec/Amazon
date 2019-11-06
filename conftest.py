"""
File is for test pre setup
"""
import os
from pytest import fixture
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOption
from selenium.webdriver.firefox.options import Options as FirefoxOption

HOST_PARAM_STAGING = 'https://www.staging.amazon.com/'
HOST_PARAM_PROD = 'https://www.amazon.com/'

MOBILE_EMULATION = {
    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; en-us; Nexus 5 Build/JOP40D)"
                 " AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}

CHROME_DRIVER_HARD_CODED_VERSION = '74.0.3729.6'

COMMAND_EXECUTOR = 'http://oleksandr122:uMu2ZjEampUAabMyfSEx@hub.browserstack.com:80/wd/hub'


def pytest_addoption(parser):
    """Declaring the command-line options for test run"""
    parser.addoption('--host',
                     default='staging',
                     help='host options: "staging", "production", or your own host for local testing')
    parser.addoption('--headless',
                     default='true',
                     help='headless options: "true" or "false"')
    parser.addoption('--browser',
                     default='chrome',
                     help='option to define type of browser')
    parser.addoption('--browser_type',
                     default='mobile',
                     help='option to define web or mobile browser')


@fixture(autouse=True)
def driver_type(request):
    """Return type of browser mobile or web
    :param request:
    :return:
    """
    browser_type = request.config.getoption('--browser_type')
    yield browser_type


@fixture(autouse=True)
def driver(request, driver_type):
    """Return browser
    :param driver_type:
    :param request:
    :return:
    """
    # define browser type
    browser = request.config.getoption('--browser')

    # create browser type options
    chrome_option = ChromeOption()
    firefox_option = FirefoxOption()

    # define cli headless mode
    headless = request.config.getoption('--headless')

    if browser == 'firefox':
        if headless == 'true':
            firefox_option.add_argument('--headless')
            firefox_option.add_argument('--ignore-certificate-errors')
        driver_instance = webdriver.Firefox(executable_path=GeckoDriverManager().install(),
                                            firefox_options=firefox_option)
    elif browser == 'chrome':
        if headless == 'true':
            # run headless browser
            chrome_option.add_argument('--headless')

        chrome_option.add_argument('--ignore-certificate-errors')
        chrome_option.add_argument("--window-size=1920,1080")

        if driver_type == 'mobile':
            # run mobile browser
            chrome_option.add_experimental_option('mobileEmulation', MOBILE_EMULATION)
            # version = CHROME_DRIVER_HARD_CODED_VERSION
        driver_instance = webdriver.Chrome(ChromeDriverManager().install(),
                                           chrome_options=chrome_option)

    request.addfinalizer(lambda *args: driver_instance.quit())
    yield driver_instance


@fixture(autouse=True)
def host(request):
    """Return the target host
    :param request:
    :return:
    """
    # get host value
    cli_value = request.config.getoption('--host')

    if cli_value == '' or cli_value == 'staging':
        domain = HOST_PARAM_STAGING
    elif cli_value == 'prod':
        domain = HOST_PARAM_PROD
    else:
        domain = cli_value
    yield domain


@fixture(autouse=True)
def environment(request):
    """Return the target host
    :param request:
    :return:
    """
    # get environment
    cli_value = request.config.getoption('--host')
    yield cli_value
