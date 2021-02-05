"""
A custom PyHamcrest matcher that will match against objects that have a given
method that when called with the provided arguments and keyword arguments will
produce the expected return value. For example:

    assert_that(
        dict(("a", 1)), has_method_with_return_value("get", args=["a"], 1)
    )
"""


from typing import Any, Iterable, Mapping, Optional, Union

from hamcrest.core import not_none
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher as wrap_shortcut
from hamcrest.core.matcher import Matcher
from hamcrest.core.string_description import StringDescription


class IsObjectWithCallableProducingValue(BaseMatcher[object]):
    """
    Match against an object that has a return value produced by calling the
    specified method with the provided arguments and keyword arguments.
    """

    def __init__(
        self,
        method_name: str,
        value_matcher: Matcher[Any],
        args: Iterable[Any] = None,
        kwargs: Mapping[str, Any] = None,
    ) -> None:
        self.method_name = method_name
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.value_matcher = value_matcher
        self.retval = None

    def get_callargs_str(self) -> str:
        """Produce a string showing the structure of the called method."""
        args_str = ", ".join(map(str, self.args)) if self.args else ""

        kwargs_str = ""
        if self.kwargs:
            kwargs_bits = map(
                lambda x: "=".join(map(str, x)),
                sorted(self.kwargs.items(), key=lambda x: x[0]),
            )
            kwargs_str = ", ".join(kwargs_bits)

        if args_str and kwargs_str:
            kwargs_str = f", {kwargs_str}"

        return f"({args_str}{kwargs_str})"

    def get_return_value(self, item: object) -> Any:
        """
        Call the method with the provided arguments and keyword arguments,
        returning whatever that call produces.

        Args:
            item: the object in which to find the method.

        Returns:
            Whatever the item's method returns.
        """
        self.retval = getattr(item, self.method_name)(*self.args, **self.kwargs)
        return self.retval

    def _matches(self, item: object) -> bool:
        if item is None:
            return False

        if not hasattr(item, self.method_name):
            return False

        return_value = self.get_return_value(item)
        return self.value_matcher.matches(return_value)

    def describe_to(self, description: Description) -> None:
        """
        Describe this matcher to the passed in description.

        Args:
            description: the description that is being built.
        """
        description.append_text("an object with a method '").append_text(
            self.method_name
        ).append_text("' whose return value when called with ").append_text(
            self.get_callargs_str()
        ).append_text(
            " matches "
        ).append_description_of(
            self.value_matcher
        )

    def describe_mismatch(
        self, item: object, mismatch_description: Description
    ) -> None:
        """
        Describe the mismatch to the passed-in description.

        Args:
            item: the object that was tested.
            mismatch_description: the description that is being built.
        """
        if item is None:
            mismatch_description.append_text("was None")
            return

        if not hasattr(item, self.method_name):
            mismatch_description.append_description_of(item).append_text(
                " did not have a "
            ).append_description_of(self.method_name).append_text(" method")
            return

        mismatch_description.append_text("method ").append_description_of(
            self.method_name
        ).append_text(" called with ").append_text(self.get_callargs_str()).append_text(
            " "
        )

        self.value_matcher.describe_mismatch(self.retval, mismatch_description)

    def __str__(self) -> str:
        d = StringDescription()
        self.describe_to(d)
        return str(d)


def has_method_with_return_value(
    name: str,
    args: Iterable[Any] = None,
    kwargs: Mapping[str, Any] = None,
    match: Optional[Union[Matcher[Any], Any]] = None,
) -> Matcher[object]:
    """
    Match against an object which has a method with the given name that, when
    called with the given args and kwargs, returns the expected value.

    Examples::

        assert_that(
            list(1, 2, 3), has_method_with_return_value("copy", [1, 2, 3])
        )
        assert_that(
            dict((a, "Hello, world!")),
            has_method_with_return_value(
                "get", args=["a"], contains_string("world")
            )
        )

    Args:
        name: the name of the method to call.
        args: the list of args to provide when calling.
        kwargs: a dictionary of kwargs to pass when calling.
        match: the expected value of calling the method.
    """
    if match is None:
        match = not_none()

    return IsObjectWithCallableProducingValue(
        name, wrap_shortcut(match), args=args, kwargs=kwargs
    )
