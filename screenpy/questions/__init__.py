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
from .text_of_the_alert import TextOfTheAlert

# Natural-language-enabling syntactic sugar
TheList = List
TheNumber = Number
TheSelected = Selected
TheText = Text
TheTextOfTheAlert = TextOfTheAlert


__all__ = [
    "BaseQuestion",
    "List",
    "Number",
    "Selected",
    "Text",
    "TextOfTheAlert",
    "TheList",
    "TheNumber",
    "TheSelected",
    "TheText",
    "TheTextOfTheAlert",
]
