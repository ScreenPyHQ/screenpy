"""
A grab-bag of useful language-massaging functions with broad applicability.
"""

import re
from typing import Union

from screenpy.protocols import Answerable, Any, Performable


def get_additive_description(describable: Union[Performable, Answerable, Any]) -> str:
    """Extract a description that can be placed within a sentence.

    The ``describe`` method of Performables and Answerables will provide a
    description in present tense, capitalized and with punctuation at the end.
    Lower that case, remove that punctuation; bam! You can stick that in the
    middle of a different sentence.

    If there is no ``describe`` method, try to create a description using the
    class name by replacing each capital letter with a space and a lower-case
    letter (e.g. "BuildItAndTheyWillCome" -> "build it and they will come").

    If the describable does not appear to be an Answerable or Performable,
    stick a "the" in front of the class name. This should make it read like
    "the list" or "the str".
    """
    if hasattr(describable, "describe"):
        description = describable.describe()  # type: ignore # see PEP 544
        description = description[0].lower() + description[1:]
        description = re.sub(r"[.,?!;:]*$", r"", description)
    elif hasattr(describable, "perform_as") or hasattr(describable, "answered_by"):
        # No describe method, so fabricate a description from the class name.
        description = describable.__class__.__name__
        description = re.sub(r"(?<!^)([A-Z])", r" \1", description).lower()
    else:
        # Neither describable nor Answerable/Performable, must be a value.
        description = f"the {describable.__class__.__name__}"

    return description
