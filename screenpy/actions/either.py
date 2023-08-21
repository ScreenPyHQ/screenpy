"""
try/accept logic using screenplay pattern
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.pacing import the_narrator
from screenpy.speech_tools import get_additive_description

if TYPE_CHECKING:
    from screenpy import Actor
    from screenpy.protocols import Performable


class Either:
    """Either perform followup action if the first one fails.

    Allows actors to perform try/except blocks while still using screenplay pattern.
    Examples::

        the_actor.will(Either(DoAction()).or_(DoDifferentAction())

        the_actor.will(
            Either(CheckIfOnDomain(URL())).or_(Open.their_browser_on(URL())
        )
    """

    except_performables: tuple[Performable, ...]

    def perform_as(self, the_actor: Actor) -> None:
        """perform a try/accept using the two provided actions"""
        # logs the first attempt even if it fails
        # try:
        #     with the_narrator.mic_cable_kinked():
        #         the_actor.will(*self.try_performables)
        # except AssertionError:
        #     try:
        #         the_actor.will(*self.except_performables)
        #     except Exception as exc:
        #         raise exc from None

        # Since we are fully expecting assertion error to be raised we kink the
        # cable to avoid the explanation; which only happens when the cable is not
        # kinked

        # logs the first attempt only if it succeeds.
        with the_narrator.mic_cable_kinked():
            try:
                the_actor.will(*self.try_performables)
                return
            except AssertionError:
                the_narrator.clear_backup()

        the_actor.will(*self.except_performables)
        return

    def or_(self, *except_performables: Performable) -> Either:
        """submit the except_performables action"""
        self.except_performables = except_performables
        return self

    except_ = else_ = otherwise = alternatively = failing_that = or_

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
