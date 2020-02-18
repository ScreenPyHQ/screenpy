import pytest

from screenpy.actions import (
    AcceptAlert,
    BaseAction,
    Click,
    Debug,
    DismissAlert,
    Enter,
    Enter2FAToken,
    Open,
    Opens,
    Pause,
    Press,
    RespondToThePrompt,
    Select,
    SwitchTo,
)
from screenpy.actions.select import SelectByIndex, SelectByText, SelectByValue


class TestBaseAction:
    def test_perform_as_must_be_overridden(self):
        """perform_as must be overridden in subclasses"""

        class SubclassedAction(BaseAction):
            pass

        subclassed_action = SubclassedAction()

        with pytest.raises(NotImplementedError):
            subclassed_action.perform_as(None)


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


class TestEnter2FAToken:
    def test_can_be_instantiated(self):
        """Enter2FAToken can be instantiated"""
        e1 = Enter2FAToken.into(None)
        e2 = Enter2FAToken.into_the(None)

        assert isinstance(e1, Enter2FAToken)
        assert isinstance(e2, Enter2FAToken)


class TestOpen:
    def test_can_be_instantiated(self):
        """Open can be instantiated"""
        o1 = Open.browser_on(None)
        o2 = Open.their_browser_on(None)
        o3 = Opens.browser_on(None)

        assert isinstance(o1, Open)
        assert isinstance(o2, Open)
        assert isinstance(o3, Open)


class TestPause:
    def test_can_be_instantiated(self):
        """Pause can be instantiated."""
        p1 = Pause.for_(20)
        p2 = Pause.for_(20).seconds_because("test")
        p3 = Pause.for_(20).milliseconds_because("test")

        assert isinstance(p1, Pause)
        assert isinstance(p2, Pause)
        assert isinstance(p3, Pause)

    def test_seconds(self):
        """Choosing seconds stores the correct time."""
        duration = 20
        pause = Pause.for_(duration).seconds_because("test")

        assert pause.time == duration

    def test_milliseconds(self):
        """Choosing milliseconds stores the correct time."""
        duration = 20
        pause = Pause.for_(duration).milliseconds_because("Test")

        assert pause.time == duration / 1000.0


class TestRespondToThePrompt:
    def test_can_be_instantiated(self):
        """RespondToThePrompt can be instantiated"""
        rttp = RespondToThePrompt.with_("test")

        assert isinstance(rttp, RespondToThePrompt)


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
