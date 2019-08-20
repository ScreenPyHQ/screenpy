from .base_resolution import Resolution
from .contains_the_text import ContainsTheText
from .empty import Empty
from .is_equal_to import IsEqualTo
from .is_not import IsNot
from .reads_exactly import ReadsExactly


# Natural-language-enabling syntactic sugar
ContainTheText = ContainsTheText
DoesNot = DoNot = AreNot = IsNot
IsEqual = Equals = Equal = IsEqualTo
ReadExactly = ReadsExactly
ToBeEmpty = IsEmpty = Empty
