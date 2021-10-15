import logging
import sys
import time
from typing import List
from unittest import mock

import pytest
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

from screenpy import Director, Target, Actor, settings
from screenpy.abilities import AuthenticateWith2FA, BrowseTheWeb, MakeAPIRequests
from screenpy.actions import (
    AcceptAlert,
    AddHeaders,
    AttachTheFile,
    Chain,
    Clear,
    Click,
    Debug,
    DismissAlert,
    DoubleClick,
    Enter,
    Enter2FAToken,
    Eventually,
    GoBack,
    GoForward,
    HoldDown,
    MakeNote,
    MoveMouse,
    Open,
    Pause,
    RefreshPage,
    Release,
    RespondToThePrompt,
    RightClick,
    SaveConsoleLog,
    SaveScreenshot,
    See,
    SeeAllOf,
    SeeAnyOf,
    Select,
    SendAPIRequest,
    SetHeaders,
    SwitchTo,
    SwitchToTab,
    Wait,
)
from screenpy.directions import noted_under
from screenpy.exceptions import DeliveryError, UnableToAct, UnableToDirect
from screenpy.protocols import Performable


def test_accept_alert_calls_accept(Tester):
    Tester.attempts_to(AcceptAlert())

    mocked_browser = Tester.ability_to(BrowseTheWeb).browser
    mocked_browser.switch_to.alert.accept.assert_called_once()


class TestAddHeaders:
    def test_adds_headers(self, APITester):
        test_headers = {"test": "header", "another": "one"}
        session = APITester.ability_to(MakeAPIRequests).session
        session.headers = {}

        APITester.attempts_to(AddHeaders(**test_headers))

        assert session.headers == test_headers

    def test_logs_headers(self, APITester, caplog):
        test_headers = {"foo": "bar"}

        with caplog.at_level(logging.INFO):
            APITester.attempts_to(AddHeaders(**test_headers))

        assert str(test_headers) in caplog.text

    def test_hides_secret_headers(self, APITester, caplog):
        test_headers = {"foo": "bar"}

        with caplog.at_level(logging.INFO):
            APITester.attempts_to(AddHeaders(**test_headers).secretly())

        assert str(test_headers) not in caplog.text


class TestAttachTheFile:
    @mock.patch("screenpy.actions.attach_the_file.the_narrator")
    def test_save_screenshot_sends_kwargs_to_attach(self, mocked_narrator, Tester):
        test_path = "souiiie.png"
        test_kwargs = {"color": "Red", "weather": "Tornado"}

        Tester.attempts_to(AttachTheFile(test_path, **test_kwargs))

        mocked_narrator.attaches_a_file.assert_called_once_with(
            test_path, **test_kwargs
        )


def test_clear_calls_clear(Tester):
    fake_target = Target.the("fake").located_by("//xpath")

    Tester.attempts_to(Clear.the_text_from(fake_target))

    mocked_browser = Tester.ability_to(BrowseTheWeb).browser
    mocked_browser.find_element.return_value.clear.assert_called_once()


class TestClick:
    def test_calls_click(self, Tester):
        fake_target = Target.the("fake").located_by("//xpath")

        Tester.attempts_to(Click.on_the(fake_target))

        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.find_element.return_value.click.assert_called_once()

    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_can_be_chained(self, MockedActionChains, Tester):
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element

        Tester.attempts_to(Chain(Click.on_the(mock_target)))

        MockedActionChains().click.assert_called_once_with(on_element=mock_element)

    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_target_is_only_optional_for_chaining(self, MockedActionChains, Tester):
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element

        Tester.attempts_to(Chain(Click()))
        Tester.attempts_to(Chain(Click.on_the(mock_target)))

        with pytest.raises(UnableToAct):
            Tester.attempts_to(Click())


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

    mocked_browser = Tester.ability_to(BrowseTheWeb).browser
    mocked_browser.switch_to.alert.dismiss.assert_called_once()


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
        fake_target = Target.the("fake").located_by("//xpath")

        Tester.attempts_to(Enter.the_text(text).into_the(fake_target))

        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.find_element.return_value.send_keys.assert_called_once_with(text)

    def test_following_keys(self, Tester):
        text = "test"
        fake_target = Target.the("fake").located_by("//xpath")

        Tester.attempts_to(
            Enter.the_text(text).into_the(fake_target).then_hit(Keys.ENTER)
        )

        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_element = mocked_browser.find_element.return_value
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
        text = "test"
        mocked_2fa = Tester.ability_to(AuthenticateWith2FA)
        mocked_2fa.to_get_token.return_value = text
        fake_target = Target.the("fake").located_by("//xpath")

        Tester.attempts_to(Enter2FAToken.into_the(fake_target))
        mocked_2fa.to_get_token.assert_called_once()
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.find_element.return_value.send_keys.assert_called_once_with(text)

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

    mocked_browser = Tester.ability_to(BrowseTheWeb).browser
    mocked_browser.back.assert_called_once()


