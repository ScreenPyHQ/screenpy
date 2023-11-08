"""A matcher that matches a number in a range.

For example:

    assert_that(5, is_in_bounds("5, 10"))
    assert_that(5, is_in_bounds(1, 20))
"""

from __future__ import annotations

import operator
import re
from typing import TYPE_CHECKING

from hamcrest.core.base_matcher import BaseMatcher

if TYPE_CHECKING:
    from typing import Callable

    from hamcrest.core.description import Description

    InequalityFunc = Callable[[float, float], bool]


class IsInBounds(BaseMatcher[float]):
    """Matches a number which is in the given range."""

    def __init__(
        self,
        minorant: float,
        lower_comparator: InequalityFunc,
        upper_comparator: InequalityFunc,
        majorant: float,
    ) -> None:
        self.minorant = minorant
        self.lower_comparator = lower_comparator
        self.upper_comparator = upper_comparator
        self.majorant = majorant

    def _matches(self, item: float) -> bool:
        matches_lower = self.lower_comparator(self.minorant, item)
        matches_upper = self.upper_comparator(item, self.majorant)
        return matches_lower and matches_upper

    def describe_to(self, description: Description) -> None:
        """Describe the passing case."""
        description.append_text(
            f"the number is within the range of {self.minorant} and {self.majorant}"
        )

    def describe_match(self, item: float, match_description: Description) -> None:
        """Describe the match."""
        match_description.append_text(
            f"{item} was within the range of {self.minorant} and {self.majorant}"
        )

    def describe_mismatch(self, item: float, mismatch_description: Description) -> None:
        """Describe the failing case."""
        mismatch_description.append_text(
            f"{item} does not fall within the range of"
            f" {self.minorant} and {self.majorant}"
        )


def is_in_bounds(*bounds: int | (float | str)) -> IsInBounds:
    """Matches a number that falls within the bounds."""
    lower_comparator = operator.le
    upper_comparator = operator.le
    if len(bounds) == 1:
        bounding_string = str(bounds[0])
        pattern = (
            r"^(?P<lower>[\[\(]?)"
            r"(?P<minorant>\d+).*?(?P<majorant>\d+)"
            r"(?P<upper>[\]\)]?)$"
        )
        matched = re.match(pattern, bounding_string)
        if matched is None:
            msg = "bounding string did not match correct pattern."
            raise ValueError(msg)
        if matched.group("lower") == "(":
            lower_comparator = operator.lt
        if matched.group("upper") == ")":
            upper_comparator = operator.lt
        minorant, majorant = map(float, matched.group("minorant", "majorant"))
    elif len(bounds) == 2:  # noqa: PLR2004
        minorant, majorant = map(float, bounds)
    else:
        msg = "is_in_bounds takes either a range string or two numbers."
        raise TypeError(msg)

    return IsInBounds(minorant, lower_comparator, upper_comparator, majorant)
