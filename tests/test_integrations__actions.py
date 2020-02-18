from unittest import mock

import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from screenpy import Target
from screenpy.abilities import AuthenticateWith2FA, BrowseTheWeb
from screenpy.actions import (
    AcceptAlert,
    Clear,
    Click,
    Debug,
    DismissAlert,
    Enter,
    Enter2FAToken,
    Open,
    Pause,
    RespondToThePrompt,
    Select,
    SwitchTo,
    Wait,
)
from screenpy.exceptions import UnableToActError


def test_accept_alert(Tester):
    """AcceptAlert calls .to_switch_to_alert() and .accept()"""
    Tester.attempts_to(AcceptAlert())

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_switch_to_alert.assert_called_once()
    mocked_alert = mocked_btw.to_switch_to_alert.return_value
    mocked_alert.accept.assert_called_once()


def test_clear(Tester):
    """Clear finds its target and calls .clear()"""
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)

    Tester.attempts_to(Clear.the_text_from(fake_target))

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_find.assert_called_once_with(fake_target)
    mocked_btw.to_find.return_value.clear.assert_called_once()


def test_click(Tester):
    """Click finds its target and calls .click()"""
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)

    Tester.attempts_to(Click.on_the(fake_target))

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_find.assert_called_once_with(fake_target)
    mocked_btw.to_find.return_value.click.assert_called_once()


class TestDebug:
    @mock.patch("screenpy.actions.debug.breakpoint")
    def test_breakpoint(self, mocked_breakpoint, Tester):
        """Debug calls breakpoint()"""
        Tester.attempts_to(Debug())

        mocked_breakpoint.assert_called_once()

    @mock.patch("screenpy.actions.debug.breakpoint")
    @mock.patch("screenpy.actions.debug.pdb")
    def test_falls_back_to_pdb(self, mocked_pdb, mocked_breakpoint, Tester):
        """Debug calls set_trace() if breakpoint is unavailable"""
        mocked_breakpoint.side_effect = NameError("name 'breakpoint' is not defined")

        Tester.attempts_to(Debug())

        mocked_pdb.set_trace.assert_called_once()


def test_dismiss_alert(Tester):
    """DismissAlert calls .to_switch_to_alert() and .dismiss()"""
    Tester.attempts_to(DismissAlert())

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_switch_to_alert.assert_called_once()
    mocked_alert = mocked_btw.to_switch_to_alert.return_value
    mocked_alert.dismiss.assert_called_once()


class TestEnter:
    def test_basic_action(self, Tester):
        """Enter finds its target and calls .send_keys()"""
        text = "test"
        fake_xpath = "//xpath"
        fake_target = Target.the("fake").located_by(fake_xpath)

        Tester.attempts_to(Enter.the_text(text).into_the(fake_target))

        mocked_btw = Tester.ability_to(BrowseTheWeb)
        mocked_btw.to_find.assert_called_once_with(fake_target)
        mocked_btw.to_find.return_value.send_keys.assert_called_once_with(text)

    def test_following_keys(self, Tester):
        """Enter hits the following keys"""
        text = "test"
        fake_xpath = "//xpath"
        fake_target = Target.the("fake").located_by(fake_xpath)

        Tester.attempts_to(
            Enter.the_text(text).into_the(fake_target).then_hit(Keys.ENTER)
        )

        mocked_btw = Tester.ability_to(BrowseTheWeb)
        mocked_btw.to_find.assert_called_once_with(fake_target)
        mocked_element = mocked_btw.to_find.return_value
        assert mocked_element.send_keys.call_count == 2
        called_args, _ = mocked_element.send_keys.call_args_list[1]
        assert Keys.ENTER in called_args

    def test_complains_for_no_target(self, Tester):
        """Enter complains if no target was given"""
        with pytest.raises(UnableToActError):
            Tester.attempts_to(Enter.the_text("test"))


def test_enter_2FA_token(Tester):
    """Enter2FAToken calls .to_get_token(), .to_find(), and .send_keys()"""
    text = "test"
    mocked_2fa = Tester.ability_to(AuthenticateWith2FA)
    mocked_2fa.to_get_token.return_value = text
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)

    Tester.attempts_to(Enter2FAToken.into_the(fake_target))

    mocked_2fa.to_get_token.assert_called_once()
    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_find.assert_called_once_with(fake_target)
    mocked_btw.to_find.return_value.send_keys.assert_called_once_with(text)


def test_open(Tester):
    """Open calls .get()"""
    url = "https://localtest.test"

    Tester.attempts_to(Open.their_browser_on(url))

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_visit.assert_called_once_with(url)


