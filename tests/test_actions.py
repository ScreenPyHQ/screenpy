import pytest
from selenium.webdriver.common.keys import Keys
from unittest import mock

from screenpy.actions import (
    AcceptAlert,
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
    Press,
    RefreshPage,
    Release,
    RespondToThePrompt,
    RightClick,
    Select,
    SwitchTo,
    SwitchToTab,
)
from screenpy.actions.web.select import SelectByIndex, SelectByText, SelectByValue
from screenpy import Target


class TestAcceptAlert:
    def test_can_be_instantiated(self):
        """AcceptAlert can be instantiated"""
        aa = AcceptAlert()

        assert isinstance(aa, AcceptAlert)


class TestClick:
    def test_can_be_instantiated(self):
        """Click can be instantiated"""
        c1 = Click.on(None)
        c2 = Click.on_the(None)

        assert isinstance(c1, Click)
        assert isinstance(c2, Click)


class TestDebug:
    def test_can_be_instantiated(self):
        """Debug can be instantiated"""
        d = Debug()

        assert isinstance(d, Debug)


class TestDismissAlert:
    def test_can_be_instantiated(self):
        """DismissAlert can be instantiated"""
        da = DismissAlert()

        assert isinstance(da, DismissAlert)


class TestDoubleClick:
    def test_can_be_instantiated(self):
        """DoubleClick can be instantiated"""
        dc1 = DoubleClick()
        dc2 = DoubleClick.on_the(None)

        assert isinstance(dc1, DoubleClick)
        assert isinstance(dc2, DoubleClick)


class TestEnter:
    def test_can_be_instantiated(self):
        """Enter can be instantiated"""
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
        """Enter2FAToken can be instantiated"""
        e1 = Enter2FAToken.into(None)
        e2 = Enter2FAToken.into_the(None)

        assert isinstance(e1, Enter2FAToken)
        assert isinstance(e2, Enter2FAToken)


class TestGoBack:
    def test_can_be_instantiated(self):
        """GoBack can be instantiated"""
        gb = GoBack()

        assert isinstance(gb, GoBack)


class TestGoForward:
    def test_can_be_instantiated(self):
        """GoForward can be instantiated"""
        gf = GoForward()

        assert isinstance(gf, GoForward)


class TestHoldDown:
    def test_can_be_instantiated(self):
        """HoldDown can be instantiated"""
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
        system_path = "screenpy.actions.web.hold_down.platform.system"
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
        """MoveMouse can be instantiated"""
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
        """Open can be instantiated"""
        o1 = Open.browser_on(None)
        o2 = Open.their_browser_on(None)

        assert isinstance(o1, Open)
        assert isinstance(o2, Open)


class TestPause:
    def test_can_be_instantiated(self):
        """Pause can be instantiated"""
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


class TestRelease:
    def test_can_be_instantiated(self):
        """Release can be instantiated"""
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
        system_path = "screenpy.actions.web.hold_down.platform.system"
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
        """RefreshPage can be instantiated"""
        r = RefreshPage()

        assert isinstance(r, RefreshPage)


class TestRespondToThePrompt:
    def test_can_be_instantiated(self):
        """RespondToThePrompt can be instantiated"""
        rttp = RespondToThePrompt.with_("test")

        assert isinstance(rttp, RespondToThePrompt)


class TestRightClick:
    def test_can_be_instantiated(self):
        """RightClick can be instantiated"""
        rc1 = RightClick()
        rc2 = RightClick.on_the(None)

        assert isinstance(rc1, RightClick)
        assert isinstance(rc2, RightClick)


class TestSelect:
    def test_specifics_can_be_instantiated(self):
        """Select's specific classes can be instantiated"""
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


class TestSwitchTo:
    def test_can_be_instantiated(self):
        """SwitchTo can be instantiated"""
        st1 = SwitchTo.the(None)
        st2 = SwitchTo.default()

        assert isinstance(st1, SwitchTo)
        assert isinstance(st2, SwitchTo)


class TestSwitchToTab:
    def test_can_be_instantiated(self):
        """SwitchToTab can be instantiated"""
        stt1 = SwitchToTab(1)
        stt2 = SwitchToTab.on_top()

        assert isinstance(stt1, SwitchToTab)
        assert isinstance(stt2, SwitchToTab)

    def test_description_describes_chosen_tab(self):
        """description is set based on which tab to switch to"""
        stt1 = SwitchToTab(1)
        stt2 = SwitchToTab.on_top()

        assert "tab #1" in stt1.description
        assert "newest tab" in stt2.description
