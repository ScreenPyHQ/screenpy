import pytest
from selenium.webdriver.common.keys import Keys
from unittest import mock

from screenpy.actions import (
    AcceptAlert,
    AddHeader,
    AddHeaders,
    Click,
    Debug,
    DismissAlert,
    DoubleClick,
    Enter,
    Enter2FAToken,
    generate_send_method_class,
    GoBack,
    GoForward,
    HoldDown,
    MoveMouse,
    Open,
    Pause,
    Press,
    RefreshPage,
    Release,
    RespondToThePrompt,
    RightClick,
    Select,
    SendAPIRequest,
    SendDELETERequest,
    SendGETRequest,
    SendHEADRequest,
    SendOPTIONSRequest,
    SendPATCHRequest,
    SendPOSTRequest,
    SendPUTRequest,
    SetHeaders,
    SwitchTo,
    SwitchToTab,
    Wait,
)
from screenpy.actions.select import SelectByIndex, SelectByText, SelectByValue
from screenpy import Target


class TestAcceptAlert:
    def test_can_be_instantiated(self):
        aa = AcceptAlert()

        assert isinstance(aa, AcceptAlert)


class TestAddHeader:
    def test_can_be_instantiated(self):
        ah1 = AddHeader(a="a")
        ah2 = AddHeaders(a="a")

        assert isinstance(ah1, AddHeader)
        assert isinstance(ah2, AddHeader)

    def test_can_be_secret(self):
        ah = AddHeader(a="a").secretly()

        assert ah.secret

    def test_remembers_headers(self):
        ah = AddHeader(a="a")

        assert ah.headers == {"a": "a"}

    def test_possible_arguments(self):
        """can handle dict, pairs, and kwargs"""
        ah1 = AddHeader({"a": 1})
        ah2 = AddHeader("a", 1)
        ah3 = AddHeader(a=1)
        ah4 = AddHeader({"a": 1}, b=2)

        assert ah1.headers == {"a": 1}
        assert ah2.headers == {"a": 1}
        assert ah3.headers == {"a": 1}
        assert ah4.headers == {"a": 1, "b": 2}

    def test_raises_on_odd_arguments(self):
        with pytest.raises(ValueError):
            AddHeader("a", 1, "b")

    def test_raises_on_non_iterable_arguments(self):
        with pytest.raises(ValueError):
            AddHeader("a")


class TestClick:
    def test_can_be_instantiated(self):
        c1 = Click.on(None)
        c2 = Click.on_the(None)

        assert isinstance(c1, Click)
        assert isinstance(c2, Click)


class TestDebug:
    def test_can_be_instantiated(self):
        d = Debug()

        assert isinstance(d, Debug)


class TestDismissAlert:
    def test_can_be_instantiated(self):
        da = DismissAlert()

        assert isinstance(da, DismissAlert)


class TestDoubleClick:
    def test_can_be_instantiated(self):
        dc1 = DoubleClick()
        dc2 = DoubleClick.on_the(None)

        assert isinstance(dc1, DoubleClick)
        assert isinstance(dc2, DoubleClick)


class TestEnter:
    def test_can_be_instantiated(self):
        e1 = Enter.the_text("test")
        e2 = Enter.the_text("test").into(None)
        e3 = Enter.the_keys("test").into(None)
        e4 = Enter.the_text("test").into_the(None)
        e5 = Enter.the_text("test").on(None)
        e6 = Enter.the_keys("test").on(None)
        e7 = Enter.the_text("test").into(None).then_press(None)
        e9 = Enter.the_secret("test")
        e8 = Press.the_keys("test")

        assert isinstance(e1, Enter)
        assert isinstance(e2, Enter)
        assert isinstance(e3, Enter)
        assert isinstance(e4, Enter)
        assert isinstance(e5, Enter)
        assert isinstance(e6, Enter)
        assert isinstance(e7, Enter)
        assert isinstance(e8, Enter)
        assert isinstance(e9, Enter)

    def test_secret_masks_text(self):
        """the_secret sets text_to_log to [CENSORED]"""
        text = "Keep it a secret to everybody"
        e = Enter.the_secret(text)

        assert e.text == text
        assert e.text_to_log == "[CENSORED]"

    def test_text_to_log_humanizes_keys(self):
        """unicode key values are turned into human-readable text"""
        e = Enter.the_text(Keys.ENTER)

        assert "ENTER" in e.text_to_log


