"""
try/accept logic using screenplay pattern
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.configuration import settings
from screenpy.pacing import the_narrator
from screenpy.speech_tools import get_additive_description

if TYPE_CHECKING:
    from screenpy import Actor
    from screenpy.protocols import Performable


class Either:
    """Either performs followup action if the first one fails.

    Allows actors to perform try/except blocks while still using screenplay pattern.

    Examples::

        the_actor.will(Either(DoAction()).or_(DoDifferentAction())

        the_actor.will(
            Either(DoAction()).otherwise(DoDifferentAction()).ignoring(
                AssertionError, NotImplementedError
            )
        )

        the_actor.will(
            Either(CheckIfOnDomain(URL())).or_(Open.their_browser_on(URL())
        )
    """

    except_performables: tuple[Performable, ...]
    ignore_exceptions: tuple[type[BaseException], ...]

    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to do one of two actions using try/accept."""
        # kinking the cable before the attempt
        # avoids explaning what the actor tries to do.
        # logs the first attempt only if it succeeds
        # or if UNABRIDGED_NARRATION is enabled
        with the_narrator.mic_cable_kinked():
            try:
                the_actor.will(*self.try_performables)
            except self.ignore_exceptions:
                if not settings.UNABRIDGED_NARRATION:
                    the_narrator.clear_backup()
            else:
                return

        the_actor.will(*self.except_performables)
        return

    def or_(self, *except_performables: Performable) -> Either:
        """Provide the alternative routine to perform.

        Aliases:
            * :meth:`~screenpy.actions.Either.except_`
            * :meth:`~screenpy.actions.Either.else_`
            * :meth:`~screenpy.actions.Either.otherwise`
            * :meth:`~screenpy.actions.Either.alternatively`
            * :meth:`~screenpy.actions.Either.failing_that`
        """
        self.except_performables = except_performables
        return self

    except_ = else_ = otherwise = alternatively = failing_that = or_

    def ignoring(self, *ignored_exceptions: type[BaseException]) -> Either:
        """Set the expception classes to Ignore"""
        self.ignore_exceptions = ignored_exceptions
        return self

    def describe(self) -> str:
        """Describe the Action in present tense."""
        try_summary = ", ".join(
            get_additive_description(action) for action in self.try_performables
        )
        except_summary = ", ".join(
            get_additive_description(action) for action in self.except_performables
        )

        return f"Either {try_summary} or {except_summary}"

    def __init__(self, *first: Performable) -> None:
        self.try_performables: tuple[Performable, ...] = first
        self.ignore_exceptions = (AssertionError,)