def test_go_forward_uses_forward(Tester):
    Tester.attempts_to(GoForward())

    mocked_browser = Tester.ability_to(BrowseTheWeb).browser
    mocked_browser.forward.assert_called_once()


class TestHoldDown:
    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_calls_key_down(self, MockedActionChains, Tester):
        Tester.attempts_to(Chain(HoldDown(Keys.ALT)))

        MockedActionChains().key_down.assert_called_once_with(Keys.ALT)

    @mock.patch("screenpy.actions.chain.ActionChains")
    def test_calls_click_and_hold(self, MockedActionChains, Tester):
        Tester.attempts_to(Chain(HoldDown.left_mouse_button()))

        MockedActionChains().click_and_hold.assert_called_once()


class TestMakeNote:
    def test_answers_question(self, Tester):
        MockQuestion = mock.Mock()

        Tester.attempts_to(MakeNote.of_the(MockQuestion).as_("test"))

        assert MockQuestion.answered_by.called_once_with(Tester)

    def test_raises_without_key(self, Tester):
        with pytest.raises(UnableToAct):
            Tester.attempts_to(MakeNote.of_the(None))

    def test_adds_note_to_director(self, Tester):
        key = "key"
        value = "note"
        MockQuestion = mock.Mock()
        MockQuestion.answered_by.return_value = value

        Tester.attempts_to(MakeNote.of_the(MockQuestion).as_(key))

        assert Director().looks_up(key) == value

    def test_using_note_immediately_raises_with_docs(self, Tester):
        """Raised exception points to docs"""
        MockQuestion = mock.Mock()
        MockElement = mock.Mock()
        key = "spam, spam, spam, spam, baked beans, and spam"

        with pytest.raises(UnableToDirect) as exc:
            Tester.attempts_to(
                MakeNote.of_the(MockQuestion).as_(key),
                Enter.the_text(noted_under(key).into_the(MockElement)),
            )

        assert "screenpy-docs.readthedocs.io" in str(exc.value)

    def test_can_use_value_instead_of_question(self, Tester):
        key = "key"
        test_note = "note"

        Tester.attempts_to(MakeNote.of_the(test_note).as_(key))

        assert Director().looks_up(key) == test_note


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


class TestSaveConsoleLog:
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_calls_open_with_path(self, mocked_open, Tester):
        test_path = "jhowlett/images/a_wolverine.py"
        browser = Tester.ability_to(BrowseTheWeb).browser
        browser.get_log.return_value = ["logan"]

        Tester.attempts_to(SaveConsoleLog(test_path))

        mocked_open.assert_called_once_with(test_path, "w+", encoding="utf-8")

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_writes_log(self, mocked_open, Tester):
        test_path = "ssummers/images/a_cyclops.py"
        test_log = ["shot a beam", "shot a second beam", "closed my eyes"]
        browser = Tester.ability_to(BrowseTheWeb).browser
        browser.get_log.return_value = test_log

        Tester.attempts_to(SaveConsoleLog(test_path))

        file_descriptor = mocked_open()
        file_descriptor.write.assert_called_once_with("\n".join(test_log))

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch("screenpy.actions.save_console_log.AttachTheFile")
    def test_sends_kwargs_to_attach(self, mocked_atf, mocked_open, Tester):
        test_path = "doppelganger.png"
        test_kwargs = {"name": "Mystique"}
        browser = Tester.ability_to(BrowseTheWeb).browser
        browser.get_log.return_value = [1, 2, 3]

        Tester.attempts_to(SaveConsoleLog(test_path).and_attach_it(**test_kwargs))

        mocked_atf.assert_called_once_with(test_path, **test_kwargs)


