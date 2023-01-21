"""
Resolutions are expected results asserted by Actors, compared against the
answers to their Questions.

These form the second half of test assertions in Screenplay Pattern; the
first half is handled by Questions.
"""

from .base_resolution import BaseResolution
from .contains_item_matching import ContainsItemMatching
from .contains_the_entry import ContainsTheEntry
from .contains_the_item import ContainsTheItem
from .contains_the_key import ContainsTheKey
from .contains_the_text import ContainsTheText
from .contains_the_value import ContainsTheValue
from .ends_with import EndsWith
from .has_length import HasLength
from .is_close_to import IsCloseTo
from .is_empty import IsEmpty
from .is_equal_to import IsEqualTo
from .is_not import IsNot
from .matches import Matches
from .reads_exactly import ReadsExactly
from .starts_with import StartsWith

# Natural-language-enabling syntactic sugar
CloseTo = IsCloseTo
ContainItemMatching = ContainsItemMatching
ContainTheEntry = ContainTheEntries = ContainsTheEntries = ContainsTheEntry
ContainTheItem = ContainsTheItem
ContainTheKey = ContainsTheKey
ContainTheText = ContainsTheText
ContainTheValue = ContainsTheValue
DoesNot = DoNot = IsNot
Empty = IsEmpty
EndWith = EndsWith
HaveLength = HasLength
IsEqual = Equals = Equal = EqualTo = IsEqualTo
Match = Matches
ReadExactly = ReadsExactly
StartWith = StartsWith


__all__ = [
    "BaseResolution",
    "ContainItemMatching",
    "ContainsItemMatching",
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
    "DoesNot",
    "DoNot",
    "Empty",
    "EndsWith",
    "EndWith",
    "Equal",
    "Equals",
    "EqualTo",
    "HasLength",
    "IsCloseTo",
    "IsEmpty",
    "IsEqual",
    "IsEqualTo",
    "IsNot",
    "Match",
    "Matches",
    "ReadExactly",
    "ReadsExactly",
    "StartsWith",
    "StartWith",
]