@mock.patch("screenpy.actions.pause.sleep")
def test_pause(mocked_sleep, Tester):
    """Pause calls time.sleep()"""
    duration = 20

    Tester.attempts_to(Pause.for_(duration).seconds_because("test"))

    mocked_sleep.assert_called_once_with(duration)


def test_pause_complains_for_no_reason(Tester):
    """Pause throws an assertion if no reason was given"""
    with pytest.raises(UnableToActError):
        Tester.attempts_to(Pause.for_(20))


def test_respond_to_the_prompt(Tester):
    """RespondToThePrompt calls .to_switch_to_alert() and .dismiss()"""
    text = "Hello!"

    Tester.attempts_to(RespondToThePrompt.with_(text))

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_switch_to_alert.assert_called_once()
    mocked_alert = mocked_btw.to_switch_to_alert.return_value
    mocked_alert.send_keys.assert_called_once_with(text)
    mocked_alert.accept.assert_called_once()


class TestSelectByIndex:
    @mock.patch("screenpy.actions.select.SeleniumSelect")
    def test_basic_action(self, mocked_selenium_select, Tester):
        """SelectByIndex finds its target and calls .select_by_index()"""
        index = 1
        fake_xpath = "//xpath"
        fake_target = Target.the("fake").located_by(fake_xpath)

        Tester.attempts_to(Select.the_option_at_index(index).from_the(fake_target))

        mocked_btw = Tester.ability_to(BrowseTheWeb)
        mocked_btw.to_find.assert_called_once_with(fake_target)
        mocked_selenium_select.return_value.select_by_index.assert_called_once_with(
            str(index)
        )

    def test_complains_for_no_target(self, Tester):
        """SelectByIndex complains if no target was given"""
        with pytest.raises(UnableToActError):
            Tester.attempts_to(Select.the_option_at_index(1))


class TestSelectByText:
    @mock.patch("screenpy.actions.select.SeleniumSelect")
    def test_basic_action(self, mocked_selenium_select, Tester):
        """SelectByText finds its target and calls .select_by_visible_text()"""
        text = "test"
        fake_xpath = "//xpath"
        fake_target = Target.the("fake").located_by(fake_xpath)

        Tester.attempts_to(Select.the_option_named(text).from_the(fake_target))

        mocked_btw = Tester.ability_to(BrowseTheWeb)
        mocked_btw.to_find.assert_called_once_with(fake_target)
        mocked_select = mocked_selenium_select.return_value
        mocked_select.select_by_visible_text.assert_called_once_with(text)

    def test_complains_for_no_target(self, Tester):
        """SelectByText complains if no target was given"""
        with pytest.raises(UnableToActError):
            Tester.attempts_to(Select.the_option_named("text"))


class TestSelectByValue:
    @mock.patch("screenpy.actions.select.SeleniumSelect")
    def test_basic_action(self, mocked_selenium_select, Tester):
        """SelectByValue finds its target and calls .select_by_visible_text()"""
        value = 1337
        fake_xpath = "//xpath"
        fake_target = Target.the("fake").located_by(fake_xpath)

        Tester.attempts_to(Select.the_option_with_value(value).from_the(fake_target))

        mocked_btw = Tester.ability_to(BrowseTheWeb)
        mocked_btw.to_find.assert_called_once_with(fake_target)
        mocked_selenium_select.return_value.select_by_value.assert_called_once_with(
            str(value)
        )

    def test_complains_for_no_target(self, Tester):
        """SelectByValue complains if no target was given"""
        with pytest.raises(UnableToActError):
            Tester.attempts_to(Select.the_option_with_value("value"))


class TestSwitchTo:
    def test_switch_to_frame(self, Tester):
        """SwitchTo calls .to_switch_to()"""
        fake_xpath = "//xpath"
        fake_target = Target.the("fake").located_by(fake_xpath)

        Tester.attempts_to(SwitchTo.the(fake_target))

        mocked_btw = Tester.ability_to(BrowseTheWeb)
        mocked_btw.to_switch_to.assert_called_once_with(fake_target)

    def test_switch_to_default(self, Tester):
        """SwitchTo calls .to_switch_to_default()"""
        Tester.attempts_to(SwitchTo.default())

        mocked_btw = Tester.ability_to(BrowseTheWeb)
        mocked_btw.to_switch_to_default.assert_called_once()


def test_wait(Tester):
    """Wait calls .to_wait_for()"""
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)

    Tester.attempts_to(Wait.for_the(fake_target).to_appear())

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_wait_for.assert_called_once_with(
        fake_target, timeout=20, cond=EC.visibility_of_element_located
    )
