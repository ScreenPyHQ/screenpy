from unittest import mock

import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from screenpy import Target
from screenpy.abilities import AuthenticateWith2FA, BrowseTheWeb
from screenpy.actions import (
    AcceptAlert,
    Chain,
    Clear,
    Click,
    Debug,
    DismissAlert,
    DoubleClick,
    Enter,
    Enter2FAToken,
    GoBack,
    GoForward,
    HoldDown,
    MoveMouse,
    Open,
    Pause,
    RefreshPage,
    Release,
    RespondToThePrompt,
    RightClick,
    Select,
    SwitchTo,
    SwitchToTab,
    Wait,
)
from screenpy.exceptions import UnableToAct


def test_accept_alert(Tester):
    """AcceptAlert calls .accept()"""
    Tester.attempts_to(AcceptAlert())

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.browser.switch_to.alert.accept.assert_called_once()


def test_clear(Tester):
    """Clear finds its target and calls .clear()"""
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)

    Tester.attempts_to(Clear.the_text_from(fake_target))

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_find.assert_called_once_with(fake_target)
    mocked_btw.to_find.return_value.clear.assert_called_once()


class TestClick:
    def test_calls_click(self, Tester):
        """Click finds its target and calls .click()"""
        fake_xpath = "//xpath"
        fake_target = Target.the("fake").located_by(fake_xpath)

        Tester.attempts_to(Click.on_the(fake_target))

        mocked_btw = Tester.ability_to(BrowseTheWeb)
        mocked_btw.to_find.assert_called_once_with(fake_target)
        mocked_btw.to_find.return_value.click.assert_called_once()

    @mock.patch("screenpy.actions.web.chain.ActionChains")
    def test_can_be_chained(self, MockedActionChains, Tester):
        """Click chained calls .click()"""
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element

        Tester.attempts_to(Chain(Click.on_the(mock_target)))

        MockedActionChains().click.assert_called_once_with(mock_element)


class TestDebug:
    @mock.patch("screenpy.actions.web.debug.breakpoint")
    def test_breakpoint(self, mocked_breakpoint, Tester):
        """Debug calls breakpoint()"""
        Tester.attempts_to(Debug())

        mocked_breakpoint.assert_called_once()

    @mock.patch("screenpy.actions.web.debug.breakpoint")
    @mock.patch("screenpy.actions.web.debug.pdb")
    def test_falls_back_to_pdb(self, mocked_pdb, mocked_breakpoint, Tester):
        """Debug calls set_trace() if breakpoint is unavailable"""
        mocked_breakpoint.side_effect = NameError("name 'breakpoint' is not defined")

        Tester.attempts_to(Debug())

        mocked_pdb.set_trace.assert_called_once()


def test_dismiss_alert(Tester):
    """DismissAlert calls .dismiss()"""
    Tester.attempts_to(DismissAlert())

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.browser.switch_to.alert.dismiss.assert_called_once()


class TestDoubleClick:
    @mock.patch("screenpy.actions.web.chain.ActionChains")
    def test_calls_double_click(self, MockedActionChains, Tester):
        """DoubleClick calls .double_click()"""
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element

        Tester.attempts_to(Chain(DoubleClick.on_the(mock_target)))

        MockedActionChains().double_click.assert_called_once_with(
            on_element=mock_element
        )

    @mock.patch("screenpy.actions.web.chain.ActionChains")
    def test_without_element(self, MockedActionChains, Tester):
        """DoubleClick works with no target"""
        Tester.attempts_to(Chain(DoubleClick()))

        MockedActionChains().double_click.assert_called_once_with(on_element=None)

    @mock.patch("screenpy.actions.web.double_click.ActionChains")
    def test_can_be_performed(self, MockedActionChains, Tester):
        """DoubleClick can be performed directly"""
        Tester.attempts_to(DoubleClick())

        MockedActionChains().double_click.assert_called_once_with(on_element=None)


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
        with pytest.raises(UnableToAct):
            Tester.attempts_to(Enter.the_text("test"))

    @mock.patch("screenpy.actions.web.chain.ActionChains")
    def test_chained_calls_send_keys(self, MockedActionChains, Tester):
        """Enter chained with no element calls .send_keys()"""
        text = "test"

        Tester.attempts_to(Chain(Enter.the_text(text)))

        MockedActionChains().send_keys.assert_called_once_with(text)

    @mock.patch("screenpy.actions.web.chain.ActionChains")
    def test_chained_calls_send_keys_to_element(self, MockedActionChains, Tester):
        """Enter chained with an element calls .send_keys_to_element()"""
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element
        text = "test"

        Tester.attempts_to(Chain(Enter.the_text(text).into_the(mock_target)))

        MockedActionChains().send_keys_to_element.assert_called_once_with(
            mock_element, text
        )


