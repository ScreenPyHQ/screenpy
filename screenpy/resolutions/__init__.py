"""
Resolutions are asserted by actors to ensure the answer to their Questions
are as they expect. Ask your actors to provide resolutions by passing the
resolutions into their |Actor.should_see_the| or |Actor.should_see_that|
methods, with the questions they are resolving.

These form the second half of test assertions in Screenplay Pattern; the
first half is handled by Questions.
"""

from .base_resolution import BaseResolution
from .contains_the_entry import ContainsTheEntry
from .contains_the_item import ContainsTheItem
from .contains_the_key import ContainsTheKey
from .contains_the_text import ContainsTheText
from .contains_the_value import ContainsTheValue
from .has_length import HasLength
from .is_empty import IsEmpty
from .is_equal_to import IsEqualTo
from .is_not import IsNot
from .is_visible import IsVisible
from .reads_exactly import ReadsExactly

# Natural-language-enabling syntactic sugar
ContainTheEntry = ContainTheEntries = ContainsTheEntries = ContainsTheEntry
ContainTheItem = ContainsTheItem
ContainTheKey = ContainsTheKey
ContainTheText = ContainsTheText
ContainTheValue = ContainsTheValue
DoesNot = DoNot = IsNot
Empty = IsEmpty
IsDisplayed = Displayed = Visible = IsVisible
IsEqual = Equals = Equal = EqualTo = IsEqualTo
ReadExactly = ReadsExactly


__all__ = [
    "BaseResolution",
    "ContainsTheEntries",
    "ContainsTheEntry",
    "ContainsTheItem",
    "ContainsTheKey",
    "ContainsTheText",
    "ContainsTheValue",
    "ContainTheEntries",
    "ContainTheEntry",
    "ContainTheItem",
    "ContainTheKey",
    "ContainTheText",
    "ContainTheValue",
    "Displayed",
    "DoesNot",
    "DoNot",
    "Empty",
    "Equal",
    "Equals",
    "EqualTo",
    "HasLength",
    "IsDisplayed",
    "IsEmpty",
    "IsEqual",
    "IsEqualTo",
    "IsNot",
    "IsVisible",
    "ReadExactly",
    "ReadsExactly",
    "Visible",
]
