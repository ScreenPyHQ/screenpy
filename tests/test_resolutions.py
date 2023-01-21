from unittest import mock

import pytest

from screenpy.resolutions import (
    BaseResolution,
    ContainsItemMatching,
    ContainsTheEntry,
    ContainsTheItem,
    ContainsTheKey,
    ContainsTheText,
    ContainsTheValue,
    DoesNot,
    EndsWith,
    Equal,
    HasLength,
    IsCloseTo,
    IsEmpty,
    IsEqualTo,
    IsNot,
    Matches,
    ReadsExactly,
)
from screenpy.resolutions.base_resolution import BaseMatcher


def assert_matcher_annotation(obj: BaseResolution) -> None:
    assert type(obj.matcher) is obj.__annotations__["matcher"]


class TestBaseResolution:
    @pytest.mark.parametrize(
        "args,kwargs,expected",
        [
            ([], {}, True),
            ([1], {}, 1),
            ([1, 2], {}, (1, 2)),
            ([], {"a": 1}, {"a": 1}),
            ([1], {"a": 1}, ((1,), {"a": 1})),
        ],
    )
    def test_matcher_instantiation(self, args, kwargs, expected) -> None:
        """matcher function is properly called."""

        class MockResolution(BaseResolution):
            """Must be defined here for new mock matchers."""

            matcher_function = mock.create_autospec(BaseMatcher)

        resolution = MockResolution(*args, **kwargs)

        assert resolution.expected == expected
        resolution.matcher_function.assert_called_once_with(*args, **kwargs)

    @pytest.mark.parametrize(
        "method,args,expected_method",
        [
            ("_matches", [mock.create_autospec(BaseResolution._matches)], "matches"),
            (
                "describe_to",
                [mock.create_autospec(BaseResolution.describe_to)],
                "describe_to",
            ),
            (
                "describe_match",
                [mock.create_autospec(BaseResolution.describe_match), mock.Mock()],
                "describe_match",
            ),
            (
                "describe_mismatch",
                [mock.create_autospec(BaseResolution.describe_mismatch), mock.Mock()],
                "describe_mismatch",
            ),
        ],
    )
    def test_passthroughs(self, method, args, expected_method) -> None:
        class MockResolution(BaseResolution):
            """Must be defined here for new mock matchers."""

            matcher_function = mock.create_autospec(BaseMatcher)

        resolution = MockResolution()

        getattr(resolution, method)(*args)

        getattr(resolution.matcher, expected_method).assert_called_once_with(*args)

    def test___repr__(self) -> None:
        class MockResolution(BaseResolution):
            """Must be defined here for new mock matchers."""

            matcher_function = mock.create_autospec(BaseMatcher)
            get_line = mock.create_autospec(BaseResolution.get_line, return_value="")

        resolution = MockResolution()

        repr(resolution)

        resolution.get_line.assert_called_once()


class TestContainsItemMatching:
    def test_can_be_instantiated(self) -> None:
        cim = ContainsItemMatching(r"^$")

        assert isinstance(cim, ContainsItemMatching)

    def test_the_test(self) -> None:
        cim = ContainsItemMatching(r"([Ss]pam ?)+")

        assert cim.matches(["Spam", "Eggs", "Spam and eggs"])
        assert not cim.matches(["Porridge"])

    def test_type_hint(self) -> None:
        assert_matcher_annotation(ContainsItemMatching(r"^$"))


class TestContainsTheEntry:
    def test_can_be_instantiated(self) -> None:
        cte_single = ContainsTheEntry(key="value")
        cte_multiple = ContainsTheEntry(key1="value1", key2="value2")

        assert isinstance(cte_single, ContainsTheEntry)
        assert isinstance(cte_multiple, ContainsTheEntry)

    def test_the_test(self) -> None:
        """Matches dictionaries containing the entry(/ies)"""
        cte_single = ContainsTheEntry(key="value")
        cte_multiple = ContainsTheEntry(key1="value1", key2="value2")
        cte_alt2 = ContainsTheEntry({"key2": "something2"})
        cte_alt3 = ContainsTheEntry("key3", "something3")

        assert cte_alt2.matches({"key2": "something2"})
        assert cte_alt3.matches({"key3": "something3"})
        assert cte_single.matches({"key": "value"})
        assert cte_single.matches({"key": "value", "play": "Hamlet"})
        assert not cte_single.matches({"play": "Hamlet"})
        assert cte_multiple.matches({"key1": "value1", "key2": "value2"})
        assert cte_multiple.matches(
            {"key1": "value1", "key2": "value2", "play": "Hamlet"}
        )
        assert not cte_multiple.matches({"key1": "value1"})

    def test_type_hint(self) -> None:
        assert_matcher_annotation(ContainsTheEntry(key2="hi"))


class TestContainsTheItem:
    def test_can_be_instantiated(self) -> None:
        cti = ContainsTheItem(1)

        assert isinstance(cti, ContainsTheItem)

    def test_the_test(self) -> None:
        """Matches lists containing the item"""
        cti = ContainsTheItem(1)

        assert cti.matches(range(0, 10))
        assert not cti.matches({0, 3, 5})

    def test_type_hint(self) -> None:
        assert_matcher_annotation(ContainsTheItem(1))