class TestEnter2FAToken:
    def test_enter_2FA_token(self, Tester):
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

    @mock.patch("screenpy.actions.web.chain.ActionChains")
    def test_can_be_chained(self, MockedActionChains, Tester):
        """Enter2FAToken when chained calls .send_keys_to_element()"""
        text = "test"
        mocked_2fa = Tester.ability_to(AuthenticateWith2FA)
        mocked_2fa.to_get_token.return_value = text
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element

        Tester.attempts_to(Chain(Enter2FAToken.into_the(mock_target)))

        MockedActionChains().send_keys_to_element.assert_called_once_with(
            mock_element, text
        )


def test_go_back_uses_back(Tester):
    """GoBack uses .back()"""
    Tester.attempts_to(GoBack())

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.browser.back.assert_called_once()


def test_go_forward_uses_forward(Tester):
    """GoForward uses .forward()"""
    Tester.attempts_to(GoForward())

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.browser.forward.assert_called_once()


class TestHoldDown:
    def test_cannot_be_performed(self, Tester):
        """HoldDown action cannot be performed"""
        with pytest.raises(UnableToAct):
            Tester.attempts_to(HoldDown(Keys.SHIFT))

    @mock.patch("screenpy.actions.web.chain.ActionChains")
    def test_uses_key_down(self, MockedActionChains, Tester):
        """HoldDown key uses ActionChains.key_down"""
        Tester.attempts_to(Chain(HoldDown(Keys.ALT)))

        MockedActionChains().key_down.assert_called_once_with(Keys.ALT)

    @mock.patch("screenpy.actions.web.chain.ActionChains")
    def test_uses_click_and_hold(self, MockedActionChains, Tester):
        """HoldDown left mouse button uses ActionChains.click_and_hold"""
        Tester.attempts_to(Chain(HoldDown.left_mouse_button()))

        MockedActionChains().click_and_hold.assert_called_once()


class TestMoveMouse:
    @mock.patch("screenpy.actions.web.move_mouse.ActionChains")
    def test_calls_move_to_element(self, MockedActionChains, Tester):
        """MoveMouse calls move_to_element if element provided"""
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element

        Tester.attempts_to(MoveMouse.to_the(mock_target))

        MockedActionChains().move_to_element.assert_called_once_with(mock_element)

    @mock.patch("screenpy.actions.web.move_mouse.ActionChains")
    def test_calls_move_by_offset(self, MockedActionChains, Tester):
        """MoveMouse calls move_by_offset if offset provided"""
        offset = (1, 2)

        Tester.attempts_to(MoveMouse.by_offset(*offset))

        MockedActionChains().move_by_offset.assert_called_once_with(*offset)

    @mock.patch("screenpy.actions.web.move_mouse.ActionChains")
    def test_calls_move_to_element_by_offset(self, MockedActionChains, Tester):
        """MoveMouse calls move_to_element_by_offset if both provided"""
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element
        offset = (1, 2)

        Tester.attempts_to(MoveMouse.to_the(mock_target).with_offset(*offset))

        MockedActionChains().move_to_element_with_offset.assert_called_once_with(
            mock_element, *offset
        )

    @mock.patch("screenpy.actions.web.chain.ActionChains")
    def test_can_be_chained(self, MockedActionChains, Tester):
        """MoveMouse can be chained"""
        offset = (1, 2)

        Tester.attempts_to(Chain(MoveMouse.by_offset(*offset)))

        MockedActionChains().move_by_offset.assert_called_once_with(*offset)


def test_open(Tester):
    """Open calls .get()"""
    url = "https://localtest.test"

    Tester.attempts_to(Open.their_browser_on(url))

    mocked_browser = Tester.ability_to(BrowseTheWeb).browser
    mocked_browser.get.assert_called_once_with(url)


class TestPause:
    @mock.patch("screenpy.actions.web.pause.sleep")
    def test_calls_sleep(self, mocked_sleep, Tester):
        """Pause calls time.sleep()"""
        duration = 20

        Tester.attempts_to(Pause.for_(duration).seconds_because("test"))

        mocked_sleep.assert_called_once_with(duration)

    def test_complains_for_missing_reason(self, Tester):
        """Pause throws an assertion if no reason was given"""
        with pytest.raises(UnableToAct):
            Tester.attempts_to(Pause.for_(20))

    @mock.patch("screenpy.actions.web.chain.ActionChains")
    def test_can_be_chained(self, MockedActionChains, Tester):
        """Pause when chained calls .pause()"""
        duration = 20

        Tester.attempts_to(Chain(Pause.for_(duration).seconds_because("... reasons")))

        MockedActionChains().pause.assert_called_once_with(duration)


