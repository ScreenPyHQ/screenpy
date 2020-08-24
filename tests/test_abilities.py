from unittest import mock

import pytest

from screenpy.abilities import AuthenticateWith2FA, BrowseTheWeb, MakeAPIRequests
from screenpy.abilities.browse_the_web import (
    DEFAULT_ANDROID_CAPABILITIES,
    DEFAULT_APPIUM_HUB_URL,
    DEFAULT_IOS_CAPABILITIES,
)
from screenpy.exceptions import RequestError


class TestBrowseTheWeb:
    def test_can_be_instantiated(self):
        """Can be instantiated"""
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


class TestAuthenticateWith2FA:
    def test_can_be_instantiated(self):
        """Can be instantiated"""
        a1 = AuthenticateWith2FA.using_secret("")
        a2 = AuthenticateWith2FA.using(None)

        assert isinstance(a1, AuthenticateWith2FA)
        assert isinstance(a2, AuthenticateWith2FA)

    @mock.patch("screenpy.abilities.authenticate_with_2fa.pyotp")
    def test_using_secret(self, mocked_pyotp):
        """Creates pyotp.TOTP instance"""
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