class TestSaveScreenshot:
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_calls_open_with_path(self, mocked_open, Tester):
        test_path = "bwayne/images/a_bat.py"

        Tester.attempts_to(SaveScreenshot(test_path))

        mocked_open.assert_called_once_with(test_path, "wb+")

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch("screenpy.actions.save_screenshot.AttachTheFile")
    def test_sends_kwargs_to_attach(self, mocked_atf, mocked_open, Tester):
        test_path = "souiiie.png"
        test_kwargs = {"color": "Red", "weather": "Tornado"}

        Tester.attempts_to(SaveScreenshot(test_path).and_attach_it(**test_kwargs))

        mocked_atf.assert_called_once_with(test_path, **test_kwargs)


class TestSee:
    @mock.patch("screenpy.actions.see.assert_that")
    def test_calls_assert_that_with_answered_question(self, mocked_assert_that, Tester):
        mock_question = mock.Mock()
        mock_question.describe.return_value = "What was your mother?"
        mock_resolution = mock.Mock()
        mock_resolution.describe.return_value = "A hamster!"

        Tester.should(See.the(mock_question, mock_resolution))

        mock_question.answered_by.assert_called_once_with(Tester)
        mocked_assert_that.assert_called_once_with(
            mock_question.answered_by.return_value, mock_resolution
        )

    @mock.patch("screenpy.actions.see.assert_that")
    def test_calls_assert_that_with_value(self, mocked_assert_that, Tester):
        test_value = "Your father smelt of"
        mock_resolution = mock.Mock()
        mock_resolution.describe.return_value = "Elderberries!"

        Tester.should(See.the(test_value, mock_resolution))

        mocked_assert_that.assert_called_once_with(test_value, mock_resolution)


class TestSeeAllOf:
    @mock.patch("screenpy.actions.see_all_of.See")
    def test_calls_see_for_each_test(self, MockedSee, Tester):
        num_tests = 3
        tests = ((mock.Mock(), mock.Mock()),) * num_tests

        Tester.should(SeeAllOf.the(*tests))

        assert MockedSee.the.call_count == num_tests
        # In 3.7 and earlier, you can't get the .args of a method call from
        # the mocked instance. We can't do the full test there.
        if sys.version_info >= (3, 8):
            for num, test in enumerate(tests):
                assert MockedSee.method_calls[num].args == test


class TestSeeAnyOf:
    @mock.patch("screenpy.actions.see_any_of.See")
    def test_calls_see_for_each_test(self, MockedSee, Tester):
        num_tests = 3
        tests = ((mock.Mock(), mock.Mock()),) * num_tests

        Tester.should(SeeAnyOf.the(*tests))

        assert MockedSee.the.call_count == num_tests
        # In 3.7 and earlier, you can't get the .args of a method call from
        # the mocked instance. We can't do the full test there.
        if sys.version_info >= (3, 8):
            for num, test in enumerate(tests):
                assert MockedSee.method_calls[num].args == test


class TestSelectByIndex:
    @mock.patch("screenpy.actions.select.SeleniumSelect")
    def test_calls_select_by_index(self, mocked_selenium_select, Tester):
        index = 1
        fake_target = Target.the("fake").located_by("//xpath")

        Tester.attempts_to(Select.the_option_at_index(index).from_the(fake_target))

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
        fake_target = Target.the("fake").located_by("//xpath")

        Tester.attempts_to(Select.the_option_named(text).from_the(fake_target))

        mocked_select = mocked_selenium_select.return_value
        mocked_select.select_by_visible_text.assert_called_once_with(text)

    def test_complains_for_no_target(self, Tester):
        with pytest.raises(UnableToAct):
            Tester.attempts_to(Select.the_option_named("text"))


class TestSelectByValue:
    @mock.patch("screenpy.actions.select.SeleniumSelect")
    def test_calls_select_by_value(self, mocked_selenium_select, Tester):
        value = 1337
        fake_target = Target.the("fake").located_by("//xpath")

        Tester.attempts_to(Select.the_option_with_value(value).from_the(fake_target))

        mocked_selenium_select.return_value.select_by_value.assert_called_once_with(
            str(value)
        )

    def test_complains_for_no_target(self, Tester):
        with pytest.raises(UnableToAct):
            Tester.attempts_to(Select.the_option_with_value("value"))


