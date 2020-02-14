from unittest import mock

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from screenpy import Target
from screenpy.abilities import BrowseTheWeb
from screenpy.actions import Clear, Click, Debug, Enter, Open, Pause, Select, Wait
from screenpy.exceptions import UnableToActError


def test_clear(Tester):
    """Clear action finds its target and calls .clear()"""
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)

    Tester.attempts_to(Clear.the_text_from(fake_target))

    mocked_ability = Tester.ability_to(BrowseTheWeb)
    mocked_ability.to_find.assert_called_once_with((By.XPATH, fake_xpath))
    mocked_ability.to_find.return_value.clear.assert_called_once()


def test_click(Tester):
    """Click action finds its target and calls .click()"""
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)

    Tester.attempts_to(Click.on_the(fake_target))

    mocked_ability = Tester.ability_to(BrowseTheWeb)
    mocked_ability.to_find.assert_called_once_with((By.XPATH, fake_xpath))
    mocked_ability.to_find.return_value.click.assert_called_once()


@mock.patch("screenpy.actions.debug.breakpoint")
def test_debug(mocked_breakpoint, Tester):
    """Debug calls breakpoint()"""
    Tester.attempts_to(Debug())

    mocked_breakpoint.assert_called_once()


@mock.patch("screenpy.actions.debug.breakpoint")
@mock.patch("screenpy.actions.debug.pdb")
def test_debug_falls_back_to_pdb(mocked_pdb, mocked_breakpoint, Tester):
    """Debug calls breakpoint()"""
    mocked_breakpoint.side_effect = NameError("name 'breakpoint' is not defined")

    Tester.attempts_to(Debug())

    mocked_pdb.set_trace.assert_called_once()


def test_enter(Tester):
    """Enter action finds its target and calls .send_keys()"""
    text = "test"
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)

    Tester.attempts_to(Enter.the_text(text).into_the(fake_target))

    mocked_ability = Tester.ability_to(BrowseTheWeb)
    mocked_ability.to_find.assert_called_once_with((By.XPATH, fake_xpath))
    mocked_ability.to_find.return_value.send_keys.assert_called_once_with(text)


def test_enter_following_keys(Tester):
    """Enter action hits the following keys"""
    text = "test"
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)

    Tester.attempts_to(Enter.the_text(text).into_the(fake_target).then_hit(Keys.ENTER))

    mocked_ability = Tester.ability_to(BrowseTheWeb)
    mocked_ability.to_find.assert_called_once_with((By.XPATH, fake_xpath))
    mocked_element = mocked_ability.to_find.return_value
    assert mocked_element.send_keys.call_count == 2
    called_args, _ = mocked_element.send_keys.call_args_list[1]
    assert Keys.ENTER in called_args


def test_enter_complains_for_no_target(Tester):
    """Enter complains if no target was given"""
    with pytest.raises(UnableToActError):
        Tester.attempts_to(Enter.the_text("test"))


def test_open(Tester):
    """Open action calls .get()"""
    url = "https://localtest.test"

    Tester.attempts_to(Open.their_browser_on(url))

    mocked_ability = Tester.ability_to(BrowseTheWeb)
    mocked_ability.to_visit.assert_called_once_with(url)


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


@mock.patch("screenpy.actions.select.SeleniumSelect")
def test_select_by_index(mocked_selenium_select, Tester):
    """SelectByIndex action finds its target and calls .select_by_index()"""
    index = 1
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)

    Tester.attempts_to(Select.the_option_at_index(index).from_the(fake_target))

    mocked_ability = Tester.ability_to(BrowseTheWeb)
    mocked_ability.to_find.assert_called_once_with((By.XPATH, fake_xpath))
    mocked_selenium_select.return_value.select_by_index.assert_called_once_with(
        str(index)
    )


def test_select_by_index_complains_for_no_target(Tester):
    """SelectByIndex complains if no target was given"""
    with pytest.raises(UnableToActError):
        Tester.attempts_to(Select.the_option_at_index(1))


@mock.patch("screenpy.actions.select.SeleniumSelect")
def test_select_by_text(mocked_selenium_select, Tester):
    """SelectByText action finds its target and calls .select_by_visible_text()"""
    text = "test"
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)

    Tester.attempts_to(Select.the_option_named(text).from_the(fake_target))

    mocked_ability = Tester.ability_to(BrowseTheWeb)
    mocked_ability.to_find.assert_called_once_with((By.XPATH, fake_xpath))
    mocked_selenium_select.return_value.select_by_visible_text.assert_called_once_with(
        text
    )


def test_select_by_text_complains_for_no_target(Tester):
    """SelectByText complains if no target was given"""
    with pytest.raises(UnableToActError):
        Tester.attempts_to(Select.the_option_named("text"))


@mock.patch("screenpy.actions.select.SeleniumSelect")
def test_select_by_value(mocked_selenium_select, Tester):
    """SelectByValue action finds its target and calls .select_by_visible_text()"""
    value = 1337
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)

    Tester.attempts_to(Select.the_option_with_value(value).from_the(fake_target))

    mocked_ability = Tester.ability_to(BrowseTheWeb)
    mocked_ability.to_find.assert_called_once_with((By.XPATH, fake_xpath))
    mocked_selenium_select.return_value.select_by_value.assert_called_once_with(
        str(value)
    )


def test_select_by_value_complains_for_no_target(Tester):
    """SelectByValue complains if no target was given"""
    with pytest.raises(UnableToActError):
        Tester.attempts_to(Select.the_option_with_value("value"))


def test_wait(Tester):
    """Wait calls .to_wait_for()"""
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)

    Tester.attempts_to(Wait.for_the(fake_target).to_appear())

    mocked_ability = Tester.ability_to(BrowseTheWeb)
    mocked_ability.to_wait_for.assert_called_once_with(
        fake_target, timeout=20, cond=EC.visibility_of_element_located
    )