class TestContainsTheKey:
    def test_can_be_instantiated(self) -> None:
        ctk = ContainsTheKey("key")

        assert isinstance(ctk, ContainsTheKey)

    def test_the_test(self) -> None:
        """Matches dictionaries containing the key"""
        ctk = ContainsTheKey("key")

        assert ctk.matches({"key": "value"})
        assert ctk.matches({"key": "value", "play": "Hamlet"})
        assert not ctk.matches({"play": "Hamlet"})

    def test_type_hint(self) -> None:
        assert_matcher_annotation(ContainsTheKey(1))


class TestContainsTheText:
    def test_can_be_instantiated(self) -> None:
        ctt = ContainsTheText("hello")

        assert isinstance(ctt, ContainsTheText)

    def test_the_test(self) -> None:
        """Matches text with the substring"""
        ctt = ContainsTheText("hello")

        assert ctt.matches("hello world!")
        assert not ctt.matches("goodbye universe.")

    def test_type_hint(self) -> None:
        assert_matcher_annotation(ContainsTheText("hello"))


class TestContainsTheValue:
    def test_can_be_instantiated(self) -> None:
        ctv = ContainsTheValue("Value")

        assert isinstance(ctv, ContainsTheValue)

    def test_the_test(self) -> None:
        """Matches dictionaries which contain the value"""
        ctv = ContainsTheValue("value")

        assert ctv.matches({"key": "value"})
        assert ctv.matches({"key": "value", "play": "Hamlet"})
        assert not ctv.matches({"play": "Hamlet"})

    def test_type_hint(self) -> None:
        assert_matcher_annotation(ContainsTheValue(1))


class TestEmpty:
    def test_can_be_instantiated(self) -> None:
        e = IsEmpty()

        assert isinstance(e, IsEmpty)

    def test_the_test(self) -> None:
        """Matches against empty collections"""
        e = IsEmpty()

        assert e.matches([])
        assert not e.matches(["not", "empty"])

    def test_type_hint(self) -> None:
        assert_matcher_annotation(IsEmpty())


class TestEndsWith:
    def test_can_be_instantiated(self) -> None:
        ew = EndsWith("")

        assert isinstance(ew, EndsWith)

    def test_the_test(self) -> None:
        ew = EndsWith("of life!")

        assert ew.matches("Bereft of life!")
        assert not ew.matches("He has ceased to be!")

    def test_type_hint(self) -> None:
        assert_matcher_annotation(EndsWith(""))


class TestHasLength:
    def test_can_be_instantiated(self) -> None:
        hl = HasLength(5)

        assert isinstance(hl, HasLength)

    def test_the_test(self) -> None:
        """Matches lists with the right length"""
        hl = HasLength(5)

        assert hl.matches([1, 2, 3, 4, 5])
        assert not hl.matches([1])

    def test_type_hint(self) -> None:
        assert_matcher_annotation(HasLength(1))


class TestIsCloseTo:
    def test_can_be_instantiated(self) -> None:
        ict = IsCloseTo(1, delta=3)

        assert isinstance(ict, IsCloseTo)

    def test_the_test(self) -> None:
        ict = IsCloseTo(1, delta=3)

        assert ict.matches(1)
        assert ict.matches(4)
        assert not ict.matches(5)
        assert not ict.matches(-5)

    def test_get_line(self) -> None:
        num = 1
        delta = 3

        ict = IsCloseTo(num, delta=delta)

        assert ict.get_line() == f"a value at most {delta} away from {num}."

    def test_type_hint(self) -> None:
        assert_matcher_annotation(IsCloseTo(2))


class TestIsEqualTo:
    def test_can_be_instantiated(self) -> None:
        ie = IsEqualTo(1)

        assert isinstance(ie, IsEqualTo)

    def test_the_test(self) -> None:
        """Matches objects that are equal to what was passed in"""
        ie = IsEqualTo(1)

        assert ie.matches(1)
        assert not ie.matches(2)

    def test_type_hint(self) -> None:
        assert_matcher_annotation(IsEqualTo(1))


class TestIsNot:
    def test_can_be_instantiated(self) -> None:
        in_ = IsNot(None)

        assert isinstance(in_, IsNot)

    def test_the_test(self) -> None:
        """Matches the opposite of what was passed in"""
        in_ = DoesNot(Equal(1))

        assert in_.matches(2)
        assert not in_.matches(1)

    def test_type_hint(self) -> None:
        assert_matcher_annotation(IsNot(1))


class TestMatches:
    def test_can_be_instantiated(self) -> None:
        m = Matches(r"^$")

        assert isinstance(m, Matches)

    def test_the_test(self) -> None:
        m = Matches(r"([Ss]pam ?)+")

        assert m.matches("Spam spam spam spam baked beans and spam")
        assert not m.matches("What do you mean Eugh?!")

    def test_type_hint(self) -> None:
        assert_matcher_annotation(Matches(r"^$"))


class TestReadsExactly:
    def test_can_be_instantiated(self) -> None:
        re_ = ReadsExactly("Blah")

        assert isinstance(re_, ReadsExactly)

    def test_the_test(self) -> None:
        """Matches text exactly"""
        re_ = ReadsExactly("Blah")

        assert re_.matches("Blah")
        assert not re_.matches("blah")

    def test_type_hint(self) -> None:
        assert_matcher_annotation(ReadsExactly("hi"))
