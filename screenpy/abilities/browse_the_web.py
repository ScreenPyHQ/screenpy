from typing import List

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BrowseTheWeb(object):
    """
    The ability to browse the web with a web browser. This ability is
    meant to be instantiated with its |BrowseTheWeb.using| static method,
    which takes in the WebDriver to use. A typical invocation looks like:

        BrowseTheWeb.using(selenium.webdriver.Firefox())

    This will create the ability that can be passed in to an actor's
    |Actor.who_can| method.
    """

    @staticmethod
    def using(browser: "WebDriver") -> "BrowseTheWeb":
        """
        Specifies the driver to use to browse the web. This can be any
        |WebDriver| instance, even a remote one, or an entirely different
        driver that has a similar API.

        Args:
            browser (webdriver): The driver to use.

        Returns:
            |BrowseTheWeb|
        """
        return BrowseTheWeb(browser)

    def find(self, locator: tuple) -> "WebElement":
        """
        Locates a single element on the page using the given locator.

        Args:
            locator (tuple): The tuple describing the element, like
                (|By|, string)

        Returns:
            |WebElement|
        """
        return self.browser.find_element(*locator)

    def find_all(self, locator: tuple) -> List["WebElement"]:
        """
        Locates many elements on the page using the given locator.

        Args:
            locator (tuple): The tuple describing the elements, like
                (|By|, string)

        Returns:
            list(|WebElement|)
        """
        return self.browser.find_elements(*locator)

    def wait_then_find(
        self, locator: tuple, timeout=20, cond=EC.visibility_of_element_located
    ) -> "WebElement":
        """
        Waits for the element described by the locator to appear, then
        gets it.

        Args:
            locator (tuple): The tuple describing the element, like
                (|By|, string)
            timeout (int): How many seconds to wait before raising a
                TimeoutException. Default is 20.
            cond (ExpectedCondition): The condition to wait for. Default
                is visibility_of_element_located.

        Returns:
            |WebElement|
        """
        self.wait_for(locator, timeout, cond)
        return self.find(locator)

    def wait_then_find_all(
        self, locator: tuple, timeout=20, cond=EC.visibility_of_element_located
    ) -> List["WebElement"]:
        """
        Waits for the elements described by the locator to appear, then
        gets them all.

        Args:
            locator (tuple): The tuple describing the element, like
                (|By|, string)
            timeout (int): How many seconds to wait before raising a
                TimeoutException. Default is 20.
            cond (ExpectedCondition): The condition to wait for. Default
                is visibility_of_element_located.

        Returns:
            list(|WebElement|)
        """
        self.wait_for(locator, timeout, cond)
        return self.find_all(locator)

    def wait_for(self, locator, timeout=20, cond=EC.visibility_of_element_located):
        """
        Waits for the element specified by locator to fulfill the given
        condition.

        Args:
            locator (tuple or Target): The tuple or |Target| describing
            the element.
            timeout (int): How many seconds to wait before raising a
                TimeoutException. Default is 20.
            cond (ExpectedCondition): The condition to wait for. Default
                is visibility_of_element_located.

        Raises:
            TimeoutException: if the element did not satisfy the condition
                in a timely manner.
        """
        if not isinstance(locator, tuple):
            locator = locator.get_locator()
        try:
            WebDriverWait(self.browser, timeout).until(cond(locator))
        except TimeoutException:
            msg = "Waiting {0} seconds for '{1}' to satisfy {2} timed out."
            msg = msg.format(timeout, locator, cond.__name__)
            raise TimeoutException(msg)

    def to_wait_for(self, locator, timeout=20, cond=EC.visibility_of_element_located):
        """Syntactic sugar for |BrowseTheWeb.wait_for|"""
        return self.wait_for(locator, timeout, cond)

    def to_get(self, url: str) -> "BrowseTheWeb":
        """
        Uses the connected browser to visit the specified URL.

        Args:
            url (string): the URL to visit.

        Returns:
            |BrowseTheWeb|
        """
        self.browser.get(url)
        return self

    def forget(self):
        """
        What happens when the actor forgets this ability: it quits the
        connected browser.
        """
        self.browser.quit()

    def __repr__(self):
        return "Browse the Web"

    def __init__(self, browser: "WebDriver") -> None:
        self.browser = browser
