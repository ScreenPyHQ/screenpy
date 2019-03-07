from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BrowseTheWeb(object):
    """
    The ability to browse the web with a web browser.
    """

    def find(self, locator):
        return self.browser.find_element(*locator)

    def find_all(self, locator):
        return self.browser.find_elements(*locator)

    def wait_then_find(
        self, locator, timeout=20, cond=EC.visibility_of_element_located
    ):
        self.wait_for(locator, timeout, cond)
        return self.find(locator)

    def wait_then_find_all(
        self, locator, timeout=20, cond=EC.visibility_of_element_located
    ):
        self.wait_for(locator, timeout, cond)
        return self.find_all(locator)

    def to_wait_for(self, locator, timeout=20, cond=EC.visibility_of_element_located):
        return self.wait_for(locator, timeout, cond)

    def wait_for(self, locator, timeout=20, cond=EC.visibility_of_element_located):
        if not isinstance(locator, tuple):
            locator = locator.get_locator()
        try:
            WebDriverWait(self.browser, timeout).until(cond(locator))
        except TimeoutException:
            msg = "Waiting {0} seconds for '{1}' to satisfy {2} timed out."
            msg = msg.format(timeout, locator, cond.__name__)
            raise TimeoutException(msg)

    def to_get(self, url):
        self.browser.get(url)
        return self

    def forget(self):
        self.browser.quit()

    @staticmethod
    def using(browser):
        return BrowseTheWeb(browser)

    def __init__(self, browser):
        self.browser = browser
