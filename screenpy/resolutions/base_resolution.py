"""
Resolutions provide the expected answers to Questions. All Resolutions
are given the expected value when instantiated. For example:

    ReadsExactly("the expected text")

The Resolution will then be passed in to an Actor's test method, along
with a Question to get the actual value. An assertion might look like:

    Perry.should(
        See.the(Text.of(THE_WELCOME_MESSAGE), ReadsExactly("Welcome!")),
    )
"""

from typing import Any, Callable, TypeVar

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
    matcher_function: Callable
    expected: Any
    line = (
        "-- I'm sorry, this Resolution did not provide a line. Please define a more "
        "descriptive line for this custom Resolution such that it completes the "
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
        """Get the line that describes this Resolution."""
        return self.line.format(expectation=str(self.expected))

    @property
    def motivation(self) -> str:
        """Used to provide fancy logging for the allure report."""
        return self.get_line()

    def __init__(self, *args: object, **kwargs: object) -> None:
        cls = self.__class__
        if args and kwargs:
            self.expected = (args, kwargs)
            self.matcher = cls.matcher_function(*args, **kwargs)
        elif args:
            self.expected = args if len(args) > 1 else args[0]
            self.matcher = cls.matcher_function(*args)
        elif kwargs:
            self.expected = kwargs
            self.matcher = cls.matcher_function(**kwargs)
        else:
            self.expected = True
            self.matcher = cls.matcher_function()

    def __repr__(self) -> str:
        return self.get_line()
