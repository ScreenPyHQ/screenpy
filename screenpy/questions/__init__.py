"""
Questions are asked by Actors to determine the current state of the
application under test. Ask your actors to ask questions by passing the
questions into their |Actor.should_see_the| or |Actor.should_see_that|
methods, with the resolutions that will assert the correct answer.

These form the first half of test assertions in Screenplay Pattern; the
second half is handled by Resolutions.
"""


from .base_question import BaseQuestion
from .list import List
from .number import Number
from .selected import Selected
from .text import Text

# Natural-language-enabling syntactic sugar
TheList = List
TheNumber = Number
TheSelected = Selected
TheText = Text


__all__ = [
    "BaseQuestion",
    "List",
    "Number",
    "Selected",
    "Text",
    "TheList",
    "TheNumber",
    "TheSelected",
    "TheText",
]
