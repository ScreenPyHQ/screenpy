"""
Resolutions are asserted by actors to ensure the answer to their Questions
are as they expect. Ask your actors to provide resolutions by passing the
resolutions into their |Actor.should_see_the| or |Actor.should_see_that|
methods, with the questions they are resolving.

These form the second half of test assertions in Screenplay Pattern; the
first half is handled by Questions.
"""


from .base_resolution import BaseResolution
from .contains_the_text import ContainsTheText
from .is_empty import IsEmpty
from .is_equal_to import IsEqualTo
from .is_not import IsNot
from .reads_exactly import ReadsExactly

# Natural-language-enabling syntactic sugar
ContainTheText = ContainsTheText
DoesNot = DoNot = AreNot = IsNot
IsEqual = Equals = Equal = IsEqualTo
ReadExactly = ReadsExactly
ToBeEmpty = Empty = IsEmpty


__all__ = [
    "AreNot",
    "BaseResolution",
    "ContainsTheText",
    "ContainTheText",
    "DoesNot",
    "DoNot",
    "Empty",
    "Equal",
    "Equals",
    "IsEmpty",
    "IsEqual",
    "IsEqualTo",
    "IsNot",
    "ReadExactly",
    "ReadsExactly",
    "ToBeEmpty",
]
