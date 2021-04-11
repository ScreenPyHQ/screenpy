"""
Enable the actor to browse the web.
"""

import os

from selenium.webdriver import Chrome, Firefox, Remote, Safari
from selenium.webdriver.remote.webdriver import WebDriver

from ..exceptions import BrowsingError

DEFAULT_APPIUM_HUB_URL = "http://localhost:4723/wd/hub"


class BrowseTheWeb:
    """Use Selenium to enable browsing the web with a web browser.

    Examples::

        Perry = AnActor.named("Perry").who_can(
            BrowseTheWeb.using_firefox()
        )

        Perry = AnActor.named("Perry").who_can(
            BrowseTheWeb.using(driver)
        )
    """

    @staticmethod
    def using_chrome() -> "BrowseTheWeb":
        """Create and use a default Chrome Selenium webdriver instance."""
        return BrowseTheWeb.using(Chrome())

    @staticmethod
    def using_firefox() -> "BrowseTheWeb":
        """Create and use a default Firefox Selenium webdriver instance."""
        return BrowseTheWeb.using(Firefox())

    @staticmethod
    def using_safari() -> "BrowseTheWeb":
        """Create and use a default Safari Selenium webdriver instance."""
        return BrowseTheWeb.using(Safari())

    @staticmethod
    def using_ios() -> "BrowseTheWeb":
        """
        Create and use a default Remote driver instance to connect to a
        running Appium server and open Safari on iOS.

        Note that Appium requires non-trivial setup to be able to connect
        to iPhone simulators. See the Appium documentation to get started:
        http://appium.io/docs/en/writing-running-appium/running-tests/

        Environment Variables:
            APPIUM_HUB_URL: the URL to look for the Appium server. Default
                is "http://localhost:4723/wd/hub"
            IOS_DEVICE_VERSION: the version of the device to put in the
                desired capabilities. This must be set.
            IOS_DEVICE_NAME: the device name to request in the desired
                capabilities. Default is "iPhone Simulator"
        """
        hub_url = os.getenv("APPIUM_HUB_URL", DEFAULT_APPIUM_HUB_URL)
        IOS_CAPABILITIES = {
            "platformName": "iOS",
            "platformVersion": os.getenv("IOS_DEVICE_VERSION"),
            "deviceName": os.getenv("IOS_DEVICE_NAME", "iPhone Simulator"),
            "automationName": "xcuitest",
            "browserName": "Safari",
        }
        if IOS_CAPABILITIES["platformVersion"] is None:
            raise BrowsingError("IOS_DEVICE_VERSION Environment variable must be set.")

        return BrowseTheWeb.using(Remote(hub_url, IOS_CAPABILITIES))

    @staticmethod
    def using_android() -> "BrowseTheWeb":
        """
        Create and use a default Remote driver instance to connect to a
        running Appium server and open Chrome on Android.

        Note that Appium requires non-trivial setup to be able to connect
        to Android emulators. See the Appium documentation to get started:
        http://appium.io/docs/en/writing-running-appium/running-tests/

        Environment Variables:
            APPIUM_HUB_URL: the URL to look for the Appium server. Default
                is "http://localhost:4723/wd/hub"
            ANDROID_DEVICE_VERSION: the version of the device to put in
                the desired capabilities. This must be set.
            ANDROID_DEVICE_NAME: the device name to request in the desired
                capabilities. Default is "Android Emulator"
        """
        hub_url = os.getenv("APPIUM_HUB_URL", DEFAULT_APPIUM_HUB_URL)
        ANDROID_CAPABILITIES = {
            "platformName": "Android",
            "platformVersion": os.getenv("ANDROID_DEVICE_VERSION"),
            "deviceName": os.getenv("ANDROID_DEVICE_NAME", "Android Emulator"),
            "automationName": "UIAutomator2",
            "browserName": "Chrome",
        }
        if ANDROID_CAPABILITIES["platformVersion"] is None:
            raise BrowsingError(
                "ANDROID_DEVICE_VERSION environment variable must be set."
            )

        return BrowseTheWeb.using(Remote(hub_url, ANDROID_CAPABILITIES))

    @staticmethod
    def using(browser: WebDriver) -> "BrowseTheWeb":
        """Provide an already-set-up |WebDriver| to use to browse the web."""
        return BrowseTheWeb(browser)

    def forget(self) -> None:
        """Quit the attached browser."""
        self.browser.quit()

    def __repr__(self) -> str:
        return "Browse the Web"

    __str__ = __repr__

    def __init__(self, browser: "WebDriver") -> None:
        self.browser = browser
