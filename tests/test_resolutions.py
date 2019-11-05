from unittest import TestCase

from screenpy.resolutions import (
    ContainsTheText,
    Empty,
    IsEqualTo,
    Equal,
    IsNot,
    DoesNot,
    ReadsExactly,
)


class TestContainsTheText(TestCase):
    def test_can_be_instantiated(self):
        """ContainsTheText can be instantiated"""
        ctt = ContainsTheText("hello")

        self.assertIsInstance(ctt, ContainsTheText)

    def test_the_test(self):
        """ContainsTheText tests what it says on the tin"""
        ctt = ContainsTheText("hello")

        self.assertTrue(ctt.matches("hello world!"))
        self.assertFalse(ctt.matches("goodbye universe."))


class TestEmpty(TestCase):
    def test_can_be_instantiated(self):
        """Empty can be instantiated"""
        e = Empty()

        self.assertIsInstance(e, Empty)

    def test_the_test(self):
        """Empty tests what it says on the tin"""
        e = Empty()

        self.assertTrue(e.matches([]))
        self.assertFalse(e.matches(["not", "empty"]))


class TestIsEqualTo(TestCase):
    def test_can_be_instantiated(self):
        """IsEqual can be instantiated"""
        ie = IsEqualTo(1)

        self.assertIsInstance(ie, IsEqualTo)

    def test_the_test(self):
        """IsEqual tests what it says on the tin"""
        ie = IsEqualTo(1)

        self.assertTrue(ie.matches(1))
        self.assertFalse(ie.matches(2))


class TestIsNot(TestCase):
    def test_can_be_instantiated(self):
        """IsNot can be instantiated"""
        in_ = IsNot(None)

        self.assertIsInstance(in_, IsNot)

    def test_the_test(self):
        """IsNot tests what it says on the tin"""
        in_ = DoesNot(Equal(1))

        self.assertTrue(in_.matches(2))
        self.assertFalse(in_.matches(1))


class TestReadsExactly(TestCase):
    def test_can_be_instantiated(self):
        """ReadsExactly can be instantiated"""
        re_ = ReadsExactly("Blah")

        self.assertIsInstance(re_, ReadsExactly)

    def test_the_test(self):
        """ReadsExactly tests what it says on the tin"""
        re_ = ReadsExactly("Blah")

        self.assertTrue(re_.matches("Blah"))
        self.assertFalse(re_.matches("blah"))
