from unittest import mock

import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from screenpy import Target
from screenpy.abilities import AuthenticateWith2FA, BrowseTheWeb, MakeAPIRequests
from screenpy.actions import (
    AcceptAlert,
    AddHeaders,
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
    SendAPIRequest,
    Select,
    SwitchTo,
    SwitchToTab,
    Wait,
)
from screenpy.exceptions import UnableToAct


def test_accept_alert_calls_accept(Tester):
    Tester.attempts_to(AcceptAlert())

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.browser.switch_to.alert.accept.assert_called_once()


def test_clear_calls_clear(Tester):
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)

    Tester.attempts_to(Clear.the_text_from(fake_target))

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_find.assert_called_once_with(fake_target)
    mocked_btw.to_find.return_value.clear.assert_called_once()


def test_add_headers_adds_headers(APITester):
    test_headers = {"test": "header", "another": "one"}
    session = APITester.ability_to(MakeAPIRequests).session
    session.headers = {}

    APITester.attempts_to(AddHeaders(**test_headers))

    assert session.headers == test_headers


class TestClick:
    def test_calls_click(self, Tester):
        fake_xpath = "//xpath"
        fake_target = Target.the("fake").located_by(fake_xpath)

        Tester.attempts_to(Click.on_the(fake_target))

        mocked_btw = Tester.ability_to(BrowseTheWeb)
        mocked_btw.to_find.assert_called_once_with(fake_target)
        mocked_btw.to_find.return_value.click.assert_called_once()

    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_can_be_chained(self, MockedActionChains, Tester):
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element

        Tester.attempts_to(Chain(Click.on_the(mock_target)))

        MockedActionChains().click.assert_called_once_with(mock_element)


class TestDebug:
    @mock.patch("screenpy.actions.debug.breakpoint")
    def test_calls_breakpoint(self, mocked_breakpoint, Tester):
        Tester.attempts_to(Debug())

        mocked_breakpoint.assert_called_once()

    @mock.patch("screenpy.actions.debug.breakpoint")
    @mock.patch("screenpy.actions.debug.pdb")
    def test_falls_back_to_pdb(self, mocked_pdb, mocked_breakpoint, Tester):
        mocked_breakpoint.side_effect = NameError("name 'breakpoint' is not defined")

        Tester.attempts_to(Debug())

        mocked_pdb.set_trace.assert_called_once()


def test_dismiss_alert_calls_dismiss(Tester):
    Tester.attempts_to(DismissAlert())

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.browser.switch_to.alert.dismiss.assert_called_once()


class TestDoubleClick:
    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_calls_double_click(self, MockedActionChains, Tester):
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element

        Tester.attempts_to(Chain(DoubleClick.on_the(mock_target)))

        MockedActionChains().double_click.assert_called_once_with(
            on_element=mock_element
        )

    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_without_target(self, MockedActionChains, Tester):
        Tester.attempts_to(Chain(DoubleClick()))

        MockedActionChains().double_click.assert_called_once_with(on_element=None)

    @mock.patch("screenpy.actions.double_click.ActionChains")
    def test_can_be_performed(self, MockedActionChains, Tester):
        Tester.attempts_to(DoubleClick())

        MockedActionChains().double_click.assert_called_once_with(on_element=None)


class TestEnter:
    def test_calls_send_keys(self, Tester):
        text = "test"
        fake_xpath = "//xpath"
        fake_target = Target.the("fake").located_by(fake_xpath)

        Tester.attempts_to(Enter.the_text(text).into_the(fake_target))

        mocked_btw = Tester.ability_to(BrowseTheWeb)
        mocked_btw.to_find.assert_called_once_with(fake_target)
        mocked_btw.to_find.return_value.send_keys.assert_called_once_with(text)

    def test_following_keys(self, Tester):
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
        with pytest.raises(UnableToAct):
            Tester.attempts_to(Enter.the_text("test"))

    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_chained_calls_send_keys(self, MockedActionChains, Tester):
        text = "test"

        Tester.attempts_to(Chain(Enter.the_text(text)))

        MockedActionChains().send_keys.assert_called_once_with(text)

    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_chained_calls_send_keys_to_element(self, MockedActionChains, Tester):
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element
        text = "test"

        Tester.attempts_to(Chain(Enter.the_text(text).into_the(mock_target)))

        MockedActionChains().send_keys_to_element.assert_called_once_with(
            mock_element, text
        )


