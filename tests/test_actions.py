from unittest import TestCase

from screenpy.actions import Click, Enter, Open, Opens, Press, Select
from screenpy.actions.select import SelectByIndex, SelectByText, SelectByValue


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
        e4 = Enter.the_text("test").into_the(None)
        e5 = Enter.the_text("test").on(None)
        e6 = Enter.the_keys("test").on(None)
        e7 = Enter.the_text("test").into(None).then_press(None)
        e8 = Enter.the_text("test").into(None).then_wait_for(None)
        e9 = Press.the_keys("test")

        self.assertIsInstance(e1, Enter)
        self.assertIsInstance(e2, Enter)
        self.assertIsInstance(e3, Enter)
        self.assertIsInstance(e4, Enter)
        self.assertIsInstance(e5, Enter)
        self.assertIsInstance(e6, Enter)
        self.assertIsInstance(e7, Enter)
        self.assertIsInstance(e8, Enter)
        self.assertIsInstance(e9, Enter)


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
        by_index1 = Select.the_option_at_index(0)
        by_index2 = Select.the_option_at_index(0).from_(None)
        by_index3 = Select.the_option_at_index(0).from_the(None)
        by_text1 = Select.the_option_named("Option")
        by_text2 = Select.the_option_named("Option").from_(None)
        by_text3 = Select.the_option_named("Option").from_the(None)
        by_value1 = Select.the_option_with_value(1)
        by_value2 = Select.the_option_with_value(1).from_(None)
        by_value3 = Select.the_option_with_value(1).from_the(None)

        self.assertIsInstance(by_index1, SelectByIndex)
        self.assertIsInstance(by_index2, SelectByIndex)
        self.assertIsInstance(by_index3, SelectByIndex)
        self.assertIsInstance(by_text1, SelectByText)
        self.assertIsInstance(by_text2, SelectByText)
        self.assertIsInstance(by_text3, SelectByText)
        self.assertIsInstance(by_value1, SelectByValue)
        self.assertIsInstance(by_value2, SelectByValue)
        self.assertIsInstance(by_value3, SelectByValue)
