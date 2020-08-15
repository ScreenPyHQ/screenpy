"""
Questions are asked by Actors to determine the current state of the
application under test. Ask your actors to ask questions by passing the
questions into their |Actor.should_see_the| or |Actor.should_see_that|
methods, with the resolutions that will assert the correct answer.

These form the first half of test assertions in Screenplay Pattern; the
second half is handled by Resolutions.
"""


from .web.browser_title import BrowserTitle
from .web.browser_url import BrowserURL
from .web.element import Element
from .web.list import List
from .web.number import Number
from .web.selected import Selected
from .web.text import Text
from .web.text_of_the_alert import TextOfTheAlert

# Natural-language-enabling syntactic sugar
TheBrowserTitle = BrowserTitle
TheBrowserURL = BrowserURL
TheElement = Element
TheList = List
TheNumber = Number
TheSelected = Selected
TheText = Text
TheTextOfTheAlert = TextOfTheAlert


__all__ = [
    "BrowserTitle",
    "BrowserURL",
    "Element",
    "List",
    "Number",
    "Selected",
    "Text",
    "TextOfTheAlert",
    "TheBrowserTitle",
    "TheBrowserURL",
    "TheElement",
    "TheList",
    "TheNumber",
    "TheSelected",
    "TheText",
    "TheTextOfTheAlert",
]
