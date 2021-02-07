from unittest import mock

import pytest
from selenium.common.exceptions import TimeoutException, WebDriverException

from screenpy import Target
from screenpy.abilities import AuthenticateWith2FA, BrowseTheWeb, MakeAPIRequests
from screenpy.abilities.browse_the_web import (
    DEFAULT_ANDROID_CAPABILITIES,
    DEFAULT_APPIUM_HUB_URL,
    DEFAULT_IOS_CAPABILITIES,
)
from screenpy.exceptions import BrowsingError, RequestError


class TestBrowseTheWeb:
    def test_can_be_instantiated(self):
        b = BrowseTheWeb.using(None)

        assert isinstance(b, BrowseTheWeb)

    @mock.patch("screenpy.abilities.browse_the_web.Firefox")
    def test_using_firefox(self, mocked_firefox):
        """Creates new Firefox driver instance"""
        BrowseTheWeb.using_firefox()

        mocked_firefox.assert_called_once()

    @mock.patch("screenpy.abilities.browse_the_web.Chrome")
    def test_using_chrome(self, mocked_chrome):
        """Creates new Chrome driver instance"""
        BrowseTheWeb.using_chrome()

        mocked_chrome.assert_called_once()

    @mock.patch("screenpy.abilities.browse_the_web.Safari")
    def test_using_safari(self, mocked_safari):
        """Creates new Safari driver instance"""
        BrowseTheWeb.using_safari()

        mocked_safari.assert_called_once()

    @mock.patch("screenpy.abilities.browse_the_web.Remote")
    def test_using_ios(self, mocked_remote):
        """Creates new IOS remote driver instance"""
        BrowseTheWeb.using_ios()

        mocked_remote.assert_called_once_with(
            DEFAULT_APPIUM_HUB_URL, DEFAULT_IOS_CAPABILITIES
        )

    @mock.patch("screenpy.abilities.browse_the_web.Remote")
    def test_using_android(self, mocked_android):
        """Creates new Android remote driver instance"""
        BrowseTheWeb.using_android()

        mocked_android.assert_called_once_with(
            DEFAULT_APPIUM_HUB_URL, DEFAULT_ANDROID_CAPABILITIES
        )

    @mock.patch("screenpy.abilities.browse_the_web.Firefox")
    def test_to_find(self, mocked_ff):
        """Find is called with the locator tuple."""
        btw = BrowseTheWeb.using_firefox()
        test_locator = (1, 2)
        test_target = Target.the("test").located_by(test_locator)

        btw.to_find(test_target)

        btw.browser.find_element.assert_called_once_with(*test_locator)

    @mock.patch("screenpy.abilities.browse_the_web.Firefox")
    def test_to_find_exception(self, mocked_ff):
        """Find throws a browsing error if something goes wrong."""
        btw = BrowseTheWeb.using_firefox()
        btw.browser.find_element.side_effect = WebDriverException("test")

        with pytest.raises(BrowsingError):
            btw.to_find(Target.the("test").located_by((1, 2)))

    @mock.patch("screenpy.abilities.browse_the_web.Firefox")
    def test_to_find_all(self, mocked_ff):
        """Find all is called with the locator tuple."""
        btw = BrowseTheWeb.using_firefox()
        test_locator = (1, 2)
        test_target = Target.the("test").located_by(test_locator)

        btw.to_find_all(test_target)

        btw.browser.find_elements.assert_called_once_with(*test_locator)

    @mock.patch("screenpy.abilities.browse_the_web.Firefox")
    def test_to_find_all_exception(self, mocked_ff):
        """Find all throws a browsing error if something goes wrong."""
        btw = BrowseTheWeb.using_firefox()
        btw.browser.find_elements.side_effect = WebDriverException("test")

        with pytest.raises(BrowsingError):
            btw.to_find_all(Target.the("test").located_by((1, 2)))

    @mock.patch("screenpy.abilities.browse_the_web.WebDriverWait")
    @mock.patch("screenpy.abilities.browse_the_web.Firefox")
    def test_to_wait_for(self, mocked_ff, mocked_wdw):
        """Wait for returns what WebDriverWait returns."""
        btw = BrowseTheWeb.using_firefox()
        test_value = "foo"
        mocked_wdw.return_value.until.return_value = test_value

        actual_value = btw.to_wait_for((None, None))

        assert actual_value == test_value

    @mock.patch("screenpy.abilities.browse_the_web.WebDriverWait")
    @mock.patch("screenpy.abilities.browse_the_web.Firefox")
    def test_to_wait_for_exception(self, mocked_ff, mocked_wdw):
        """Wait for throws a browsing error if something goes wrong."""
        btw = BrowseTheWeb.using_firefox()
        mocked_wdw.return_value.until.side_effect = TimeoutException("test")

        with pytest.raises(BrowsingError):
            btw.to_wait_for(Target.the("test").located_by((1, 2)))


class TestAuthenticateWith2FA:
    def test_can_be_instantiated(self):
        a1 = AuthenticateWith2FA.using_secret("")
        a2 = AuthenticateWith2FA.using(None)

        assert isinstance(a1, AuthenticateWith2FA)
        assert isinstance(a2, AuthenticateWith2FA)

    @mock.patch("screenpy.abilities.authenticate_with_2fa.pyotp")
    def test_using_secret(self, mocked_pyotp):
        """Creates a new pyotp.TOTP instance"""
        secret = "THISISJUSTATESTTOKENITSNOTAREAL1"
        AuthenticateWith2FA.using_secret(secret)

        mocked_pyotp.TOTP.assert_called_once_with(secret)


class TestMakeAPIRequests:
    def test_can_be_instantiated(self):
        mar1 = MakeAPIRequests()
        mar2 = MakeAPIRequests.using(None)

        assert isinstance(mar1, MakeAPIRequests)
        assert isinstance(mar2, MakeAPIRequests)

    def test_unexpected_http_method(self):
        """Unexpected HTTP method causes an exception"""
        mar = MakeAPIRequests()

        with pytest.raises(RequestError):
            mar.send("TEST_METHOD", "url")

    @pytest.mark.parametrize(
        "method", ["delete", "get", "head", "options", "patch", "post", "put"]
    )
    @mock.patch("screenpy.abilities.make_api_requests.Session")
    def test_http_method_calls_correct_session_method(self, mocked_session, method):
        mar = MakeAPIRequests()

        mar.send(method, "url")

        getattr(mar.session, method).assert_called_once()
