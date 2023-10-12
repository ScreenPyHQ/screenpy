"""The base class for Resolutions.

***
This approach to Resolutions is deprecated; please use the Resolvable protocol
to implement your own custom Resolutions.
***

Resolutions provide the expected answers to Questions. All Resolutions
are given the expected value when instantiated. For example:

    ReadsExactly("the expected text")

The Resolution will then be passed in to an Actor's test method, along
with a Question to get the actual value. An assertion might look like:

    Perry.should(
        See.the(Text.of(THE_WELCOME_MESSAGE), ReadsExactly("Welcome!")),
    )
"""

import warnings
from typing import Any, Callable, TypeVar

from hamcrest.core.base_matcher import BaseMatcher, Matcher
from hamcrest.core.description import Description

from ..pacing import beat

T = TypeVar("T")


class BaseResolution(BaseMatcher[T]):
    """Base class for Resolutions, ScreenPy's "expected value".

    An abstraction barrier for PyHamcrest's matchers. Allows for natural
    language assertions and hooks into ScreenPy's logging framework.

    You probably shouldn't expect to call any of the defined methods on
    this class or any inherited classes. Just pass an instantiated
    Resolution to your Actor, they'll know what to do with it.
    """

    matcher: Matcher
    matcher_function: Callable
    expected: Any
    line = (
        "-- I'm sorry, this Resolution did not provide a line. Please define a more "
        "descriptive line for this custom Resolution such that it completes the "
        'phrase: "hoping it\'s...".'
    )

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return self.get_line().capitalize()

    def resolve(self) -> BaseMatcher[T]:
        """Produce the Matcher to make the assertion."""
        return self

    @beat("... hoping it's {motivation}")
    def _matches(self, item: T) -> bool:
        """Passthrough to the matcher's method."""
        return self.matcher.matches(item)

    def describe_to(self, description: Description) -> None:
        """Passthrough to the matcher's method."""
        return self.matcher.describe_to(description)

    def describe_match(self, item: T, match_description: Description) -> None:
        """Passthrough to the matcher's method."""
        self.matcher.describe_match(item, match_description)

    def describe_mismatch(self, item: T, mismatch_description: Description) -> None:
        """Passthrough to the matcher's method."""
        self.matcher.describe_mismatch(item, mismatch_description)

    def get_line(self) -> str:
        """Get the line that describes this Resolution."""
        return self.line.format(expectation=str(self.expected))

    @property
    def motivation(self) -> str:
        """Used to provide fancy logging for the allure report."""
        return self.get_line()

    def __init__(self, *args: object, **kwargs: object) -> None:
        warnings.warn(
            "BaseResolution is deprecated and will be removed in ScreenPy v5.0.0."
            " Please make your Resolution Resolvable instead."
            "\nSee https://screenpy-docs.readthedocs.io/en/latest/deprecations.html",
            DeprecationWarning,
            stacklevel=2,
        )
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
        """Represent the Resolution using its line."""
        return self.get_line()
