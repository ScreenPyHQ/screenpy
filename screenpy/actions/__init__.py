"""
Actions are what the Actors do, possibly requiring use of their Abilities.
"""

from .attach_the_file import AttachTheFile
from .debug import Debug
from .eventually import Eventually
from .make_note import MakeNote
from .pause import Pause
from .see import See
from .see_all_of import SeeAllOf
from .see_any_of import SeeAnyOf

# Natural-language-enabling syntactic sugar
AttachFile = AttachAFile = AttachTheFile
Observe = Verify = Confirm = Assert = See
ObserveAllOf = VerifyAllOf = ConfirmAllOf = AssertAllOf = SeeAllOf
ObserveAnyOf = VerifyAnyOf = ConfirmAnyOf = AssertAnyOf = SeeAnyOf
Sleep = Pause
TakeNote = MakeNote


__all__ = [
    "Assert",
    "AssertAllOf",
    "AssertAnyOf",
    "AttachAFile",
    "AttachFile",
    "AttachTheFile",
    "Confirm",
    "ConfirmAllOf",
    "ConfirmAnyOf",
    "Debug",
    "Eventually",
    "Observe",
    "ObserveAllOf",
    "ObserveAnyOf",
    "Pause",
    "See",
    "SeeAllOf",
    "SeeAnyOf",
    "Sleep",
    "Verify",
    "VerifyAllOf",
    "VerifyAnyOf",
]
