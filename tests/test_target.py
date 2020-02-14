import pytest
from selenium.webdriver.common.by import By

from screenpy.target import Target, TargetingError


def test_can_be_instantiated():
    """Target can be instantiated"""
    t1 = Target.the("test")
    t2 = Target.the("test").located_by("test")

    assert isinstance(t1, Target)
    assert isinstance(t2, Target)


def test_complains_for_no_locator():
    """Target will complain if no locator was supplied."""
    target = Target.the("test")

    with pytest.raises(TargetingError):
        target.get_locator()


def test_get_locator():
    """Target returns the correct locator tuple"""
    css_selector = "#id"
    xpath_locator = '//div[@id="id"]'
    css_target = Target.the("css element").located_by(css_selector)
    xpath_target = Target.the("xpath element").located_by(xpath_locator)

    assert css_target.get_locator() == (By.CSS_SELECTOR, css_selector)
    assert xpath_target.get_locator() == (By.XPATH, xpath_locator)


def test_located():
    """Target accepts the locator provided by a user"""
    locator = (By.ID, "spam")
    target = Target.the("test").located(locator)

    assert target.get_locator() == locator
