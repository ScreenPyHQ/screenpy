"""
Actions are what the Actors do, possibly requiring use of their Abilities.
"""

from .attach_the_file import AttachTheFile
from .debug import Debug
from .eventually import Eventually
from .log import Log
from .make_note import MakeNote
from .pause import Pause
from .see import See
from .see_all_of import SeeAllOf
from .see_any_of import SeeAnyOf
from .silently import Silently

# Natural-language-enabling syntactic sugar
AttachFile = AttachAFile = AttachTheFile
AttachesFile = AttachesAFile = AttachesTheFile = AttachTheFile
Observe = Verify = Confirm = Assert = See
Observes = Verifies = Confirms = Asserts = Sees = See
ObserveAllOf = VerifyAllOf = ConfirmAllOf = AssertAllOf = SeeAllOf
ObservesAllOf = VerifiesAllOf = ConfirmsAllOf = AssertsAllOf = SeesAllOf = SeeAllOf
ObserveAnyOf = VerifyAnyOf = ConfirmAnyOf = AssertAnyOf = SeeAnyOf
ObservesAnyOf = VerifiesAnyOf = ConfirmsAnyOf = AssertsAnyOf = SeesAnyOf = SeeAnyOf
Quietly = Silently
Sleep = Pause
Sleeps = Pauses = Pause
TakeNote = MakeNote
TakesNote = MakesNote = MakeNote


__all__ = [
    "Assert",
    "AssertAllOf",
    "AssertAnyOf",
    "Asserts",
    "AssertsAllOf",
    "AssertsAnyOf",
    "AttachAFile",
    "AttachesAFile",
    "AttachesFile",
    "AttachesTheFile",
    "AttachFile",
    "AttachTheFile",
    "Confirm",
    "ConfirmAllOf",
    "ConfirmAnyOf",
    "Confirms",
    "ConfirmsAllOf",
    "ConfirmsAnyOf",
    "Debug",
    "Eventually",
    "Log",
    "MakeNote",
    "MakesNote",
    "Observe",
    "ObserveAllOf",
    "ObserveAnyOf",
    "Observes",
    "ObservesAllOf",
    "ObservesAnyOf",
    "Pause",
    "Pauses",
    "Quietly",
    "See",
    "SeeAllOf",
    "SeeAnyOf",
    "Sees",
    "SeesAllOf",
    "SeesAnyOf",
    "Silently",
    "Sleep",
    "Sleeps",
    "TakeNote",
    "TakesNote",
    "Verifies",
    "VerifiesAllOf",
    "VerifiesAnyOf",
    "Verify",
    "VerifyAllOf",
    "VerifyAnyOf",
]
