import pytest
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from screenpy.abilities import BrowseTheWeb
from screenpy.target import Target, TargetingError


def test_can_be_instantiated():
    t1 = Target.the("test")
    t2 = Target.the("test").located_by("test")

    assert isinstance(t1, Target)
    assert isinstance(t2, Target)


def test_complains_for_no_locator():
    """Raises if no locator was supplied."""
    target = Target.the("test")

    with pytest.raises(TargetingError):
        target.get_locator()


def test_get_locator():
    """Returns the locator tuple when asked for it"""
    css_selector = "#id"
    xpath_locator = '//div[@id="id"]'
    xpath_locator_2 = "(//a)[5]"
    css_target = Target.the("css element").located_by(css_selector)
    xpath_target = Target.the("xpath element").located_by(xpath_locator)
    xpath_target_2 = Target.the("xpath element 2").located_by(xpath_locator_2)

    assert css_target.get_locator() == (By.CSS_SELECTOR, css_selector)
    assert xpath_target.get_locator() == (By.XPATH, xpath_locator)
    assert xpath_target_2.get_locator() == (By.XPATH, xpath_locator_2)


def test_located():
    """Uses the provided locator tuple, unaltered"""
    locator = (By.ID, "spam")
    target = Target.the("test").located(locator)

    assert target.get_locator() == locator


def test_can_be_indexed():
    locator = (By.ID, "eggs")
    target = Target.the("test").located(locator)

    assert target[0] == locator[0]
    assert target[1] == locator[1]


def test_found_by(Tester):
    test_locator = (By.ID, "eggs")
    Target.the("test").located(test_locator).found_by(Tester)

    mocked_browser = Tester.ability_to(BrowseTheWeb).browser
    mocked_browser.find_element.assert_called_once_with(*test_locator)


def test_found_by_raises(Tester):
    test_name = "frobnosticator"
    mocked_browser = Tester.ability_to(BrowseTheWeb).browser
    mocked_browser.find_element.side_effect = WebDriverException

    with pytest.raises(TargetingError) as excinfo:
        Target.the(test_name).located_by("*").found_by(Tester)

    assert test_name in str(excinfo.value)


def test_all_found_by(Tester):
    test_locator = (By.ID, "baked beans")
    Target.the("test").located(test_locator).all_found_by(Tester)

    mocked_browser = Tester.ability_to(BrowseTheWeb).browser
    mocked_browser.find_elements.assert_called_once_with(*test_locator)


def test_all_found_by_raises(Tester):
    test_name = "transmogrifier"
    mocked_browser = Tester.ability_to(BrowseTheWeb).browser
    mocked_browser.find_elements.side_effect = WebDriverException

    with pytest.raises(TargetingError) as excinfo:
        Target.the(test_name).located_by("*").all_found_by(Tester)

    assert test_name in str(excinfo.value)