class TestEnter2FAToken:
    def test_calls_relevant_methods(self, Tester):
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

    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_can_be_chained(self, MockedActionChains, Tester):
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
    Tester.attempts_to(GoBack())

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.browser.back.assert_called_once()


def test_go_forward_uses_forward(Tester):
    Tester.attempts_to(GoForward())

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.browser.forward.assert_called_once()


class TestHoldDown:
    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_calls_key_down(self, MockedActionChains, Tester):
        Tester.attempts_to(Chain(HoldDown(Keys.ALT)))

        MockedActionChains().key_down.assert_called_once_with(Keys.ALT)

    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_calls_click_and_hold(self, MockedActionChains, Tester):
        Tester.attempts_to(Chain(HoldDown.left_mouse_button()))

        MockedActionChains().click_and_hold.assert_called_once()


class TestMoveMouse:
    @mock.patch("screenpy.actions.move_mouse.ActionChains")
    def test_calls_move_to_element(self, MockedActionChains, Tester):
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element

        Tester.attempts_to(MoveMouse.to_the(mock_target))

        MockedActionChains().move_to_element.assert_called_once_with(mock_element)

    @mock.patch("screenpy.actions.move_mouse.ActionChains")
    def test_calls_move_by_offset(self, MockedActionChains, Tester):
        offset = (1, 2)

        Tester.attempts_to(MoveMouse.by_offset(*offset))

        MockedActionChains().move_by_offset.assert_called_once_with(*offset)

    @mock.patch("screenpy.actions.move_mouse.ActionChains")
    def test_calls_move_to_element_by_offset(self, MockedActionChains, Tester):
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element
        offset = (1, 2)

        Tester.attempts_to(MoveMouse.to_the(mock_target).with_offset(*offset))

        MockedActionChains().move_to_element_with_offset.assert_called_once_with(
            mock_element, *offset
        )

    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_can_be_chained(self, MockedActionChains, Tester):
        offset = (1, 2)

        Tester.attempts_to(Chain(MoveMouse.by_offset(*offset)))

        MockedActionChains().move_by_offset.assert_called_once_with(*offset)


def test_open_calls_get(Tester):
    url = "https://localtest.test"

    Tester.attempts_to(Open.their_browser_on(url))

    mocked_browser = Tester.ability_to(BrowseTheWeb).browser
    mocked_browser.get.assert_called_once_with(url)


class TestPause:
    @mock.patch("screenpy.actions.pause.sleep")
    def test_calls_sleep(self, mocked_sleep, Tester):
        duration = 20

        Tester.attempts_to(Pause.for_(duration).seconds_because("test"))

        mocked_sleep.assert_called_once_with(duration)

    def test_complains_for_missing_reason(self, Tester):
        with pytest.raises(UnableToAct):
            Tester.attempts_to(Pause.for_(20))

    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_can_be_chained(self, MockedActionChains, Tester):
        duration = 20

        Tester.attempts_to(Chain(Pause.for_(duration).seconds_because("... reasons")))

        MockedActionChains().pause.assert_called_once_with(duration)


def test_refresh_page_calls_refresh(Tester):
    Tester.attempts_to(RefreshPage())

    mocked_browser = Tester.ability_to(BrowseTheWeb).browser
    mocked_browser.refresh.assert_called_once()


class TestRelease:
    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_calls_key_down(self, MockedActionChains, Tester):
        Tester.attempts_to(Chain(Release(Keys.ALT)))

        MockedActionChains().key_up.assert_called_once_with(Keys.ALT)

    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_calls_release(self, MockedActionChains, Tester):
        Tester.attempts_to(Chain(Release.left_mouse_button()))

        MockedActionChains().release.assert_called_once()


