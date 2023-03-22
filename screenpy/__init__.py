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

from . import actions, narration, resolutions
from .actions import *  # noqa
from .actor import Actor
from .directions import noted, noted_under, the_noted
from .director import Director
from .exceptions import (
    AbilityError,
    ActionError,
    DeliveryError,
    QuestionError,
    ScreenPyError,
    UnableToAct,
    UnableToAnswer,
    UnableToDirect,
    UnableToNarrate,
    UnableToPerform,
)
from .given_when_then import and_, given, given_that, then, when
from .narration import *  # noqa
from .pacing import act, aside, beat, scene
from .protocols import (
    Adapter,
    Answerable,
    Describable,
    ErrorKeeper,
    Forgettable,
    Performable,
)
from .resolutions import *  # noqa

# Natural-language-enabling syntactic sugar
AnActor = Actor


__all__ = [
    "AbilityError",
    "act",
    "ActionError",
    "Actor",
    "Adapter",
    "AnActor",
    "and_",
    "Answerable",
    "aside",
    "beat",
    "DeliveryError",
    "Describable",
    "Director",
    "ErrorKeeper",
    "Forgettable",
    "given",
    "given_that",
    "noted",
    "noted_under",
    "Performable",
    "QuestionError",
    "scene",
    "ScreenPyError",
    "the_noted",
    "then",
    "UnableToAct",
    "UnableToAnswer",
    "UnableToDirect",
    "UnableToNarrate",
    "UnableToPerform",
    "when",
]
__all__ += actions.__all__ + resolutions.__all__ + narration.__all__
