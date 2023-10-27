"""A grab-bag of useful language-massaging functions with broad applicability."""

from __future__ import annotations

import re
from typing import TypeVar, overload

from hamcrest.core.helpers.hasmethod import hasmethod
from hamcrest.core.helpers.ismock import ismock

from screenpy.protocols import Answerable, Describable, Performable, Resolvable

T = TypeVar("T")


def get_additive_description(describable: Describable | T) -> str:
    """Extract a description that can be placed within a sentence.

    The ``describe`` method of Describables will provide a description,
    capitalized and with punctuation at the end. Lower that case, remove that
    punctuation; bam! You can stick that in the middle of a new sentence.

    If there is no ``describe`` method, try to create a description using the
    class name: replace each capital letter with a space and a lower-case
    letter (e.g. "BuildItAndTheyWillCome" -> "build it and they will come").

    If the object does not appear to be any -able, stick a "the" in front of
    the class name. This should make it read like "the list" or "the str".

    Args:
        describable: the object to attempt to describe.

    Returns:
        str: the string to place within another string.
    """
    if isinstance(describable, Describable):
        description = describable.describe()
        if description:
            description = description[0].lower() + description[1:]
            description = re.sub(r"[.,?!;:]*$", r"", description)
        else:
            description = "something indescribable"
    elif isinstance(describable, (Answerable, Performable, Resolvable)):
        # No describe method, so fabricate a description from the class name.
        description = describable.__class__.__name__
        description = re.sub(r"(?<!^)([A-Z])", r" \1", description).lower()
    else:
        # Neither Describable nor any other -able, must be a value.
        description = f"the {describable.__class__.__name__}"

    return description


@overload
def represent_prop(item: str) -> str:
    ...


@overload
def represent_prop(item: T) -> T:
    ...


def represent_prop(item: str | T) -> str | T:
    """Represent items in a manner suitable for the audience (logging)."""
    if not ismock(item) and hasmethod(item, "describe_to"):
        return f"{item}"
    if isinstance(item, str):
        return repr(item)

    description = str(item)
    if description[:1] == "<" and description[-1:] == ">":
        return item

    return f"<{item}>"
