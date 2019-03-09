"""
Resolutions provide the expected answers to Questions. All Resolutions
are given the expected value when instantiated. For example:

    ReadsExactly("the expected text")

The Resolution will then be passed in to an actor's test method, along
with a question to get the actual value. An assertion might look like:

    perry.sees_that((TheHeader.text(), ReadsExactly("Welcome!")),)

Resolutions might be the only example of inheritance in the entirety of
ScreenPy. Hm.
"""

from typing import Iterable

from hamcrest import *
from hamcrest.core.matcher import Matcher

from .pacing import beat, MINOR


class Resolution(Matcher):
    """
    An abstraction barrier for :mod:`PyHamcrest`'s matchers. Allows for
    more natural language possibilities as well as nice logging for the
    allure reports.

    You probably shouldn't expect to call any of the defined methods on
    this class or any inherited classes. Just pass an instantiated
    Resolution to your :class:`|Actor|`, they'll know what to do with it.
    """

    @beat("... hoping {motivation}", gravitas=MINOR)
    def matches(self, actual) -> bool:
        """passthrough to the matcher's method."""
        return self.matcher.matches(actual)

    def describe_to(self, description) -> str:
        """passthrough to the matcher's method."""
        return self.matcher.describe_to(description)

    def describe_mismatch(self, item, mismatch_description) -> str:
        """passthrough to the matcher's method."""
        return self.matcher.describe_mismatch(item, mismatch_description)

    @property
    def motivation(self) -> "Resolution":
        """Used to provide fancy logging for the allure report."""
        return self


class ReadsExactly(Resolution):
    """
    Matches a string exactly (e.g. `"screenplay" == "screenplay"`).
    """

    line = "to read '{},' exactly"

    def __init__(self, string: str) -> None:
        self.string = string
        self.matcher = has_string(string)

    def __repr__(self) -> str:
        return self.line.format(self.string)


class ContainsTheText(Resolution):
    """
    Matches a substring (e.g. `"play" in "screenplay"`).
    """

    line = "to have '{}'"

    def __init__(self, substring: str) -> None:
        self.substring = substring
        self.matcher = contains_string(substring)

    def __repr__(self) -> str:
        return self.line.format(self.substring)


class IsEqualTo(Resolution):
    """
    Matches on equality (i.e. `a == b`).
    """

    line = "to find {}"

    def __init__(self, obj: object) -> None:
        self.obj = obj
        self.matcher = equal_to(obj)

    def __repr__(self) -> str:
        return self.line.format(self.obj)


class Empty(Resolution):
    """
    Matches on an empty collection (e.g. `[]`).
    """

    line = "for {} to be empty"

    def __init__(self, collection: Iterable) -> None:
        self.collection = collection
        self.matcher = empty(collection)

    def __repr__(self) -> str:
        return self.line.format(self.collection)


class IsNot(Resolution):
    """
    Matches a negated Resolution (e.g. `not ReadsExactly("yes")`).
    """

    line = "not {}"

    def __init__(self, resolution: "Resolution") -> None:
        self.resolution = resolution
        self.matcher = is_not(resolution)

    def __repr__(self) -> str:
        return self.line.format(self.resolution)


# Natural-language-enabling syntactic sugar
ReadExactly = ReadsExactly
ContainTheText = ContainsTheText
ToBeEmpty = Empty
DoesNot = IsNot
