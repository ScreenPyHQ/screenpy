from unittest import mock

import pytest

from screenpy.resolutions import (
    BaseResolution,
    ContainsTheEntry,
    ContainsTheItem,
    ContainsTheKey,
    ContainsTheText,
    ContainsTheValue,
    DoesNot,
    Empty,
    Equal,
    HasLength,
    IsClickable,
    IsCloseTo,
    IsEqualTo,
    IsNot,
    IsVisible,
    ReadsExactly,
)


class MockResolution(BaseResolution):
    matcher_function = mock.Mock()


class TestBaseResolution:
    @pytest.mark.parametrize(
        "args,kwargs,expected",
        [
            [[], {}, True],
            [[1], {}, 1],
            [[1, 2], {}, (1, 2)],
            [[], {"a": 1}, {"a": 1}],
            [[1], {"a": 1}, ((1,), {"a": 1})],
        ],
    )
    def test_matcher_instantiation(self, args, kwargs, expected):
        """matcher function is properly called."""
        resolution = MockResolution(*args, **kwargs)

        assert resolution.expected == expected
        assert resolution.matcher.called_once_with(*args, **kwargs)


class TestContainsTheEntry:
    def test_can_be_instantiated(self):
        cte_single = ContainsTheEntry(key="value")
        cte_multiple = ContainsTheEntry(key1="value1", key2="value2")

        assert isinstance(cte_single, ContainsTheEntry)
        assert isinstance(cte_multiple, ContainsTheEntry)

    def test_the_test(self):
        """Matches dictionaries containing the entry(/ies)"""
        cte_single = ContainsTheEntry(key="value")
        cte_multiple = ContainsTheEntry(key1="value1", key2="value2")

        assert cte_single.matches({"key": "value"})
        assert cte_single.matches({"key": "value", "play": "Hamlet"})
        assert not cte_single.matches({"play": "Hamlet"})
        assert cte_multiple.matches({"key1": "value1", "key2": "value2"})
        assert cte_multiple.matches(
            {"key1": "value1", "key2": "value2", "play": "Hamlet"}
        )
        assert not cte_multiple.matches({"key1": "value1"})


class TestContainsTheItem:
    def test_can_be_instantiated(self):
        cti = ContainsTheItem(1)

        assert isinstance(cti, ContainsTheItem)

    def test_the_test(self):
        """Matches lists containing the item"""
        cti = ContainsTheItem(1)

        assert cti.matches(range(0, 10))
        assert not cti.matches({0, 3, 5})


class TestContainsTheKey:
    def test_can_be_instantiated(self):
        ctk = ContainsTheKey("key")

        assert isinstance(ctk, ContainsTheKey)

    def test_the_test(self):
        """Matches dictionaries containing the key"""
        ctk = ContainsTheKey("key")

        assert ctk.matches({"key": "value"})
        assert ctk.matches({"key": "value", "play": "Hamlet"})
        assert not ctk.matches({"play": "Hamlet"})


class TestContainsTheText:
    def test_can_be_instantiated(self):
        ctt = ContainsTheText("hello")

        assert isinstance(ctt, ContainsTheText)

    def test_the_test(self):
        """Matches text with the substring"""
        ctt = ContainsTheText("hello")

        assert ctt.matches("hello world!")
        assert not ctt.matches("goodbye universe.")


class TestContainsTheValue:
    def test_can_be_instantiated(self):
        ctv = ContainsTheValue("Value")

        assert isinstance(ctv, ContainsTheValue)

    def test_the_test(self):
        """Matches dictionaries which contain the value"""
        ctv = ContainsTheValue("value")

        assert ctv.matches({"key": "value"})
        assert ctv.matches({"key": "value", "play": "Hamlet"})
        assert not ctv.matches({"play": "Hamlet"})


class TestEmpty:
    def test_can_be_instantiated(self):
        e = Empty()

        assert isinstance(e, Empty)

    def test_the_test(self):
        """Matches against empty collections"""
        e = Empty()

        assert e.matches([])
        assert not e.matches(["not", "empty"])


class TestHasLength:
    def test_can_be_instantiated(self):
        hl = HasLength(5)

        assert isinstance(hl, HasLength)

    def test_the_test(self):
        """Matches lists with the right length"""
        hl = HasLength(5)

        assert hl.matches([1, 2, 3, 4, 5])
        assert not hl.matches([1])


class TestIsClickable:
    def test_can_be_instantiated(self):
        ic = IsClickable()

        assert isinstance(ic, IsClickable)

    def test_the_test(self):
        """Matches elements which are visible"""
        mock_clickable_element = mock.Mock()
        mock_clickable_element.is_displayed.return_value = True
        mock_clickable_element.is_enabled.return_value = True

        mock_unclickable_element = mock.Mock()
        mock_unclickable_element.is_displayed.return_value = True
        mock_unclickable_element.is_enabled.return_value = False

        mock_invisible_element = mock.Mock()
        mock_invisible_element.is_displayed.return_value = False
        mock_invisible_element.is_enabled.return_value = True
        ic = IsClickable()

        assert ic.matches(mock_clickable_element)
        assert not ic.matches(mock_unclickable_element)
        assert not ic.matches(mock_invisible_element)


class TestIsCloseTo:
    def test_can_be_instantiated(self):
        ict = IsCloseTo(1, delta=3)

        assert isinstance(ict, IsCloseTo)

    def test_the_test(self):
        ict = IsCloseTo(1, delta=3)

        assert ict.matches(1)
        assert ict.matches(4)
        assert not ict.matches(5)
        assert not ict.matches(-5)


class TestIsEqualTo:
    def test_can_be_instantiated(self):
        ie = IsEqualTo(1)

        assert isinstance(ie, IsEqualTo)

    def test_the_test(self):
        """Matches objects that are equal to what was passed in"""
        ie = IsEqualTo(1)

        assert ie.matches(1)
        assert not ie.matches(2)


class TestIsNot:
    def test_can_be_instantiated(self):
        in_ = IsNot(None)

        assert isinstance(in_, IsNot)

    def test_the_test(self):
        """Matches the opposite of what was passed in"""
        in_ = DoesNot(Equal(1))

        assert in_.matches(2)
        assert not in_.matches(1)


class TestIsVisible:
    def test_can_be_instantiated(self):
        iv = IsVisible()

        assert isinstance(iv, IsVisible)

    def test_the_test(self):
        """Matches elements which are visible"""
        mock_visible_element = mock.Mock()
        mock_visible_element.is_displayed.return_value = True
        mock_invisible_element = mock.Mock()
        mock_invisible_element.is_displayed.return_value = False
        iv = IsVisible()

        assert iv.matches(mock_visible_element)
        assert not iv.matches(mock_invisible_element)


class TestReadsExactly:
    def test_can_be_instantiated(self):
        re_ = ReadsExactly("Blah")

        assert isinstance(re_, ReadsExactly)

    def test_the_test(self):
        """Matches text exactly"""
        re_ = ReadsExactly("Blah")

        assert re_.matches("Blah")
        assert not re_.matches("blah")