class TestEnter2FAToken:
    def test_can_be_instantiated(self):
        e1 = Enter2FAToken.into(None)
        e2 = Enter2FAToken.into_the(None)

        assert isinstance(e1, Enter2FAToken)
        assert isinstance(e2, Enter2FAToken)


class TestGoBack:
    def test_can_be_instantiated(self):
        gb = GoBack()

        assert isinstance(gb, GoBack)


class TestGoForward:
    def test_can_be_instantiated(self):
        gf = GoForward()

        assert isinstance(gf, GoForward)


class TestHoldDown:
    def test_can_be_instantiated(self):
        hd1 = HoldDown.left_mouse_button()
        hd2 = HoldDown.left_mouse_button().on_the(None)
        hd3 = HoldDown(Keys.ALT)
        hd4 = HoldDown.command_or_control_key()

        assert isinstance(hd1, HoldDown)
        assert isinstance(hd2, HoldDown)
        assert isinstance(hd3, HoldDown)
        assert isinstance(hd4, HoldDown)

    @pytest.mark.parametrize(
        "platform,expected_key", [["Windows", Keys.CONTROL], ["Darwin", Keys.COMMAND]]
    )
    def test_command_or_control_key(self, platform, expected_key):
        """HoldDown figures out which key to use based on platform"""
        system_path = "screenpy.actions.hold_down.platform.system"
        with mock.patch(system_path, return_value=platform):
            hd = HoldDown.command_or_control_key()

        assert hd.key == expected_key

    def test_description_is_correct(self):
        """description is set based on the button or key"""
        hd1 = HoldDown.left_mouse_button()
        hd2 = HoldDown(Keys.LEFT_ALT)
        hd3 = HoldDown(Keys.SHIFT)

        assert hd1.description == "LEFT MOUSE BUTTON"
        assert hd2.description == "ALT"
        assert hd3.description == "SHIFT"


class TestMoveMouse:
    def test_can_be_instantiated(self):
        mm1 = MoveMouse.to_the(None)
        mm2 = MoveMouse.on_the(None)
        mm3 = MoveMouse.by_offset(1, 1)
        mm4 = MoveMouse.to_the(None).with_offset(1, 1)

        assert isinstance(mm1, MoveMouse)
        assert isinstance(mm2, MoveMouse)
        assert isinstance(mm3, MoveMouse)
        assert isinstance(mm4, MoveMouse)

    def test_description_is_set_by_method(self):
        """Description is built by what is included"""
        element_name = "test_element"
        coords = (1, 2)
        target = Target.the(element_name).located_by("*")
        mm1 = MoveMouse.to_the(target)
        mm2 = MoveMouse.by_offset(*coords)
        mm3 = MoveMouse.to_the(target).with_offset(*coords)

        assert element_name in mm1.description
        assert str(coords) in mm2.description
        assert element_name in mm3.description and str(coords) in mm3.description


class TestOpen:
    def test_can_be_instantiated(self):
        o1 = Open.browser_on(None)
        o2 = Open.their_browser_on(None)

        assert isinstance(o1, Open)
        assert isinstance(o2, Open)


