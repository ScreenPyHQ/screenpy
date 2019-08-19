from unittest import TestCase

from screenpy.actions.click import Click
from screenpy.actions.enter import Enter, Press
from screenpy.actions.open import Open, Opens
from screenpy.actions.select import Select, SelectByText, SelectByIndex, SelectByValue


class TestClick(TestCase):
    def test_can_be_instantiated(self):
        """Click can be instantiated"""
        c1 = Click.on(None)
        c2 = Click.on_the(None)
        c3 = Click.on_the(None).then_wait_for(None)

        self.assertIsInstance(c1, Click)
        self.assertIsInstance(c2, Click)
        self.assertIsInstance(c3, Click)


class TestEnter(TestCase):
    def test_can_be_instantiated(self):
        """Enter can be instantiated"""
        e1 = Enter.the_text("test")
        e2 = Enter.the_text("test").into(None)
        e3 = Enter.the_keys("test").into(None)
        e4 = Enter.the_text("test").on(None)
        e5 = Enter.the_keys("test").on(None)
        e6 = Enter.the_text("test").into(None).then_press(None)
        e7 = Enter.the_text("test").into(None).then_wait_for(None)
        e8 = Press.the_keys("test")

        self.assertIsInstance(e1, Enter)
        self.assertIsInstance(e2, Enter)
        self.assertIsInstance(e3, Enter)
        self.assertIsInstance(e4, Enter)
        self.assertIsInstance(e5, Enter)
        self.assertIsInstance(e6, Enter)
        self.assertIsInstance(e7, Enter)
        self.assertIsInstance(e8, Enter)


class TestOpen(TestCase):
    def test_can_be_instantiated(self):
        """Open can be instantiated"""
        o1 = Open.browser_on(None)
        o2 = Open.their_browser_on(None)
        o3 = Opens.browser_on(None)

        self.assertIsInstance(o1, Open)
        self.assertIsInstance(o2, Open)
        self.assertIsInstance(o3, Open)


class TestSelect(TestCase):
    def test_specifics_can_be_instantiated(self):
        """Select's specific classes can be instantiated"""
        by_text = Select.the_option_named(None)
        by_index = Select.the_option_at_index(None)
        by_value = Select.the_option_with_value(None)

        self.assertIsInstance(by_text, SelectByText)
        self.assertIsInstance(by_index, SelectByIndex)
        self.assertIsInstance(by_value, SelectByValue)
