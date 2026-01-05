from __future__ import annotations

import operator

import pytest
from hamcrest.core.string_description import StringDescription

from screenpy.resolutions.custom_matchers.is_in_bounds import (
    DegenerateIntervalError,
    IsInBounds,
    is_in_bounds,
)
from screenpy.resolutions.custom_matchers.sequence_containing_pattern import (
    IsSequenceContainingPattern,
    has_item_matching,
)


class TestIsInBoundsMatcher:
    def test_describe_to(self) -> None:
        desc = StringDescription()
        iib = IsInBounds(1, operator.le, operator.le, 2)
        iib.describe_to(desc)

        assert desc.out == "the number is within the range of 1 and 2"

    def test_describe_match(self) -> None:
        desc = StringDescription()
        iib = IsInBounds(1, operator.le, operator.le, 4)
        iib.describe_match(2, desc)

        assert desc.out == "2 was within the range of 1 and 4"

    def test_describe_mismatch(self) -> None:
        desc = StringDescription()
        iib = IsInBounds(1, operator.le, operator.le, 4)
        iib.describe_mismatch(5, desc)

        assert desc.out == "5 does not fall within the range of 1 and 4"

    def test_matches(self) -> None:
        iib = IsInBounds(1, operator.le, operator.lt, 4)
        assert iib._matches(0) is False
        assert iib._matches(1) is True
        assert iib._matches(3) is True
        assert iib._matches(4) is False
        assert iib._matches(5) is False


class TestIsInBoundsFunction:
    @staticmethod
    def matches(i1: IsInBounds, i2: IsInBounds) -> None:
        """check if the two IsInBounds matchers are identical"""
        assert i1.minorant == i2.minorant
        assert i1.lower_comparator == i2.lower_comparator
        assert i1.upper_comparator == i2.upper_comparator
        assert i1.majorant == i2.majorant

    def test_returns_instance(self) -> None:
        i1 = is_in_bounds(1, 4)
        assert isinstance(i1, IsInBounds)

    def test_int(self) -> None:
        i1 = is_in_bounds(1, 4)
        i2 = IsInBounds(1.0, operator.le, operator.le, 4.0)

        self.matches(i1, i2)

    def test_negatives(self) -> None:
        i1 = is_in_bounds(-4, -1)
        i2 = IsInBounds(-4.0, operator.le, operator.le, -1.0)

        self.matches(i1, i2)

    def test_str_int(self) -> None:
        i1 = is_in_bounds("[1, 4)")
        i2 = IsInBounds(1.0, operator.le, operator.lt, 4.0)

        self.matches(i1, i2)

    def test_str_float(self) -> None:
        i1 = IsInBounds(1.0, operator.lt, operator.le, 4.0)
        i2 = is_in_bounds("(1.0,4.0]")
        i3 = is_in_bounds("(1., 4.]")

        i4 = IsInBounds(0.1, operator.le, operator.lt, 0.5)
        i5 = is_in_bounds("[.1, .5)")

        self.matches(i1, i2)
        self.matches(i1, i3)
        self.matches(i4, i5)

    def test_str_separator(self) -> None:
        i1 = IsInBounds(1.0, operator.lt, operator.le, 4.0)
        i2 = is_in_bounds("(1.0-4.0]")

        self.matches(i1, i2)

    def test_bad_params(self) -> None:
        with pytest.raises(
            ValueError, match=r"bounding string did not match correct pattern."
        ):
            is_in_bounds("(1.1.1.1, 4.0]")

        with pytest.raises(
            ValueError, match=r"bounding string did not match correct pattern."
        ):
            is_in_bounds("(1.1, 4.4.4.4]")

        with pytest.raises(
            ValueError, match=r"bounding string did not match correct pattern"
        ):
            is_in_bounds("(ab.cd, 1]")

        with pytest.raises(
            TypeError, match=r"is_in_bounds takes either a range string or two numbers."
        ):
            is_in_bounds(1, 2, 3)

        with pytest.raises(DegenerateIntervalError):
            is_in_bounds(2, 1)

        with pytest.raises(DegenerateIntervalError):
            is_in_bounds("[1--4]")


class TestIsSequenceContainingPatternMatcher:
    def test_describe_to(self) -> None:
        desc = StringDescription()
        isp = IsSequenceContainingPattern(r"\t.*")
        isp.describe_to(desc)

        assert desc.out == "a sequence containing an element which matches r'\\t.*'"

    def test_describe_match(self) -> None:
        desc = StringDescription()
        isp = IsSequenceContainingPattern(r"\t.*")
        isp.describe_match([], desc)

        assert desc.out == "it contains an item matching r'\\t.*'"

    def test_describe_mismatch(self) -> None:
        desc = StringDescription()
        isp = IsSequenceContainingPattern(r"\t.*")
        isp.describe_mismatch("asdf", desc)

        assert desc.out == "did not contain an item matching r'\\t.*'"

    def test_describe_mismatch_non_sequence(self) -> None:
        desc = StringDescription()
        isp = IsSequenceContainingPattern(r".*")
        isp.describe_mismatch(None, desc)  # type: ignore[arg-type]

        assert desc.out == "was not a sequence"

    def test_matches(self) -> None:
        isp = IsSequenceContainingPattern(r".*")
        assert isp._matches("asdf") is True

    def test_matches_exception(self) -> None:
        isp = IsSequenceContainingPattern(r".*")
        assert isp._matches(None) is False  # type: ignore[arg-type]


class TestHasItemMatchingFunction:
    def test_returns_instance(self) -> None:
        him = has_item_matching(r".*")
        assert isinstance(him, IsSequenceContainingPattern)
