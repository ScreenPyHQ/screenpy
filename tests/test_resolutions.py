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
    IsGreaterThan,
    IsGreaterThanOrEqualTo,
    IsInRange,
    IsLessThan,
    IsLessThanOrEqualTo,
    IsNot,
    Matches,
    ReadsExactly,
    StartsWith,
)
from screenpy.resolutions.base_resolution import BaseMatcher


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
        cim = ContainsItemMatching(r"([Ss]pam ?)+").resolve()

        assert cim.matches(["Spam", "Eggs", "Spam and eggs"])
        assert not cim.matches(["Porridge"])


class TestContainsTheEntry:
    def test_can_be_instantiated(self) -> None:
        cte_single = ContainsTheEntry(key="value")
        cte_multiple = ContainsTheEntry(key1="value1", key2="value2")

        assert isinstance(cte_single, ContainsTheEntry)
        assert isinstance(cte_multiple, ContainsTheEntry)

    def test_the_test(self) -> None:
        """Matches dictionaries containing the entry(/ies)"""
        cte_single = ContainsTheEntry(key="value").resolve()
        cte_multiple = ContainsTheEntry(key1="value1", key2="value2").resolve()
        cte_alt2 = ContainsTheEntry({"key2": "something2"}).resolve()
        cte_alt3 = ContainsTheEntry("key3", "something3").resolve()

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


class TestContainsTheItem:
    def test_can_be_instantiated(self) -> None:
        cti = ContainsTheItem(1)

        assert isinstance(cti, ContainsTheItem)

    def test_the_test(self) -> None:
        """Matches lists containing the item"""
        cti = ContainsTheItem(1).resolve()

        assert cti.matches(range(0, 10))
        assert not cti.matches({0, 3, 5})


class TestContainsTheKey:
    def test_can_be_instantiated(self) -> None:
        ctk = ContainsTheKey("key")

        assert isinstance(ctk, ContainsTheKey)

    def test_the_test(self) -> None:
        """Matches dictionaries containing the key"""
        ctk = ContainsTheKey("key").resolve()

        assert ctk.matches({"key": "value"})
        assert ctk.matches({"key": "value", "play": "Hamlet"})
        assert not ctk.matches({"play": "Hamlet"})


class TestContainsTheText:
    def test_can_be_instantiated(self) -> None:
        ctt = ContainsTheText("hello")

        assert isinstance(ctt, ContainsTheText)

    def test_the_test(self) -> None:
        """Matches text with the substring"""
        ctt = ContainsTheText("hello").resolve()

        assert ctt.matches("hello world!")
        assert not ctt.matches("goodbye universe.")


class TestContainsTheValue:
    def test_can_be_instantiated(self) -> None:
        ctv = ContainsTheValue("Value")

        assert isinstance(ctv, ContainsTheValue)

    def test_the_test(self) -> None:
        """Matches dictionaries which contain the value"""
        ctv = ContainsTheValue("value").resolve()

        assert ctv.matches({"key": "value"})
        assert ctv.matches({"key": "value", "play": "Hamlet"})
        assert not ctv.matches({"play": "Hamlet"})


class TestEmpty:
    def test_can_be_instantiated(self) -> None:
        e = IsEmpty()

        assert isinstance(e, IsEmpty)

    def test_the_test(self) -> None:
        """Matches against empty collections"""
        e = IsEmpty().resolve()

        assert e.matches([])
        assert not e.matches(["not", "empty"])


class TestEndsWith:
    def test_can_be_instantiated(self) -> None:
        ew = EndsWith("")

        assert isinstance(ew, EndsWith)

    def test_the_test(self) -> None:
        ew = EndsWith("of life!").resolve()

        assert ew.matches("Bereft of life!")
        assert not ew.matches("He has ceased to be!")


class TestHasLength:
    def test_can_be_instantiated(self) -> None:
        hl = HasLength(5)

        assert isinstance(hl, HasLength)

    def test_the_test(self) -> None:
        """Matches lists with the right length"""
        hl = HasLength(5).resolve()

        assert hl.matches([1, 2, 3, 4, 5])
        assert not hl.matches([1])


class TestIsCloseTo:
    def test_can_be_instantiated(self) -> None:
        ict = IsCloseTo(1, delta=3)

        assert isinstance(ict, IsCloseTo)

    def test_the_test(self) -> None:
        ict = IsCloseTo(1, delta=3).resolve()

        assert ict.matches(1)
        assert ict.matches(4)
        assert not ict.matches(5)
        assert not ict.matches(-5)


class TestIsEqualTo:
    def test_can_be_instantiated(self) -> None:
        ie = IsEqualTo(1)

        assert isinstance(ie, IsEqualTo)

    def test_the_test(self) -> None:
        """Matches objects that are equal to what was passed in"""
        ie = IsEqualTo(1).resolve()

        assert ie.matches(1)
        assert not ie.matches(2)