class TestSetHeaders:
    def test_sets_headers(self, APITester):
        test_headers = {"test": "header", "another": "one"}
        session = APITester.ability_to(MakeAPIRequests).session
        session.headers = {"foo": "bar"}

        APITester.attempts_to(SetHeaders(**test_headers))

        assert session.headers == test_headers

    def test_logs_headers(self, APITester, caplog):
        test_headers = {"foo": "bar"}

        with caplog.at_level(logging.INFO):
            APITester.attempts_to(SetHeaders(**test_headers))

        assert str(test_headers) in caplog.text

    def test_hides_secret_headers(self, APITester, caplog):
        test_headers = {"foo": "bar"}

        with caplog.at_level(logging.INFO):
            APITester.attempts_to(SetHeaders(**test_headers).secretly())

        assert str(test_headers) not in caplog.text


class TestSwitchTo:
    def test_switch_to_frame_calls_frame(self, Tester):
        mock_target = mock.Mock()
        mock_element = "element"
        mock_target.found_by.return_value = mock_element

        Tester.attempts_to(SwitchTo.the(mock_target))

        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.switch_to.frame.assert_called_once_with(mock_element)

    def test_switch_to_default_calls_default_content(self, Tester):
        Tester.attempts_to(SwitchTo.default())

        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.switch_to.default_content.assert_called_once()


def test_switch_to_tab_calls_window(Tester):
    number = 3
    mocked_browser = Tester.ability_to(BrowseTheWeb).browser
    mocked_browser.window_handles = range(number + 1)

    Tester.attempts_to(SwitchToTab(number))

    mocked_browser.switch_to.window.assert_called_once_with(number - 1)


class TestSendAPIRequest:
    def test_parameters_passed_along(self, APITester):
        """Args and kwargs given to SendAPIRequest are passed to ``to_send``"""
        method = "GET"
        url = "TEST_URL"
        kwargs = {"test": "kwargs"}

        APITester.attempts_to(SendAPIRequest(method, url).with_(**kwargs))

        mocked_mar = APITester.ability_to(MakeAPIRequests)
        mocked_mar.to_send.assert_called_once_with(method, url, **kwargs)

    def test_parameters_logged(self, APITester, caplog):
        kwargs = {"test": "kwargs", "data": "foo"}

        with caplog.at_level(logging.INFO):
            APITester.attempts_to(SendAPIRequest("GET", "TEST_URL").with_(**kwargs))

        assert str(kwargs) in caplog.text

    def test_parameters_not_logged_if_secret(self, APITester, caplog):
        kwargs = {"test": "kwargs", "data": "foo"}

        with caplog.at_level(logging.INFO):
            APITester.attempts_to(
                SendAPIRequest("GET", "TEST_URL").with_(**kwargs).secretly()
            )

        assert str(kwargs) not in caplog.text


class TestWait:
    @mock.patch("screenpy.actions.wait.EC")
    @mock.patch("screenpy.actions.wait.WebDriverWait")
    def test_defaults(self, mocked_webdriverwait, mocked_ec, Tester):
        test_target = Target.the("foo").located_by("//bar")
        mocked_ec.visibility_of_element_located.__name__ = "foo"

        Tester.attempts_to(Wait.for_the(test_target))

        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_webdriverwait.assert_called_once_with(mocked_browser, settings.TIMEOUT)
        mocked_ec.visibility_of_element_located.assert_called_once_with(test_target)
        mocked_webdriverwait.return_value.until.assert_called_once_with(
            mocked_ec.visibility_of_element_located.return_value
        )

    @mock.patch("screenpy.actions.wait.WebDriverWait")
    def test_custom(self, mocked_webdriverwait, Tester):
        test_func = mock.Mock()
        test_func.__name__ = "foo"

        Tester.attempts_to(Wait().using(test_func))

        mocked_webdriverwait.return_value.until.assert_called_once_with(
            test_func.return_value
        )

    @mock.patch("screenpy.actions.wait.EC")
    @mock.patch("screenpy.actions.wait.WebDriverWait")
    def test_exception(self, mocked_webdriverwait, mocked_ec, Tester):
        test_target = Target.the("foo").located_by("//bar")
        mocked_ec.visibility_of_element_located.__name__ = "foo"
        mocked_webdriverwait.return_value.until.side_effect = WebDriverException

        with pytest.raises(DeliveryError) as excinfo:
            Tester.attempts_to(Wait.for_the(test_target))

        assert str(test_target) in str(excinfo.value)