def test_respond_to_the_prompt_calls_relevant_methods(Tester):
    """RespondToThePrompt calls .send_keys() and .accept()"""
    text = "Hello!"

    Tester.attempts_to(RespondToThePrompt.with_(text))

    mocked_alert = Tester.ability_to(BrowseTheWeb).browser.switch_to.alert
    mocked_alert.send_keys.assert_called_once_with(text)
    mocked_alert.accept.assert_called_once()


class TestRightClick:
    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_calls_double_click(self, MockedActionChains, Tester):
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element

        Tester.attempts_to(Chain(RightClick.on_the(mock_target)))

        MockedActionChains().context_click.assert_called_once_with(
            on_element=mock_element
        )

    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_without_target(self, MockedActionChains, Tester):
        Tester.attempts_to(Chain(RightClick()))

        MockedActionChains().context_click.assert_called_once_with(on_element=None)

    @mock.patch("screenpy.actions.right_click.ActionChains")
    def test_can_be_performed(self, MockedActionChains, Tester):
        Tester.attempts_to(RightClick())

        MockedActionChains().context_click.assert_called_once_with(on_element=None)


class TestSelectByIndex:
    @mock.patch("screenpy.actions.select.SeleniumSelect")
    def test_calls_select_by_index(self, mocked_selenium_select, Tester):
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
        with pytest.raises(UnableToAct):
            Tester.attempts_to(Select.the_option_at_index(1))


class TestSelectByText:
    @mock.patch("screenpy.actions.select.SeleniumSelect")
    def test_calls_select_by_visible_text(self, mocked_selenium_select, Tester):
        text = "test"
        fake_xpath = "//xpath"
        fake_target = Target.the("fake").located_by(fake_xpath)

        Tester.attempts_to(Select.the_option_named(text).from_the(fake_target))

        mocked_btw = Tester.ability_to(BrowseTheWeb)
        mocked_btw.to_find.assert_called_once_with(fake_target)
        mocked_select = mocked_selenium_select.return_value
        mocked_select.select_by_visible_text.assert_called_once_with(text)

    def test_complains_for_no_target(self, Tester):
        with pytest.raises(UnableToAct):
            Tester.attempts_to(Select.the_option_named("text"))


class TestSelectByValue:
    @mock.patch("screenpy.actions.select.SeleniumSelect")
    def test_calls_select_by_value(self, mocked_selenium_select, Tester):
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
        with pytest.raises(UnableToAct):
            Tester.attempts_to(Select.the_option_with_value("value"))


class TestSwitchTo:
    def test_switch_to_frame_calls_frame(self, Tester):
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element

        Tester.attempts_to(SwitchTo.the(mock_target))

        mocked_btw = Tester.ability_to(BrowseTheWeb)
        mocked_btw.browser.switch_to.frame.assert_called_once_with(mock_element)

    def test_switch_to_default_calls_default_content(self, Tester):
        Tester.attempts_to(SwitchTo.default())

        mocked_btw = Tester.ability_to(BrowseTheWeb)
        mocked_btw.browser.switch_to.default_content.assert_called_once()


def test_switch_to_tab_calls_window(Tester):
    number = 3
    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.browser.window_handles = range(number + 1)

    Tester.attempts_to(SwitchToTab(number))

    mocked_btw.browser.switch_to.window.assert_called_once_with(number - 1)


def test_wait_calls_to_wait_for(Tester):
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)

    Tester.attempts_to(Wait.for_the(fake_target).to_appear())

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_wait_for.assert_called_once_with(
        fake_target, timeout=20, cond=EC.visibility_of_element_located
    )


def test_send_api_request_parameters_passed_along(APITester):
    """Args and kwargs given to SendAPIRequest are passed to ``to_send``"""
    method = "GET"
    url = "TEST_URL"
    kwargs = {"test": "kwargs"}

    APITester.attempts_to(SendAPIRequest(method, url).with_(**kwargs))

    mocked_mar = APITester.ability_to(MakeAPIRequests)
    mocked_mar.to_send.assert_called_once_with(method, url, **kwargs)
