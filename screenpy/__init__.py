# -*- coding: utf-8 -*-

#                 ____                           ____
#                / ___|  ___ _ __ ___  ___ _ __ |  _ \ _   _
#                \___ \ / __| '__/ _ \/ _ \ '_ \| |_) | | | |
#                 ___) | (__| | |  __/  __/ | | |  __/| |_| |
#                |____/ \___|_|  \___|\___|_| |_|_|    \__, |
#                                                      |___/

"""
                                  ScreenPy
                                                                      FADE IN:
INT. SITEPACKAGES DIRECTORY

ScreenPy is a composition-based test framework. It is inspired by the
SerenityBDD library for Java.

:copyright: (c) 2019–2023 by Perry Goy.
:license: MIT, see LICENSE for more details.
"""

from .actions import (
    Assert,
    AssertAllOf,
    AssertAnyOf,
    AttachAFile,
    AttachFile,
    AttachTheFile,
    Confirm,
    ConfirmAllOf,
    ConfirmAnyOf,
    Debug,
    Eventually,
    MakeNote,
    Observe,
    ObserveAllOf,
    ObserveAnyOf,
    Pause,
    See,
    SeeAllOf,
    SeeAnyOf,
    Sleep,
    TakeNote,
    Verify,
    VerifyAllOf,
    VerifyAnyOf,
)
from .actor import Actor
from .directions import noted, noted_under, the_noted
from .director import Director
from .given_when_then import and_, given, given_that, then, when
from .narration import Narrator
from .pacing import act, aside, beat, scene, the_narrator
from .resolutions import (
    ContainItemMatching,
    ContainsItemMatching,
    ContainsTheEntries,
    ContainsTheEntry,
    ContainsTheItem,
    ContainsTheKey,
    ContainsTheText,
    ContainsTheValue,
    ContainTheEntries,
    ContainTheEntry,
    ContainTheItem,
    ContainTheKey,
    ContainTheText,
    ContainTheValue,
    DoesNot,
    DoNot,
    Empty,
    EndsWith,
    EndWith,
    Equal,
    Equals,
    EqualTo,
    GreaterThan,
    GreaterThanOrEqualTo,
    HasLength,
    InRange,
    IsCloseTo,
    IsEmpty,
    IsEqual,
    IsEqualTo,
    IsGreaterThan,
    IsGreaterThanOrEqualTo,
    IsInRange,
    IsLessThan,
    IsLessThanOrEqualTo,
    IsNot,
    LessThan,
    LessThanOrEqualTo,
    Match,
    Matches,
    ReadExactly,
    ReadsExactly,
    StartsWith,
    StartWith,
)

# Natural-language-enabling syntactic sugar
AnActor = Actor


__all__ = [
    "Actor",
    "AnActor",
    "Assert",
    "AssertAllOf",
    "AssertAnyOf",
    "AttachAFile",
    "AttachFile",
    "AttachTheFile",
    "Confirm",
    "ConfirmAllOf",
    "ConfirmAnyOf",
    "ContainItemMatching",
    "ContainTheEntries",
    "ContainTheEntry",
    "ContainTheItem",
    "ContainTheKey",
    "ContainTheText",
    "ContainTheValue",
    "ContainsItemMatching",
    "ContainsTheEntries",
    "ContainsTheEntry",
    "ContainsTheItem",
    "ContainsTheKey",
    "ContainsTheText",
    "ContainsTheValue",
    "Debug",
    "Director",
    "DoNot",
    "DoesNot",
    "Empty",
    "EndWith",
    "EndsWith",
    "Equal",
    "EqualTo",
    "Equals",
    "Eventually",
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
    "MakeNote",
    "Match",
    "Matches",
    "Narrator",
    "Observe",
    "ObserveAllOf",
    "ObserveAnyOf",
    "Pause",
    "ReadExactly",
    "ReadsExactly",
    "See",
    "SeeAllOf",
    "SeeAnyOf",
    "Sleep",
    "StartWith",
    "StartsWith",
    "TakeNote",
    "Verify",
    "VerifyAllOf",
    "VerifyAnyOf",
    "act",
    "and_",
    "aside",
    "beat",
    "given",
    "given_that",
    "noted",
    "noted_under",
    "scene",
    "the_narrator",
    "the_noted",
    "then",
    "when",
]
