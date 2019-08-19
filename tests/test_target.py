from unittest import TestCase

from selenium.webdriver.common.by import By

from screenpy import Target


class TestTarget(TestCase):
    def test_can_be_instantiated(self):
        """Target can be instantiated"""
        t1 = Target.the("test")
        t2 = Target.the("test").located_by("test")

        self.assertIsInstance(t1, Target)
        self.assertIsInstance(t2, Target)

    def test_get_locator(self):
        """Target returns the correct locator tuple"""
        css_selector = "#id"
        xpath_locator = '//div[@id="id"]'
        t1 = Target.the("css element").located_by(css_selector)
        t2 = Target.the("xpath element").located_by(xpath_locator)

        self.assertEqual(t1.get_locator(), (By.CSS_SELECTOR, css_selector))
        self.assertEqual(t2.get_locator(), (By.XPATH, xpath_locator))
