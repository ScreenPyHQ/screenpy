"""
Resolutions provide the expected answers to Questions. All Resolutions
are given the expected value when instantiated. For example:

    ReadsExactly("the expected text")

The Resolution will then be passed in to an actor's test method, along
with a question to get the actual value. An assertion might look like:

    Perry.should_see_the(
        (Text.of(THE_WELCOME_MESSAGE), ReadsExactly("Welcome!")),
    )
"""

from typing import TypeVar

from hamcrest.core.base_matcher import BaseMatcher, Matcher
from hamcrest.core.description import Description

from ..pacing import beat

T = TypeVar("T")


class BaseResolution(BaseMatcher[T]):
    """
    An abstraction barrier for |PyHamcrest|'s matchers. Allows for
    more natural language possibilities as well as nice logging for the
    allure reports.

    You probably shouldn't expect to call any of the defined methods on
    this class or any inherited classes. Just pass an instantiated
    Resolution to your |Actor|, they'll know what to do with it.
    """

    matcher: Matcher
    expected: object
    line = (
        "-- I'm sorry, this resolution did not provide a line. Please define a more "
        "descriptive line for this custom resolution such that it completes the "
        'phrase: "hoping it\'s...".'
    )

    @beat("... hoping it's {motivation}")
    def _matches(self, item: object) -> bool:
        """passthrough to the matcher's method."""
        return self.matcher.matches(item)

    def describe_to(self, description: Description) -> None:
        """passthrough to the matcher's method."""
        return self.matcher.describe_to(description)

    def describe_mismatch(
        self, item: object, mismatch_description: Description
    ) -> None:
        """passthrough to the matcher's method."""
        self.matcher.describe_mismatch(item, mismatch_description)

    def get_line(self) -> str:
        """Get the line that describes this resolution."""
        return self.line.format(expectation=self.expected)

    @property
    def motivation(self) -> str:
        """Used to provide fancy logging for the allure report."""
        return self.get_line()

    def __init__(self) -> None:
        raise NotImplementedError(
            "Resolutions must implement their own __init__ method. Please implement "
            f"this method for the custom '{self.__class__.__name__}' Resolution."
        )

    def __repr__(self) -> str:
        return self.get_line()
