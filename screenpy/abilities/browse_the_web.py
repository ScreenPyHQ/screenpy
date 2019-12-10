import os
from typing import List

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome, Firefox, Remote, Safari
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


DEFAULT_IOS_CAPABILITIES = {
    "platformName": "iOS",
    "platformVersion": os.getenv("IOS_DEVICE_VERSION", "13.1"),
    "deviceName": os.getenv("IOS_DEVICE_NAME", "iPhone Simulator"),
    "automationName": "xcuitest",
    "browserName": "Safari",
}
DEFAULT_ANDROID_CAPABILITIES = {
    "platformName": "Android",
    "platformVersion": os.getenv("ANDROID_DEVICE_VERSION", "10.0"),
    "deviceName": os.getenv("ANDROID_DEVICE_NAME", "Android Emulator"),
    "automationName": "UIAutomator2",
    "browserName": "Chrome",
}


class BrowseTheWeb:
    """
    The ability to browse the web with a web browser. This ability is
    meant to be instantiated with its |BrowseTheWeb.using| static method,
    which takes in the WebDriver to use. A typical invocation looks like:

        BrowseTheWeb.using(selenium.webdriver.Firefox())

    This will create the ability that can be passed in to an actor's
    |Actor.who_can| method.
    """

    @staticmethod
    def using_chrome() -> "BrowseTheWeb":
        """
        Creates and uses a default Chrome Selenium webdriver instance. Use
        this if you don't need to set anything up for your test browser.

        Returns:
            |BrowseTheWeb|
        """
        return BrowseTheWeb.using(Chrome())

    @staticmethod
    def using_firefox() -> "BrowseTheWeb":
        """
        Creates and uses a default Firefox Selenium webdriver instance. Use
        this if you don't need to set anything up for your test browser.

        Returns:
            |BrowseTheWeb|
        """
        return BrowseTheWeb.using(Firefox())

    @staticmethod
    def using_safari() -> "BrowseTheWeb":
        """
        Creates and uses a default Safari Selenium webdriver instance. Use
        this if you don't need to set anything up for your test browser.

        Returns:
            |BrowseTheWeb|
        """
        return BrowseTheWeb.using(Safari())

    @staticmethod
    def using_ios() -> "BrowseTheWeb":
        """
        Creates an uses a default Remote driver instance to connect to
        a running Appium server and open Safari on iOS. Use this if you
        don't need to set anything up for your test browser.

        Note that Appium requires non-trivial setup to be able to connect
        to iPhone simulators. See the Appium documentation to get started:
        http://appium.io/docs/en/writing-running-appium/running-tests/

        Environment Variables:
            APPIUM_HUB_URL: the URL to look for the Appium server. Default
                is "http://localhost:4723/wd/hub"
            IOS_DEVICE_VERSION: the version of the device to put in the
                desired capabilities. Default is "13.1"
            IOS_DEVICE_NAME: the device name to request in the desired
                capabilities. Default is "iPhone Simulator"

        Returns:
            |BrowseTheWeb|
        """
        hub_url = os.getenv("APPIUM_HUB_URL", "http://localhost:4723/wd/hub")
        return BrowseTheWeb.using(Remote(hub_url, DEFAULT_IOS_CAPABILITIES))

    @staticmethod
    def using_android() -> "BrowseTheWeb":
        """
        Creates an uses a default Remote driver instance to connect to
        a running Appium server and open Chrome on Android. Use this if
        you don't need to set anything up for your test browser.

        Note that Appium requires non-trivial setup to be able to connect
        to Android emulators. See the Appium documentation to get started:
        http://appium.io/docs/en/writing-running-appium/running-tests/

        Environment Variables:
            APPIUM_HUB_URL: the URL to look for the Appium server. Default
                is "http://localhost:4723/wd/hub"
            ANDROID_DEVICE_VERSION: the version of the device to put in
                the desired capabilities. Default is "10.0"
            ANDROID_DEVICE_NAME: the device name to request in the desired
                capabilities. Default is "Android Emulator"

        Returns:
            |BrowseTheWeb|
        """
        hub_url = os.getenv("APPIUM_HUB_URL", "http://localhost:4723/wd/hub")
        return BrowseTheWeb.using(Remote(hub_url, DEFAULT_ANDROID_CAPABILITIES))

    @staticmethod
    def using(browser: WebDriver) -> "BrowseTheWeb":
        """
        Specifies the driver to use to browse the web. This can be any
        |WebDriver| instance, even a remote one.

        Args:
            browser (webdriver): The driver to use.

        Returns:
            |BrowseTheWeb|
        """
        return BrowseTheWeb(browser)

    def find(self, locator: tuple) -> WebElement:
        """
        Locates a single element on the page using the given locator.

        Args:
            locator (tuple): The tuple describing the element, like
                (|By|, string)

        Returns:
            |WebElement|
        """
        return self.browser.find_element(*locator)

    def to_find(self, locator: tuple) -> WebElement:
        """Syntactic sugar for |BrowseTheWeb.find|."""
        return self.find(locator)

    def find_all(self, locator: tuple) -> List[WebElement]:
        """
        Locates many elements on the page using the given locator.

        Args:
            locator (tuple): The tuple describing the elements, like
                (|By|, string)

        Returns:
            list(|WebElement|)
        """
        return self.browser.find_elements(*locator)

    def to_find_all(self, locator: tuple) -> WebElement:
        """Syntactic sugar for |BrowseTheWeb.find_all|."""
        return self.find_all(locator)

    def wait_then_find(
        self, locator: tuple, timeout=20, cond=EC.visibility_of_element_located
    ) -> WebElement:
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
    ) -> List[WebElement]:
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
            msg = "Waiting {time} seconds for '{ele}' to satisfy {cond} timed out."
            msg = msg.format(time=timeout, ele=locator, cond=cond.__name__)
            raise TimeoutException(msg)

    def to_wait_for(self, locator, timeout=20, cond=EC.visibility_of_element_located):
        """Syntactic sugar for |BrowseTheWeb.wait_for|."""
        return self.wait_for(locator, timeout, cond)

    def to_get(self, url: str) -> "BrowseTheWeb":
        """
        Uses the connected browser to visit the specified URL.

        This action supports using the BASE_URL environment variable to
        set a base URL. If you set BASE_URL, the url passed in to this
        function will be appended to the end of it. For example, if you
        have `BASE_URL=http://localhost`, then to_get("/home") will send
        your browser to "http://localhost/home".

        If BASE_URL isn't set, then the passed-in url is assumed to be a
        fully qualified URL.

        Args:
            url (string): the URL to visit.

        Returns:
            |BrowseTheWeb|
        """
        self.browser.get(f'{os.getenv("BASE_URL", "")}{url}')
        return self

    def to_visit(self, url: str) -> "BrowseTheWeb":
        """Syntactic sugar for |BrowseTheWeb.to_get|."""
        return self.to_get(url)

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
