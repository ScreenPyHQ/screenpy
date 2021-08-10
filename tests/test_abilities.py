import os
from unittest import mock

import pytest

from screenpy.abilities import AuthenticateWith2FA, BrowseTheWeb, MakeAPIRequests
from screenpy.exceptions import BrowsingError, RequestError


class TestBrowseTheWeb:
    def test_can_be_instantiated(self):
        b = BrowseTheWeb.using(None)

        assert isinstance(b, BrowseTheWeb)

    @mock.patch("screenpy.abilities.browse_the_web.Firefox")
    def test_using_firefox(self, mocked_firefox):
        BrowseTheWeb.using_firefox()

        mocked_firefox.assert_called_once()

    @mock.patch("screenpy.abilities.browse_the_web.Chrome")
    def test_using_chrome(self, mocked_chrome):
        BrowseTheWeb.using_chrome()

        mocked_chrome.assert_called_once()

    @mock.patch("screenpy.abilities.browse_the_web.Safari")
    def test_using_safari(self, mocked_safari):
        BrowseTheWeb.using_safari()

        mocked_safari.assert_called_once()

    @mock.patch.dict(os.environ, {"IOS_DEVICE_VERSION": "1"})
    @mock.patch("screenpy.abilities.browse_the_web.Remote")
    def test_using_ios(self, mocked_remote):
        BrowseTheWeb.using_ios()

        mocked_remote.assert_called_once()

    def test_using_ios_without_env_var(self):
        with pytest.raises(BrowsingError):
            BrowseTheWeb.using_ios()

    @mock.patch.dict(os.environ, {"ANDROID_DEVICE_VERSION": "1"})
    @mock.patch("screenpy.abilities.browse_the_web.Remote")
    def test_using_android(self, mocked_android):
        BrowseTheWeb.using_android()

        mocked_android.assert_called_once()

    def test_using_android_without_env_var(self):
        with pytest.raises(BrowsingError):
            BrowseTheWeb.using_android()


class TestAuthenticateWith2FA:
    def test_can_be_instantiated(self):
        a1 = AuthenticateWith2FA.using_secret("")
        a2 = AuthenticateWith2FA.using(None)

        assert isinstance(a1, AuthenticateWith2FA)
        assert isinstance(a2, AuthenticateWith2FA)

    @mock.patch("screenpy.abilities.authenticate_with_2fa.pyotp")
    def test_using_secret(self, mocked_pyotp):
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