RUNTIME_ERROR_MSG = "This is supposed to fail"


class ExceptionPerformable:
    """A performable which raises an exception.

    For testing Eventually.
    """

    def perform_as(self, the_actor: Actor) -> None:
        raise RuntimeError(RUNTIME_ERROR_MSG)


class LoopExceptionPerformable:
    """A performable which raises many exceptions, in a loop.

    For testing Eventually.
    """

    def perform_as(self, the_actor: Actor) -> None:
        self.cur_ind = (self.cur_ind + 1) % len(self.errorlist)
        raise self.errorlist[self.cur_ind]

    def __init__(self, errorlist: List[Exception] = None) -> None:
        if errorlist is None:
            errorlist = [RuntimeError(RUNTIME_ERROR_MSG)]
        self.errorlist = errorlist
        self.cur_ind = -1


class EventualPerformable:
    """A performable which keeps track of how often it's been called.

    For testing Eventually.
    """

    def perform_as(self, the_actor: Actor) -> None:
        if self.start is None:
            self.start = time.time()
            self.end = self.start + self.duration

        if time.time() > self.end:
            return
        self.loops += 1
        raise RuntimeError("Supposed to fail until duration met")

    def __init__(self, duration):
        self.start = None
        self.end = None
        self.duration = duration
        self.loops = 0


class TestEventually:
    def do_timeout(self, ev: Performable, Tester: Actor):
        start = time.time()
        try:
            ev.perform_as(Tester)
        except DeliveryError:
            pass
        elapsed = time.time() - start
        return elapsed

    def test_timeout_occurs(self, Tester: Actor):
        timeout = 1
        ev = Eventually(ExceptionPerformable()).for_(timeout).seconds()

        elapsed = self.do_timeout(ev, Tester)

        assert int(elapsed) == timeout

    @pytest.mark.parametrize("poll,expected_loops", [[0.1, 10], [0.5, 2]])
    def test_does_looping(self, poll, expected_loops, Tester: Actor):
        expected_elapsed = 1
        ev = (
            Eventually(EventualPerformable(expected_elapsed))
            .trying_every(poll)
            .seconds()
            .for_(5)
            .seconds()
        )

        elapsed = self.do_timeout(ev, Tester)

        assert int(elapsed) == expected_elapsed
        assert ev.performable.loops == expected_loops

    def test_catches_exceptions(self, Tester: Actor):
        ev = Eventually(ExceptionPerformable()).for_(1).second()

        with pytest.raises(DeliveryError) as exexc:
            ev.perform_as(Tester)

        assert RUNTIME_ERROR_MSG in str(exexc)

    def test__timeframebuilder_is_performable(self, Tester: Actor):
        ev = Eventually(EventualPerformable(0)).for_(1)

        # test passes if no exception is raised
        ev.perform_as(Tester)

    def test_valueerror_when_poll_is_larger_than_timeout(self, Tester: Actor):
        ev = (
            Eventually(ExceptionPerformable())
            .polling_every(0.2)
            .seconds()
            .for_(0.1)
            .seconds()
        )

        with pytest.raises(ValueError) as exexc:
            ev.perform_as(Tester)

        assert "poll must be less than or equal to timeout" in str(exexc)

    def test_mentions_all_errors(self, Tester: Actor):
        exc1 = ValueError("These tracts of land aren't that huge!")
        exc2 = TypeError("This witch does not weigh as much as a duck!")
        ev = (
            Eventually(LoopExceptionPerformable([exc1, exc2]))
            .polling_every(0.1)
            .seconds()
            .for_(0.2)
            .seconds()
        )

        with pytest.raises(DeliveryError) as exexc:
            ev.perform_as(Tester)

        assert exc1.__class__.__name__ in str(exexc.value)
        assert str(exc1) in str(exexc.value)
        assert exc2.__class__.__name__ in str(exexc.value)
        assert str(exc2) in str(exexc.value)
