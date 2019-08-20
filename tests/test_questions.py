from unittest import TestCase

from screenpy.questions import List, Number, Selected, Text


class TestList(TestCase):
    def test_can_be_instantiated(self):
        """List can be instantiated"""
        l1 = List.of(None)
        l2 = List.of_all(None)

        self.assertIsInstance(l1, List)
        self.assertIsInstance(l2, List)


class TestNumber(TestCase):
    def test_can_be_instantiated(self):
        """Number can be instantiated"""
        n1 = Number.of(None)

        self.assertIsInstance(n1, Number)


class TestSelected(TestCase):
    def test_can_be_instantiated(self):
        """Selected can be instantiated"""
        s1 = Selected.option_from(None)
        s2 = Selected.option_from_the(None)
        s3 = Selected.options_from(None)
        s4 = Selected.options_from_the(None)

        self.assertIsInstance(s1, Selected)
        self.assertIsInstance(s2, Selected)
        self.assertIsInstance(s3, Selected)
        self.assertIsInstance(s4, Selected)

    def test_options_from_sets_multi(self):
        """Selected.options_from sets multi to True"""
        multi_selected = Selected.options_from(None)

        self.assertTrue(multi_selected.multi)


class TestText(TestCase):
    def test_can_be_instantiated(self):
        """Text can be instantiated"""
        t1 = Text.of(None)
        t2 = Text.of_all(None)

        self.assertIsInstance(t1, Text)
        self.assertIsInstance(t2, Text)

    def test_of_all_sets_multi(self):
        """Text.of_all sets multi to True"""
        multi_text = Text.of_all(None)

        self.assertTrue(multi_text.multi)
