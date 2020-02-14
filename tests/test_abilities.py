from unittest import mock

import pytest

from screenpy.abilities.browse_the_web import BaseAbility, BrowseTheWeb


class TestBaseAbility:
    def test_forget_must_be_overridden(self):
        """forget must be overridden by subclasses"""

        class SubclassedAbility(BaseAbility):
            pass

        subclassed_ability = SubclassedAbility()

        with pytest.raises(NotImplementedError):
            subclassed_ability.forget()


class TestBrowseTheWeb:
    def test_can_be_instantiated(self):
        """BrowseTheWeb can be instantiated"""
        b = BrowseTheWeb.using(None)

        assert isinstance(b, BrowseTheWeb)

    @mock.patch("screenpy.abilities.browse_the_web.Firefox")
    def test_using_firefox(self, mocked_firefox):
        """BrowseTheWeb can use Firefox as a default"""
        BrowseTheWeb.using_firefox()

        mocked_firefox.assert_called_once()

    @mock.patch("screenpy.abilities.browse_the_web.Chrome")
    def test_using_chrome(self, mocked_chrome):
        """BrowseTheWeb can use Chrome as a default"""
        BrowseTheWeb.using_chrome()

        mocked_chrome.assert_called_once()

    @mock.patch("screenpy.abilities.browse_the_web.Safari")
    def test_using_safari(self, mocked_safari):
        """BrowseTheWeb can use Safari as a default"""
        BrowseTheWeb.using_safari()

        mocked_safari.assert_called_once()

    @mock.patch("screenpy.abilities.browse_the_web.Remote")
    def test_using_ios(self, mocked_remote):
        """BrowseTheWeb can use IOS as a default"""
        BrowseTheWeb.using_ios()

        mocked_remote.assert_called_once()

    @mock.patch("screenpy.abilities.browse_the_web.Remote")
    def test_using_android(self, mocked_android):
        """BrowseTheWeb can use Android as a default"""
        BrowseTheWeb.using_android()

        mocked_android.assert_called_once()