class TestIsGreaterThan:
    def test_can_be_instantiated(self) -> None:
        igt = IsGreaterThan(1)

        assert isinstance(igt, IsGreaterThan)

    def test_the_test(self) -> None:
        test_num = 5
        igt = IsGreaterThan(test_num).resolve()

        assert igt.matches(test_num + 1)
        assert not igt.matches(test_num)
        assert not igt.matches(test_num - 1)


class TestIsGreaterThanOrEqualTo:
    def test_can_be_instantiated(self) -> None:
        igtoet = IsGreaterThanOrEqualTo(1)

        assert isinstance(igtoet, IsGreaterThanOrEqualTo)

    def test_the_test(self) -> None:
        test_num = 5
        igtoet = IsGreaterThanOrEqualTo(test_num).resolve()

        assert igtoet.matches(test_num + 1)
        assert igtoet.matches(test_num)
        assert not igtoet.matches(test_num - 1)


class TestIsInRange:
    def test_can_be_instantiated(self) -> None:
        iir1 = IsInRange(1, 5)
        iir2 = IsInRange("(1, 5)")

        assert isinstance(iir1, IsInRange)
        assert isinstance(iir2, IsInRange)

    def test_the_test(self) -> None:
        test_minorant = 5
        test_majorant = 10
        iir1 = IsInRange(test_minorant, test_majorant).resolve()
        iir2 = IsInRange(f"[{test_minorant}, {test_majorant}]").resolve()
        iir3 = IsInRange(f"({test_minorant}, {test_majorant})").resolve()
        iir4 = IsInRange(f"[{test_minorant}, {test_majorant})").resolve()

        assert iir1.matches(test_minorant + 1)
        assert iir2.matches(test_minorant + 1)
        assert iir3.matches(test_minorant + 1)
        assert iir4.matches(test_minorant + 1)
        assert iir1.matches(test_majorant - 1)
        assert iir2.matches(test_majorant - 1)
        assert iir3.matches(test_majorant - 1)
        assert iir4.matches(test_majorant - 1)
        assert iir1.matches(test_minorant)
        assert iir2.matches(test_minorant)
        assert not iir3.matches(test_minorant)
        assert iir4.matches(test_minorant)
        assert iir1.matches(test_majorant)
        assert iir2.matches(test_majorant)
        assert not iir3.matches(test_majorant)
        assert not iir4.matches(test_majorant)
        assert not iir1.matches(test_majorant + 1)
        assert not iir2.matches(test_majorant + 1)
        assert not iir3.matches(test_majorant + 1)
        assert not iir4.matches(test_majorant + 1)


class TestIsLessThan:
    def test_can_be_instantiated(self) -> None:
        ilt = IsLessThan(1)

        assert isinstance(ilt, IsLessThan)

    def test_the_test(self) -> None:
        test_num = 5
        ilt = IsLessThan(test_num).resolve()

        assert ilt.matches(test_num - 1)
        assert not ilt.matches(test_num)
        assert not ilt.matches(test_num + 1)


class TestIsLessThanOrEqualTo:
    def test_can_be_instantiated(self) -> None:
        iltoet = IsLessThanOrEqualTo(1)

        assert isinstance(iltoet, IsLessThanOrEqualTo)

    def test_the_test(self) -> None:
        test_num = 5
        iltoet = IsLessThanOrEqualTo(test_num).resolve()

        assert iltoet.matches(test_num - 1)
        assert iltoet.matches(test_num)
        assert not iltoet.matches(test_num + 1)


class TestIsNot:
    def test_can_be_instantiated(self) -> None:
        in_ = IsNot(None)

        assert isinstance(in_, IsNot)

    def test_the_test(self) -> None:
        """Matches the opposite of what was passed in"""
        in_ = DoesNot(Equal(1)).resolve()

        assert in_.matches(2)
        assert not in_.matches(1)


class TestMatches:
    def test_can_be_instantiated(self) -> None:
        m = Matches(r"^$")

        assert isinstance(m, Matches)

    def test_the_test(self) -> None:
        m = Matches(r"([Ss]pam ?)+").resolve()

        assert m.matches("Spam spam spam spam baked beans and spam")
        assert not m.matches("What do you mean Eugh?!")


class TestReadsExactly:
    def test_can_be_instantiated(self) -> None:
        re_ = ReadsExactly("Blah")

        assert isinstance(re_, ReadsExactly)

    def test_the_test(self) -> None:
        """Matches text exactly"""
        re_ = ReadsExactly("Blah").resolve()

        assert re_.matches("Blah")
        assert not re_.matches("blah")


class TestStartsWith:
    def test_can_be_instantiated(self) -> None:
        sw = StartsWith("")

        assert isinstance(sw, StartsWith)

    def test_the_test(self) -> None:
        sw = StartsWith("I will not buy this record").resolve()

        assert sw.matches("I will not buy this record, it is scratched.")
        assert not sw.matches("I will not buy this tobacconist, it is scratched.")
