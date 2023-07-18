"""
try/accept logic using screenplay pattern
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.pacing import the_narrator
from screenpy.protocols import Performable

if TYPE_CHECKING:
    from screenpy import Actor


class TryTo(Performable):
    """
    TryTo perform followup action if the first one fails.

    Examples::

        the_actor.will(TryTo(DoAction()).otherwise(DoDifferentAction())

        the_actor.will(
            TryTo(CheckIfOnDomain(URL())).otherwise(Open.their_browser_on(URL())
        )
    """

    Second: tuple[Performable, ...]

    def perform_as(self, the_actor: Actor) -> None:
        """perform a try/accept using the two provided actions"""
        # logs the first attempt even if it fails
        # try:
        #     with the_narrator.mic_cable_kinked():
        #         the_actor.will(*self.First)
        # except AssertionError:
        #     try:
        #         the_actor.will(*self.Second)
        #     except Exception as exc:
        #         raise exc from None

        # Since we are fully expecting assertion error to be raised we kink the
        # cable to avoid the explanation; which only happens when the cable is not
        # kinked

        # logs the first attempt only if it succeeds.
        with the_narrator.mic_cable_kinked():
            try:
                the_actor.will(*self.First)
                return
            except AssertionError:
                the_narrator.clear_backup()

        the_actor.will(*self.Second)
        return

    def or_(self, *second: Performable) -> TryTo:
        """submit the second action"""
        self.Second = second
        return self

    except_ = else_ = otherwise = alternatively = failing_that = or_

    def __init__(self, *first: Performable) -> None:
        self.First: tuple[Performable, ...] = first
