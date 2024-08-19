from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from psplpy.network_utils import *


def cookies_split(cookie_str: str) -> dict:
    cookies = {}
    for cookie_pair in cookie_str.split(';'):
        key, value = cookie_pair.split('=', maxsplit=1)
        cookies[key.strip()] = value.strip()
    return cookies


def set_cookies(driver: WebDriver, cookies: dict, kwargs: dict = None) -> None:
    driver.delete_all_cookies()
    for cookie in cookies:
        driver.add_cookie({'name': cookie, 'value': cookies[cookie], **(kwargs or {})})


def find(driver: WebDriver | WebElement, tag: str = '*', attr: str = '', value: str = '') -> WebElement:
    return driver.find_element(By.XPATH, f"//{tag}[@*[contains(name(), '{attr}') and contains(., '{value}')]]")


def finds(driver: WebDriver | WebElement, tag: str = '*', attr: str = '', value: str = '') -> list[WebElement]:
    return driver.find_elements(By.XPATH, f"//{tag}[@*[contains(name(), '{attr}') and contains(., '{value}')]]")


def find_unique(driver: WebDriver | WebElement, tag: str = '*', attr: str = '', value: str = '') -> WebElement:
    elements = finds(driver, tag, attr, value)
    if len(elements) > 1:
        raise ValueError(f"Element has {len(elements)}, more than one")
    return elements[0]


def scroll(driver: WebDriver):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')


class SeleniumTestServer:
    def __init__(self, show_seperator: bool = True):
        self.show_seperator = show_seperator

    def _handler(self, client_socket: ClientSocket, addr):
        code = client_socket.recv_pickle()
        try:
            exec(code)
        finally:
            if self.show_seperator:
                time.sleep(0.01)
                print('=' * 100)
