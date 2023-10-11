"""The expected answer to a Question.

When combined with a Question, the Question + Resolution pair make up the test
assertions in Screenplay Pattern.
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
from .is_greater_than import IsGreaterThan
from .is_greater_than_or_equal_to import IsGreaterThanOrEqualTo
from .is_in_range import IsInRange
from .is_less_than import IsLessThan
from .is_less_than_or_equal_to import IsLessThanOrEqualTo
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
GreaterThan = IsGreaterThan
GreaterThanOrEqualTo = IsGreaterThanOrEqualTo
InRange = IsInRange
LessThan = IsLessThan
LessThanOrEqualTo = IsLessThanOrEqualTo
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
    "GreaterThan",
    "GreaterThanOrEqualTo",
    "HasLength",
    "InRange",
    "IsCloseTo",
    "IsEmpty",
    "IsEqual",
    "IsEqualTo",
    "IsGreaterThan",
    "IsGreaterThanOrEqualTo",
    "IsInRange",
    "IsLessThan",
    "IsLessThanOrEqualTo",
    "IsNot",
    "LessThan",
    "LessThanOrEqualTo",
    "Match",
    "Matches",
    "ReadExactly",
    "ReadsExactly",
    "StartsWith",
    "StartWith",
]
