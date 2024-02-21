"""Attempt one of two different performances.

Simulates a try/except control flow, but in Screenplay Pattern.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.configuration import settings
from screenpy.pacing import the_narrator
from screenpy.speech_tools import get_additive_description

if TYPE_CHECKING:
    from typing_extensions import Self

    from screenpy import Actor
    from screenpy.protocols import Performable


class Either:
    """Perform one of two branching performances.

    Simulates a try/except block while still following Screenplay Pattern.

    By default, ``Either`` catches AssertionErrors, so you can use
    :class:`~screenpy.actions.See` to decide which path to follow. Use the
    :meth:`ignoring` method to ignore other exceptions.

    Examples::

        the_actor.will(Either(DoAction()).or_(DoDifferentAction())

        the_actor.will(
            Either(DoAction()).otherwise(DoDifferentAction()).ignoring(
                AssertionError, NotImplementedError
            )
        )

        # using a custom Task which raises AssertionError
        the_actor.will(
            Either(CheckIfOnDomain(URL())).or_(Open.their_browser_on(URL())
        )
    """

    except_performables: tuple[Performable, ...]
    ignore_exceptions: tuple[type[BaseException], ...]

    def or_(self, *except_performables: Performable) -> Self:
        """Provide the alternative routine to perform.

        Aliases:
            * ``except_``
            * ``else_``
            * ``otherwise``
            * ``alternatively``
            * ``failing_that``
        """
        self.except_performables = except_performables
        return self

    except_ = else_ = otherwise = alternatively = failing_that = or_

    def ignoring(self, *ignored_exceptions: type[BaseException]) -> Self:
        """Set the expception classes to ignore."""
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

    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to perform one of two performances."""
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

    def __init__(self, *first: Performable) -> None:
        self.try_performables: tuple[Performable, ...] = first
        self.ignore_exceptions = (AssertionError,)
