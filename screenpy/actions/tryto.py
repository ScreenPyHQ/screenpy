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


class TryTo:
    """TryTo perform followup action if the first one fails.

    Allows actors to perform try/except blocks while still using screenplay pattern.
    Examples::

        the_actor.will(TryTo(DoAction()).otherwise(DoDifferentAction())

        the_actor.will(
            TryTo(CheckIfOnDomain(URL())).otherwise(Open.their_browser_on(URL())
        )
    """

    second: tuple[Performable, ...]

    def perform_as(self, the_actor: Actor) -> None:
        """perform a try/accept using the two provided actions"""
        # logs the first attempt even if it fails
        # try:
        #     with the_narrator.mic_cable_kinked():
        #         the_actor.will(*self.first)
        # except AssertionError:
        #     try:
        #         the_actor.will(*self.second)
        #     except Exception as exc:
        #         raise exc from None

        # Since we are fully expecting assertion error to be raised we kink the
        # cable to avoid the explanation; which only happens when the cable is not
        # kinked

        # logs the first attempt only if it succeeds.
        with the_narrator.mic_cable_kinked():
            try:
                the_actor.will(*self.first)
                return
            except AssertionError:
                the_narrator.clear_backup()

        the_actor.will(*self.second)
        return

    def or_(self, *second: Performable) -> TryTo:
        """submit the second action"""
        self.second = second
        return self

    except_ = else_ = otherwise = alternatively = failing_that = or_

    def describe(self) -> str:
        """Describe the Action in present tense."""
        s1 = ""
        s2 = ""
        for a1 in self.first:
            s1 += get_additive_description(a1)

        for a2 in self.second:
            s2 += get_additive_description(a2)

        return f"TryTo {s1} or {s2}"

    def __init__(self, *first: Performable) -> None:
        self.first: tuple[Performable, ...] = first
