"""
An ability which provides an API for Selenium to enable actors to perform
actions related to web browsing. Grant your actor the ability to browse
the web like so:

    # during instantiation
    the_actor = AnActor.who_can(BrowseTheWeb.using_firefox())

    # after instantiation
    the_actor.can(BrowseTheWeb.using_safari())

    # use in new actions
    the_actor.uses_ability_to(BrowseTheWeb).to_find(target)
"""


import os
from typing import TYPE_CHECKING, Callable, List, Tuple, Union

from selenium.common.exceptions import (
    NoAlertPresentException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver import Chrome, Firefox, Remote, Safari
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..exceptions import AbilityError
from .base_ability import BaseAbility

if TYPE_CHECKING:
    from ..target import Target  # noqa: for type checking

DEFAULT_APPIUM_HUB_URL = "http://localhost:4723/wd/hub"
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


class BrowsingError(AbilityError):
    """Raised when BrowseTheWeb encounters an error."""


class BrowseTheWeb(BaseAbility):
    """
    The ability to browse the web with a web browser. This ability is
    meant to be instantiated with its |BrowseTheWeb.using| static method,
    which takes in the WebDriver to use, or one of its other "using"
    methods. A typical invocation looks like:

        BrowseTheWeb.using(selenium.webdriver.Firefox())

        BrowseTheWeb.using_firefox()

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
        hub_url = os.getenv("APPIUM_HUB_URL", DEFAULT_APPIUM_HUB_URL)
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
        hub_url = os.getenv("APPIUM_HUB_URL", DEFAULT_APPIUM_HUB_URL)
        return BrowseTheWeb.using(Remote(hub_url, DEFAULT_ANDROID_CAPABILITIES))

    @staticmethod
    def using(browser: WebDriver) -> "BrowseTheWeb":
        """
        Specifies the driver to use to browse the web. This can be any
        |WebDriver| instance, even a remote one.

        Args:
            browser: the webdriver instance to use.

        Returns:
            |BrowseTheWeb|
        """
        return BrowseTheWeb(browser)

    def to_find(self, target: Union["Target", Tuple[By, str]]) -> WebElement:
        """
        Locates a single element on the page using the given locator.

        Args:
            target: the |Target| or tuple describing the element.

        Returns:
            |WebElement|

        Raises:
            |BrowsingError|:
        """
        locator = self._resolve_locator(target)

        try:
            return self.browser.find_element(*locator)
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to find "
                f"{target}: {e.__class__.__name__}"
            )
            raise BrowsingError(msg).with_traceback(e.__traceback__)

    def find(self, locator: Union["Target", Tuple[By, str]]) -> WebElement:
        """Syntactic sugar for |BrowseTheWeb.to_find|."""
        return self.to_find(locator)

    def to_find_all(self, target: Union["Target", Tuple[By, str]]) -> List[WebElement]:
        """
        Locates many elements on the page using the given locator.

        Args:
            target: the |Target| or tuple describing the elements.

        Returns:
            List[|WebElement|]
        """
        locator = self._resolve_locator(target)

        try:
            return self.browser.find_elements(*locator)
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to find all "
                f"{target}: {e.__class__.__name__}"
            )
            raise BrowsingError(msg).with_traceback(e.__traceback__)

    def find_all(self, target: Union["Target", Tuple[By, str]]) -> WebElement:
        """Syntactic sugar for |BrowseTheWeb.to_find_all|."""
        return self.find_all(target)

    def to_switch_to_alert(self) -> Alert:
        """
        Switches to an alert and returns it.

        Returns:
            |Alert|

        Raises:
            |BrowsingError|: no alert was present to switch to.
        """
        try:
            return self.browser.switch_to.alert
        except NoAlertPresentException as e:
            raise BrowsingError("No alert was present to switch to.").with_traceback(
                e.__traceback__
            )

    def to_switch_to(self, target: "Target") -> None:
        """
        Switches the browser context to the target.

        Args:
            target: the |Target|  or tuple describing the element to
                switch to.
        """
        element = self.find(target)
        self.browser.switch_to.frame(element)

    def to_switch_to_default(self) -> None:
        """Switches the browser context back to the default frame."""
        self.browser.switch_to.default_content()

    def to_wait_for(
        self,
        target: Union["Target", Tuple[By, str]],
        timeout: int = 20,
        cond: Callable = EC.visibility_of_element_located,
    ):
        """
        Waits for the element to fulfill the given condition.

        Args:
            target: the tuple or |Target| describing the element.
            timeout: how many seconds to wait before raising a
                TimeoutException. Default is 20.
            cond: the condition to wait for. Default is
                visibility_of_element_located.

        Raises:
            |BrowsingError|: the target did not satisfy the condition in time.
        """
        locator = self._resolve_locator(target)

        try:
            WebDriverWait(self.browser, timeout).until(cond(locator))
        except TimeoutException as e:
            msg = "Waiting {time} seconds for {element} to satisfy {cond} timed out."
            msg = msg.format(time=timeout, element=target, cond=cond.__name__)
            raise BrowsingError(msg).with_traceback(e.__traceback__)

    def wait_for(
        self,
        locator: Union["Target", Tuple[By, str]],
        timeout: int = 20,
        cond: Callable = EC.visibility_of_element_located,
    ):
        """Syntactic sugar for |BrowseTheWeb.to_wait_for|."""
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
            url: the URL to visit.

        Returns:
            |BrowseTheWeb|
        """
        self.browser.get(f'{os.getenv("BASE_URL", "")}{url}')
        return self

    def to_visit(self, url: str) -> "BrowseTheWeb":
        """Syntactic sugar for |BrowseTheWeb.to_get|."""
        return self.to_get(url)

    def forget(self) -> None:
        """
        Asks the actor to forget how to BrowseTheWeb. This quits the
        connected browser.

        An actor who is exiting will forget all their abilities.
        """
        self.browser.quit()

    def _resolve_locator(
        self, target_or_locator: Union["Target", Tuple[By, str]]
    ) -> Tuple[By, str]:
        """
        Given a |Target| or a tuple, ensures we get a tuple back.

        Args:
            target_or_locator: the |Target| or locator to resolve.

        Returns:
            Tuple[By, str]
        """
        if not isinstance(target_or_locator, tuple):
            locator = target_or_locator.get_locator()
        else:
            locator = target_or_locator
        return locator

    def __repr__(self) -> str:
        return "Browse the Web"

    def __init__(self, browser: "WebDriver") -> None:
        self.browser = browser
