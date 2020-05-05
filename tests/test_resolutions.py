import pytest
from unittest import mock

from screenpy.resolutions import (
    BaseResolution,
    ContainsTheText,
    DoesNot,
    Empty,
    Equal,
    IsEqualTo,
    IsNot,
    IsVisible,
    ReadsExactly,
)


class TestBaseAbility:
    def test___init___must_be_overridden(self):
        """__init__ must be overridden by subclasses."""

        class SubclassedResolution(BaseResolution):
            pass

        with pytest.raises(NotImplementedError):
            SubclassedResolution()


class TestContainsTheText:
    def test_can_be_instantiated(self):
        """ContainsTheText can be instantiated"""
        ctt = ContainsTheText("hello")

        assert isinstance(ctt, ContainsTheText)

    def test_the_test(self):
        """ContainsTheText tests what it says on the tin"""
        ctt = ContainsTheText("hello")

        assert ctt.matches("hello world!")
        assert not ctt.matches("goodbye universe.")


class TestEmpty:
    def test_can_be_instantiated(self):
        """Empty can be instantiated"""
        e = Empty()

        assert isinstance(e, Empty)

    def test_the_test(self):
        """Empty tests what it says on the tin"""
        e = Empty()

        assert e.matches([])
        assert not e.matches(["not", "empty"])


class TestIsEqualTo:
    def test_can_be_instantiated(self):
        """IsEqual can be instantiated"""
        ie = IsEqualTo(1)

        assert isinstance(ie, IsEqualTo)

    def test_the_test(self):
        """IsEqual tests what it says on the tin"""
        ie = IsEqualTo(1)

        assert ie.matches(1)
        assert not ie.matches(2)


class TestIsNot:
    def test_can_be_instantiated(self):
        """IsNot can be instantiated"""
        in_ = IsNot(None)

        assert isinstance(in_, IsNot)

    def test_the_test(self):
        """IsNot tests what it says on the tin"""
        in_ = DoesNot(Equal(1))

        assert in_.matches(2)
        assert not in_.matches(1)


class TestIsVisible:
    def test_can_be_instantiated(self):
        """IsVisible can be instantiated"""
        iv = IsVisible()

        assert isinstance(iv, IsVisible)

    def test_the_test(self):
        """IsVisible tests what it says on the tin"""
        mock_visible_element = mock.Mock()
        mock_visible_element.is_displayed.return_value = True
        mock_invisible_element = mock.Mock()
        mock_invisible_element.is_displayed.return_value = False
        iv = IsVisible()

        assert iv.matches(mock_visible_element)
        assert not iv.matches(mock_invisible_element)


class TestReadsExactly:
    def test_can_be_instantiated(self):
        """ReadsExactly can be instantiated"""
        re_ = ReadsExactly("Blah")

        assert isinstance(re_, ReadsExactly)

    def test_the_test(self):
        """ReadsExactly tests what it says on the tin"""
        re_ = ReadsExactly("Blah")

        assert re_.matches("Blah")
        assert not re_.matches("blah")
