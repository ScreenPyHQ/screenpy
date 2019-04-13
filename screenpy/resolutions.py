"""
Resolutions provide the expected answers to Questions. All Resolutions
are given the expected value when instantiated. For example:

    ReadsExactly("the expected text")

The Resolution will then be passed in to an actor's test method, along
with a question to get the actual value. An assertion might look like:

    perry.should_see_the((Text.of(THE_WELCOME_MESSAGE), ReadsExactly("Welcome!")),)

Resolutions might be the only example of inheritance in the entirety of
ScreenPy. Hm.
"""

from typing import Iterable

from hamcrest import *
from hamcrest.core.matcher import Matcher

from .pacing import beat, MINOR


class Resolution(Matcher):
    """
    An abstraction barrier for |PyHamcrest|'s matchers. Allows for
    more natural language possibilities as well as nice logging for the
    allure reports.

    You probably shouldn't expect to call any of the defined methods on
    this class or any inherited classes. Just pass an instantiated
    Resolution to your |Actor|, they'll know what to do with it.
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

    def __repr__(self) -> str:
        return self.line.format(self.expected)


class ReadsExactly(Resolution):
    """
    Matches a string exactly (e.g. `"screenplay" == "screenplay"`).
    """

    line = "to read '{},' exactly"

    def __init__(self, string: str) -> None:
        self.expected = string
        self.matcher = has_string(string)


class ContainsTheText(Resolution):
    """
    Matches a substring (e.g. `"play" in "screenplay"`).
    """

    line = "to have '{}'"

    def __init__(self, substring: str) -> None:
        self.expected = substring
        self.matcher = contains_string(substring)


class IsEqualTo(Resolution):
    """
    Matches on equality (i.e. `a == b`).
    """

    line = "to find {}"

    def __init__(self, obj: object) -> None:
        self.expected = obj
        self.matcher = equal_to(obj)


class Empty(Resolution):
    """
    Matches on an empty collection (e.g. `[]`).
    """

    line = "for {} to be empty"

    def __init__(self, collection: Iterable) -> None:
        self.expected = collection
        self.matcher = empty(collection)


class IsNot(Resolution):
    """
    Matches a negated Resolution (e.g. `not ReadsExactly("yes")`).
    """

    line = "not {}"

    def __init__(self, resolution: "Resolution") -> None:
        self.expected = resolution
        self.matcher = is_not(resolution)


# Natural-language-enabling syntactic sugar
ReadExactly = ReadsExactly
ContainTheText = ContainsTheText
ToBeEmpty = IsEmpty = Empty
DoesNot = IsNot
