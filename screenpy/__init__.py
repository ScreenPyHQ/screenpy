#                 ____                           ____
#                / ___|  ___ _ __ ___  ___ _ __ |  _ \ _   _
#                \___ \ / __| '__/ _ \/ _ \ '_ \| |_) | | | |
#                 ___) | (__| | |  __/  __/ | | |  __/| |_| |
#                |____/ \___|_|  \___|\___|_| |_|_|    \__, |
#                                                      |___/

"""
                                  ScreenPy.

                                                                      FADE IN:

INT. SITEPACKAGES DIRECTORY.

ScreenPy is a composition-based test framework. It is inspired by the
SerenityBDD library for Java.

:copyright: (c) 2019-2024 by Perry Goy.
:license: MIT, see LICENSE for more details.
"""

from . import actions, narration, resolutions
from .actions import *  # noqa: F403
from .actor import Actor
from .configuration import settings
from .directions import noted, noted_under, the_noted
from .director import Director
from .exceptions import (
    AbilityError,
    ActionError,
    DeliveryError,
    NotAnswerable,
    NotPerformable,
    NotResolvable,
    QuestionError,
    ScreenPyError,
    UnableToAct,
    UnableToAnswer,
    UnableToDirect,
    UnableToNarrate,
    UnableToPerform,
)
from .given_when_then import and_, given, given_that, then, when
from .narration import *  # noqa: F403
from .pacing import act, aside, beat, scene, the_narrator
from .protocols import (
    Adapter,
    Answerable,
    Describable,
    ErrorKeeper,
    Forgettable,
    Performable,
    Resolvable,
)
from .resolutions import *  # noqa: F403

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
    "NotAnswerable",
    "noted",
    "noted_under",
    "NotPerformable",
    "NotResolvable",
    "Performable",
    "QuestionError",
    "Resolvable",
    "scene",
    "ScreenPyError",
    "settings",
    "the_narrator",
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