class TestPause:
    def test_can_be_instantiated(self):
        p1 = Pause.for_(20)
        p2 = Pause.for_(20).seconds_because("test")
        p3 = Pause.for_(20).milliseconds_because("test")

        assert isinstance(p1, Pause)
        assert isinstance(p2, Pause)
        assert isinstance(p3, Pause)

    def test_seconds(self):
        """Choosing seconds stores the correct time"""
        duration = 20
        pause = Pause.for_(duration).seconds_because("test")

        assert pause.time == duration

    def test_milliseconds(self):
        """Choosing milliseconds stores the correct time"""
        duration = 20
        pause = Pause.for_(duration).milliseconds_because("Test")

        assert pause.time == duration / 1000.0

    def test_units_are_pluralized_correctly(self):
        """Unit is pluralized if more than 1"""
        p1 = Pause.for_(1).second_because("test")
        p2 = Pause.for_(1).milliseconds_because("test")
        p3 = Pause.for_(2).seconds_because("test")
        p4 = Pause.for_(2).milliseconds_because("test")

        assert not p1.unit.endswith("s")
        assert not p2.unit.endswith("s")
        assert p3.unit.endswith("s")
        assert p4.unit.endswith("s")

    def test_reason_is_massaged_correctly(self):
        p1 = Pause.for_(1).second_because("because reasons.")
        p2 = Pause.for_(1).second_because("reasons")
        p3 = Pause.for_(1000).milliseconds_because("because reasons.")
        p4 = Pause.for_(1000).milliseconds_because("reasons")

        assert p1.reason == p2.reason == "because reasons"
        assert p3.reason == p4.reason == "because reasons"


class TestRelease:
    def test_can_be_instantiated(self):
        r1 = Release.left_mouse_button()
        r2 = Release(Keys.ALT)
        r3 = Release.command_or_control_key()

        assert isinstance(r1, Release)
        assert isinstance(r2, Release)
        assert isinstance(r3, Release)

    @pytest.mark.parametrize(
        "platform,expected_key", [["Windows", Keys.CONTROL], ["Darwin", Keys.COMMAND]]
    )
    def test_command_or_control_key(self, platform, expected_key):
        """Release figures out which key to use based on platform"""
        system_path = "screenpy.actions.hold_down.platform.system"
        with mock.patch(system_path, return_value=platform):
            r = Release.command_or_control_key()

        assert r.key == expected_key

    def test_description_is_correct(self):
        """description is set based on the button or key"""
        r1 = Release.left_mouse_button()
        r2 = Release(Keys.LEFT_ALT)
        r3 = Release(Keys.SHIFT)

        assert r1.description == "LEFT MOUSE BUTTON"
        assert r2.description == "ALT"
        assert r3.description == "SHIFT"


class TestRefreshPage:
    def test_can_be_instantiated(self):
        r = RefreshPage()

        assert isinstance(r, RefreshPage)


class TestRespondToThePrompt:
    def test_can_be_instantiated(self):
        rttp = RespondToThePrompt.with_("test")

        assert isinstance(rttp, RespondToThePrompt)


class TestRightClick:
    def test_can_be_instantiated(self):
        rc1 = RightClick()
        rc2 = RightClick.on_the(None)

        assert isinstance(rc1, RightClick)
        assert isinstance(rc2, RightClick)


class TestSelect:
    def test_specifics_can_be_instantiated(self):
        by_index1 = Select.the_option_at_index(0)
        by_index2 = Select.the_option_at_index(0).from_(None)
        by_index3 = Select.the_option_at_index(0).from_the(None)
        by_text1 = Select.the_option_named("Option")
        by_text2 = Select.the_option_named("Option").from_(None)
        by_text3 = Select.the_option_named("Option").from_the(None)
        by_value1 = Select.the_option_with_value(1)
        by_value2 = Select.the_option_with_value(1).from_(None)
        by_value3 = Select.the_option_with_value(1).from_the(None)

        assert isinstance(by_index1, SelectByIndex)
        assert isinstance(by_index2, SelectByIndex)
        assert isinstance(by_index3, SelectByIndex)
        assert isinstance(by_text1, SelectByText)
        assert isinstance(by_text2, SelectByText)
        assert isinstance(by_text3, SelectByText)
        assert isinstance(by_value1, SelectByValue)
        assert isinstance(by_value2, SelectByValue)
        assert isinstance(by_value3, SelectByValue)


