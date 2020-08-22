"""
Questions are asked by Actors to determine the current state of the
application under test. Ask your actors to ask questions by passing the
questions into their |Actor.should_see_the| or |Actor.should_see_that|
methods, with the resolutions that will assert the correct answer.

These form the first half of test assertions in Screenplay Pattern; the
second half is handled by Resolutions.
"""


from .body_of_the_last_response import BodyOfTheLastResponse
from .browser_title import BrowserTitle
from .browser_url import BrowserURL
from .cookies import Cookies, CookiesOnTheAPISession, CookiesOnTheWebSession
from .element import Element
from .headers_of_the_last_response import HeadersOfTheLastResponse
from .list import List
from .number import Number
from .selected import Selected
from .status_code_of_the_last_response import StatusCodeOfTheLastResponse
from .text import Text
from .text_of_the_alert import TextOfTheAlert

# Natural-language-enabling syntactic sugar
TheBodyOfTheLastResponse = BodyOfTheLastResponse
TheBrowserTitle = BrowserTitle
TheCookies = Cookies
TheCookiesOnTheAPISession = CookiesOnTheAPISession
TheCookiesOnTheWebSession = CookiesOnTheWebSession
TheBrowserURL = BrowserURL
TheElement = Element
TheHeadersOfTheLastResponse = HeadersOfTheLastResponse
TheList = List
TheNumber = Number
TheSelected = Selected
TheStatusCodeOfTheLastResponse = StatusCodeOfTheLastResponse
TheText = Text
TheTextOfTheAlert = TextOfTheAlert


__all__ = [
    "BodyOfTheLastResponse",
    "BrowserTitle",
    "BrowserURL",
    "Cookies",
    "CookiesOnTheAPISession",
    "CookiesOnTheWebSession",
    "Element",
    "HeadersOfTheLastResponse",
    "List",
    "Number",
    "Selected",
    "StatusCodeOfTheLastResponse",
    "Text",
    "TextOfTheAlert",
    "TheBodyOfTheLastResponse",
    "TheBrowserTitle",
    "TheBrowserURL",
    "TheCookies",
    "TheCookiesOnTheAPISession",
    "TheCookiesOnTheWebSession",
    "TheElement",
    "TheHeadersOfTheLastResponse",
    "TheList",
    "TheNumber",
    "TheSelected",
    "TheStatusCodeOfTheLastResponse",
    "TheText",
    "TheTextOfTheAlert",
]
