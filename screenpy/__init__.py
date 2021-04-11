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

:copyright: (c) 2019–2021 by Perry Goy.
:license: MIT, see LICENSE for more details.
"""


from .actor import Actor
from .director import Director
from .given_when_then import and_, given, given_that, then, when
from .target import Target

# Natural-language-enabling syntactic sugar
AnActor = Actor


__all__ = [
    "Actor",
    "AnActor",
    "Director",
    "Target",
    "and_",
    "given",
    "given_that",
    "then",
    "when",
]
