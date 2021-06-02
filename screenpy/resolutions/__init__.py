"""
Resolutions are expected results asserted by Actors, compared against the
answers to their Questions.

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
from .is_clickable import IsClickable
from .is_close_to import IsCloseTo
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
IsEnabled = Enabled = Clickable = IsClickable
IsDisplayed = Displayed = Visible = IsVisible
IsEqual = Equals = Equal = EqualTo = IsEqualTo
ReadExactly = ReadsExactly


__all__ = [
    "BaseResolution",
    "Clickable",
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
    "Enabled",
    "Equal",
    "Equals",
    "EqualTo",
    "HasLength",
    "IsClickable",
    "IsCloseTo",
    "IsDisplayed",
    "IsEmpty",
    "IsEnabled",
    "IsEqual",
    "IsEqualTo",
    "IsNot",
    "IsVisible",
    "ReadExactly",
    "ReadsExactly",
    "Visible",
]