class TestSendAPIRequest:
    def test_can_be_instantiated(self):
        sar1 = SendAPIRequest("GET", "test")
        sar2 = SendAPIRequest("GET", "test").with_(some="kwarg")

        assert isinstance(sar1, SendAPIRequest)
        assert isinstance(sar2, SendAPIRequest)

    def test_stores_kwargs(self):
        """kwargs are stored to send in the request later"""
        test_kwargs = {"test": "kwarg"}
        sar = SendAPIRequest("GET", "test").with_(**test_kwargs)

        assert sar.kwargs == test_kwargs

    def test_can_be_secret(self):
        sar = SendAPIRequest("GET", "test").with_(test="kwarg").secretly()

        assert sar.secret


def test_generate_send_method_class_docstring():
    """Generated class and method's docstring both contain method name."""
    test_method = "TEST"

    SendTESTMethod = generate_send_method_class(test_method)

    assert test_method in SendTESTMethod.__doc__
    assert test_method in SendTESTMethod.to.__doc__


@pytest.mark.parametrize(
    "request_class",
    [
        SendDELETERequest,
        SendGETRequest,
        SendHEADRequest,
        SendOPTIONSRequest,
        SendPATCHRequest,
        SendPOSTRequest,
        SendPUTRequest,
    ],
)
def test_can_be_instantiated(request_class):
    """Send{METHOD}Request instantiation gives back SendAPIRequest"""
    sr1 = request_class.to("url")
    sr2 = request_class.to("url").with_(some="kwarg")

    assert isinstance(sr1, SendAPIRequest)
    assert isinstance(sr2, SendAPIRequest)


class TestSetHeaders:
    def test_can_be_instantiated(self):
        sh1 = SetHeaders(a="a")
        sh2 = SetHeaders.to(b="b")

        assert isinstance(sh1, SetHeaders)
        assert isinstance(sh2, SetHeaders)

    def test_can_be_secret(self):
        sh = SetHeaders(a=1).secretly()

        assert sh.secret

    def test_remembers_headers(self):
        sh = SetHeaders(a="a")

        assert sh.headers == {"a": "a"}

    def test_possible_arguments(self):
        """can handle dict, pairs, and kwargs"""
        sh1 = SetHeaders({"a": 1})
        sh2 = SetHeaders("a", 1)
        sh3 = SetHeaders(a=1)
        sh4 = SetHeaders({"a": 1}, b=2)

        assert sh1.headers == {"a": 1}
        assert sh2.headers == {"a": 1}
        assert sh3.headers == {"a": 1}
        assert sh4.headers == {"a": 1, "b": 2}

    def test_raises_on_odd_arguments(self):
        with pytest.raises(ValueError):
            SetHeaders("a", 1, "b")

    def test_raises_on_non_iterable_arguments(self):
        with pytest.raises(ValueError):
            SetHeaders("a")


class TestSwitchTo:
    def test_can_be_instantiated(self):
        st1 = SwitchTo.the(None)
        st2 = SwitchTo.default()

        assert isinstance(st1, SwitchTo)
        assert isinstance(st2, SwitchTo)


class TestSwitchToTab:
    def test_can_be_instantiated(self):
        stt = SwitchToTab(1)

        assert isinstance(stt, SwitchToTab)


class TestWait:
    def test_can_be_instantiated(self):
        def foo():
            pass

        w1 = Wait.for_the(mock.Mock())
        w2 = Wait(0).seconds_for_the(mock.Mock())
        w3 = Wait().using(foo)
        w4 = Wait().using(foo).with_(mock.Mock())

        assert isinstance(w1, Wait)
        assert isinstance(w2, Wait)
        assert isinstance(w3, Wait)
        assert isinstance(w4, Wait)

    def test_default_log_message(self):
        target_name = "spam"
        w = Wait.for_the(Target.the(target_name).located_by("//eggs"))

        assert "visibility_of_element_located" in w.log_message
        assert target_name in w.log_message

    def test_custom_log_message(self):
        target_name = "baked"
        args = [1, Target.the(target_name).located_by("//beans"), "and spam"]
        w = Wait().using(mock.Mock(), "{0}, {1}, {2}").with_(*args)

        assert all([str(arg) in w.log_message for arg in args])
