from unittest import mock

import pytest

from screenpy import (
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
    EqualTo,
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
from screenpy.speech_tools import get_additive_description


class TestBaseResolution:
    def test_subclasses_deprecated(self):
        class MockResolution(BaseResolution):
            """Must be defined here for new mock matchers."""

            matcher_function = mock.create_autospec(BaseMatcher)

        with pytest.deprecated_call():
            MockResolution()

    @pytest.mark.filterwarnings("ignore:BaseResolution")
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

    @pytest.mark.filterwarnings("ignore:BaseResolution")
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

    @pytest.mark.filterwarnings("ignore:BaseResolution")
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

    def test_description(self) -> None:
        test_pattern = r".*"

        cim = ContainsItemMatching(test_pattern)

        expected_description = (
            'A sequence with an item matching the pattern r".*".'
        )
        assert cim.describe() == expected_description


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
        cte_alt2 = ContainsTheEntry({"key2": 12345}).resolve()
        cte_alt3 = ContainsTheEntry("key3", "something3").resolve()

        assert cte_alt2.matches({"key2": 12345})
        assert cte_alt3.matches({"key3": "something3"})
        assert cte_single.matches({"key": "value"})
        assert cte_single.matches({"key": "value", "play": "Hamlet"})
        assert not cte_single.matches({"play": "Hamlet"})
        assert cte_multiple.matches({"key1": "value1", "key2": "value2"})
        assert cte_multiple.matches(
            {"key1": "value1", "key2": "value2", "play": "Hamlet"}
        )
        assert not cte_multiple.matches({"key1": "value1"})

    def test_description(self) -> None:
        test_entry = {"spam": "eggs"}
        test_entries = {"number": 1234, "spam": "eggs"}

        cte_single = ContainsTheEntry(**test_entry)
        cte_multiple = ContainsTheEntry(**test_entries)

        expected_description_single = "A mapping with the entry 'spam'->'eggs'."
        expected_description_multiple = (
            "A mapping with the entries 'number'->1234, 'spam'->'eggs'."
        )
        assert cte_single.describe() == expected_description_single
        assert cte_multiple.describe() == expected_description_multiple


class TestContainsTheItem:
    def test_can_be_instantiated(self) -> None:
        cti = ContainsTheItem(1)

        assert isinstance(cti, ContainsTheItem)

    def test_the_test(self) -> None:
        """Matches lists containing the item"""
        cti = ContainsTheItem(1).resolve()

        assert cti.matches(range(0, 10))
        assert not cti.matches({0, 3, 5})

    def test_description(self) -> None:
        test_item = 1

        cti = ContainsTheItem(test_item)

        expected_description = "A sequence containing 1."
        assert cti.describe() == expected_description

    def test_description_str(self) -> None:
        test_item = "1"

        cti = ContainsTheItem(test_item)

        expected_description = "A sequence containing '1'."
        assert cti.describe() == expected_description


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

    def test_description(self) -> None:
        test_key = "spam"

        ctk = ContainsTheKey(test_key)

        expected_description = "Containing the key 'spam'."
        assert ctk.describe() == expected_description


class TestContainsTheText:
    def test_can_be_instantiated(self) -> None:
        ctt = ContainsTheText("hello")

        assert isinstance(ctt, ContainsTheText)

    def test_the_test(self) -> None:
        """Matches text with the substring"""
        ctt = ContainsTheText("hello").resolve()

        assert ctt.matches("hello world!")
        assert not ctt.matches("goodbye universe.")

    def test_description(self) -> None:
        test_text = "Wenn ist das Nunstück git und Slotermeyer?"

        ctt = ContainsTheText(test_text)

        expected_description = "Containing the text 'Wenn ist das Nunstück git und Slotermeyer?'."
        assert ctt.describe() == expected_description


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

    def test_description(self) -> None:
        test_value = 42

        ctv = ContainsTheValue(test_value)

        expected_description = "Containing the value 42."
        assert ctv.describe() == expected_description

    def test_description_str(self) -> None:
        test_value = "42"

        ctv = ContainsTheValue(test_value)

        expected_description = "Containing the value '42'."
        assert ctv.describe() == expected_description


class TestEmpty:
    def test_can_be_instantiated(self) -> None:
        e = IsEmpty()

        assert isinstance(e, IsEmpty)

    def test_the_test(self) -> None:
        """Matches against empty collections"""
        e = IsEmpty().resolve()

        assert e.matches([])
        assert not e.matches(["not", "empty"])

    def test_description(self) -> None:
        e = IsEmpty()

        assert e.describe() == "An empty collection."


class TestEndsWith:
    def test_can_be_instantiated(self) -> None:
        ew = EndsWith("")

        assert isinstance(ew, EndsWith)

    def test_the_test(self) -> None:
        ew = EndsWith("of life!").resolve()

        assert ew.matches("Bereft of life!")
        assert not ew.matches("He has ceased to be!")

    def test_description(self) -> None:
        test_postfix = "got better."

        ew = EndsWith(test_postfix)

        expected_description = "Ending with 'got better.'."
        assert ew.describe() == expected_description


class TestHasLength:
    def test_can_be_instantiated(self) -> None:
        hl = HasLength(5)

        assert isinstance(hl, HasLength)

    def test_the_test(self) -> None:
        """Matches lists with the right length"""
        hl = HasLength(5).resolve()

        assert hl.matches([1, 2, 3, 4, 5])
        assert not hl.matches([1])

    def test_description(self) -> None:
        test_length = 5

        hl1 = HasLength(1)
        hl5 = HasLength(test_length)

        expected_description1 = "1 item long."
        expected_description5 = "5 items long."
        assert hl1.describe() == expected_description1
        assert hl5.describe() == expected_description5


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

    def test_description(self) -> None:
        test_delta = 42
        test_num = 1337

        ict = IsCloseTo(test_num, delta=test_delta)

        expected_description = f"At most {test_delta} away from {test_num}."
        assert ict.describe() == expected_description


class TestIsEqualTo:
    def test_can_be_instantiated(self) -> None:
        ie = IsEqualTo(1)

        assert isinstance(ie, IsEqualTo)

    def test_the_test(self) -> None:
        """Matches objects that are equal to what was passed in"""
        ie = IsEqualTo(1).resolve()

        assert ie.matches(1)
        assert not ie.matches(2)

    def test_description(self) -> None:
        test_object = "my Schwartz"

        ie = IsEqualTo(test_object)

        expected_description = f"Equal to {test_object}."
        assert ie.describe() == expected_description


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

    def test_description(self) -> None:
        test_num = 41

        igt = IsGreaterThan(test_num)

        expected_description = f"Greater than {test_num}."
        assert igt.describe() == expected_description


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

    def test_description(self) -> None:
        test_num = 1337

        igtoet = IsGreaterThanOrEqualTo(test_num)

        expected_description = f"Greater than or equal to {test_num}."
        assert igtoet.describe() == expected_description


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

    def test_description(self) -> None:
        test_minorant = 42
        test_majorant = 1337
        test_bounding_string = "(100, 300)"

        iir_nums = IsInRange(test_minorant, test_majorant)
        iir_str = IsInRange(test_bounding_string)

        expected_description_nums = f"In the range [{test_minorant}, {test_majorant}]."
        expected_description_str = f"In the range {test_bounding_string}."
        assert iir_nums.describe() == expected_description_nums
        assert iir_str.describe() == expected_description_str


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

    def test_description(self) -> None:
        test_num = 43

        ilt = IsLessThan(test_num)

        expected_description = f"Less than {test_num}."
        assert ilt.describe() == expected_description


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

    def test_description(self) -> None:
        test_num = 1337

        iltoet = IsLessThanOrEqualTo(test_num)

        expected_description = f"Less than or equal to {test_num}."
        assert iltoet.describe() == expected_description


class TestIsNot:
    def test_can_be_instantiated(self) -> None:
        in_ = IsNot(EqualTo(True))

        assert isinstance(in_, IsNot)

    def test_the_test(self) -> None:
        """Matches the opposite of what was passed in"""
        in_ = DoesNot(Equal(1)).resolve()

        assert in_.matches(2)
        assert not in_.matches(1)

    def test_description(self) -> None:
        test_resolution = IsEqualTo(5)

        in_ = IsNot(test_resolution)

        expected_description = f"Not {get_additive_description(test_resolution)}."
        assert in_.describe() == expected_description


class TestMatches:
    def test_can_be_instantiated(self) -> None:
        m = Matches(r"^$")

        assert isinstance(m, Matches)

    def test_the_test(self) -> None:
        m = Matches(r"([Ss]pam ?)+").resolve()

        assert m.matches("Spam spam spam spam baked beans and spam")
        assert not m.matches("What do you mean Eugh?!")

    def test_description(self) -> None:
        test_match = r"(spam)+"

        m = Matches(test_match)

        expected_description = 'Text matching the pattern r"(spam)+".'
        assert m.describe() == expected_description


class TestReadsExactly:
    def test_can_be_instantiated(self) -> None:
        re_ = ReadsExactly("Blah")

        assert isinstance(re_, ReadsExactly)

    def test_the_test(self) -> None:
        """Matches text exactly"""
        re_ = ReadsExactly("Blah").resolve()

        assert re_.matches("Blah")
        assert not re_.matches("blah")

    def test_description(self) -> None:
        test_text = "I will not buy this record, it is scratched."

        re_ = ReadsExactly(test_text)

        expected_description = "'I will not buy this record, it is scratched.', verbatim."
        assert re_.describe() == expected_description


class TestStartsWith:
    def test_can_be_instantiated(self) -> None:
        sw = StartsWith("")

        assert isinstance(sw, StartsWith)

    def test_the_test(self) -> None:
        sw = StartsWith("I will not buy this record").resolve()

        assert sw.matches("I will not buy this record, it is scratched.")
        assert not sw.matches("I will not buy this tobacconist, it is scratched.")

    def test_description(self) -> None:
        test_prefix = "It was the best of times,"

        sw = StartsWith(test_prefix)

        expected_description = "Starting with 'It was the best of times,'."
        assert sw.describe() == expected_description