def test_refresh_page(Tester):
    """RefreshPage calls .refresh()"""
    Tester.attempts_to(RefreshPage())

    mocked_browser = Tester.ability_to(BrowseTheWeb).browser
    mocked_browser.refresh.assert_called_once()


class TestRelease:
    def test_cannot_be_performed(self, Tester):
        """Release action cannot be performed"""
        with pytest.raises(UnableToAct):
            Tester.attempts_to(Release(Keys.SHIFT))

    @mock.patch("screenpy.actions.web.chain.ActionChains")
    def test_uses_key_down(self, MockedActionChains, Tester):
        """Release key uses ActionChains.key_up"""
        Tester.attempts_to(Chain(Release(Keys.ALT)))

        MockedActionChains().key_up.assert_called_once_with(Keys.ALT)

    @mock.patch("screenpy.actions.web.chain.ActionChains")
    def test_uses_click_and_hold(self, MockedActionChains, Tester):
        """Release left mouse button uses ActionChains.release"""
        Tester.attempts_to(Chain(Release.left_mouse_button()))

        MockedActionChains().release.assert_called_once()


def test_respond_to_the_prompt(Tester):
    """RespondToThePrompt calls .send_keys() and .accept()"""
    text = "Hello!"

    Tester.attempts_to(RespondToThePrompt.with_(text))

    mocked_alert = Tester.ability_to(BrowseTheWeb).browser.switch_to.alert
    mocked_alert.send_keys.assert_called_once_with(text)
    mocked_alert.accept.assert_called_once()


class TestRightClick:
    @mock.patch("screenpy.actions.web.chain.ActionChains")
    def test_calls_double_click(self, MockedActionChains, Tester):
        """RightClick calls .context_click()"""
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element

        Tester.attempts_to(Chain(RightClick.on_the(mock_target)))

        MockedActionChains().context_click.assert_called_once_with(
            on_element=mock_element
        )

    @mock.patch("screenpy.actions.web.chain.ActionChains")
    def test_without_element(self, MockedActionChains, Tester):
        """RightClick works with no target"""
        Tester.attempts_to(Chain(RightClick()))

        MockedActionChains().context_click.assert_called_once_with(on_element=None)

    @mock.patch("screenpy.actions.web.right_click.ActionChains")
    def test_can_be_performed(self, MockedActionChains, Tester):
        """RightClick can be performed directly"""
        Tester.attempts_to(RightClick())

        MockedActionChains().context_click.assert_called_once_with(on_element=None)


class TestSelectByIndex:
    @mock.patch("screenpy.actions.web.select.SeleniumSelect")
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
        with pytest.raises(UnableToAct):
            Tester.attempts_to(Select.the_option_at_index(1))


class TestSelectByText:
    @mock.patch("screenpy.actions.web.select.SeleniumSelect")
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
        with pytest.raises(UnableToAct):
            Tester.attempts_to(Select.the_option_named("text"))


class TestSelectByValue:
    @mock.patch("screenpy.actions.web.select.SeleniumSelect")
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
        with pytest.raises(UnableToAct):
            Tester.attempts_to(Select.the_option_with_value("value"))


class TestSwitchTo:
    def test_switch_to_frame(self, Tester):
        """SwitchTo calls .frame()"""
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element

        Tester.attempts_to(SwitchTo.the(mock_target))

        mocked_btw = Tester.ability_to(BrowseTheWeb)
        mocked_btw.browser.switch_to.frame.assert_called_once_with(mock_element)

    def test_switch_to_default(self, Tester):
        """SwitchTo calls .default_content()"""
        Tester.attempts_to(SwitchTo.default())

        mocked_btw = Tester.ability_to(BrowseTheWeb)
        mocked_btw.browser.switch_to.default_content.assert_called_once()


def test_switch_to_tab(Tester):
    """SwitchToTab calls .window()"""
    number = 3
    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.browser.window_handles = range(number + 1)

    Tester.attempts_to(SwitchToTab(number))

    mocked_btw.browser.switch_to.window.assert_called_once_with(number - 1)


def test_wait(Tester):
    """Wait calls .to_wait_for()"""
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)

    Tester.attempts_to(Wait.for_the(fake_target).to_appear())

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_wait_for.assert_called_once_with(
        fake_target, timeout=20, cond=EC.visibility_of_element_located
    )
