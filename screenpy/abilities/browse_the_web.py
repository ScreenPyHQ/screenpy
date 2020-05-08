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

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver import Chrome, Firefox, Remote, Safari
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..exceptions import BrowsingError
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
        Create and use a default Chrome Selenium webdriver instance. Use
        this if you don't need to set anything up for your test browser.

        Returns:
            |BrowseTheWeb|
        """
        return BrowseTheWeb.using(Chrome())

    @staticmethod
    def using_firefox() -> "BrowseTheWeb":
        """
        Create and use a default Firefox Selenium webdriver instance. Use
        this if you don't need to set anything up for your test browser.

        Returns:
            |BrowseTheWeb|
        """
        return BrowseTheWeb.using(Firefox())

    @staticmethod
    def using_safari() -> "BrowseTheWeb":
        """
        Create and use a default Safari Selenium webdriver instance. Use
        this if you don't need to set anything up for your test browser.

        Returns:
            |BrowseTheWeb|
        """
        return BrowseTheWeb.using(Safari())

    @staticmethod
    def using_ios() -> "BrowseTheWeb":
        """
        Create and use a default Remote driver instance to connect to a
        running Appium server and open Safari on iOS. Use this if you don't
        need to set anything up for your test browser.

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
        Create and use a default Remote driver instance to connect to a
        running Appium server and open Chrome on Android. Use this if you
        don't need to set anything up for your test browser.

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
        Specify the driver to use to browse the web. This can be any
        |WebDriver| instance, even a remote one.

        Args:
            browser: the webdriver instance to use.

        Returns:
            |BrowseTheWeb|
        """
        return BrowseTheWeb(browser)

    def to_find(self, target: Union["Target", Tuple[By, str]]) -> WebElement:
        """
        Locate a single element on the page using the given target or locator.

        Args:
            target: the |Target| or locator tuple describing the element.

        Returns:
            |WebElement|

        Raises:
            |BrowsingError|: unable to find the described element.
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

    find = to_find

    def to_find_all(self, target: Union["Target", Tuple[By, str]]) -> List[WebElement]:
        """
        Locate many elements on the page using the given target or locator.

        Args:
            target: the |Target| or locator tuple describing the elements.

        Returns:
            List[|WebElement|]

        Raises:
            |BrowsingError|: unable to find the described elements.
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

    find_all = to_find_all

    def to_wait_for(
        self,
        target: Union["Target", Tuple[By, str]],
        timeout: int = 20,
        cond: Callable = EC.visibility_of_element_located,
    ) -> None:
        """
        Wait for the element to fulfill the given condition.

        Args:
            target: the |Target| or locator tuple describing the element.
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

    wait_for = to_wait_for

    def forget(self) -> None:
        """Quit the attached browser."""
        self.browser.quit()

    def _resolve_locator(
        self, target_or_locator: Union["Target", Tuple[By, str]]
    ) -> Tuple[By, str]:
        """
        Given a |Target| or a tuple, ensure we get a tuple back.

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
