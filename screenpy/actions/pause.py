"""Pause test execution for a specific time frame."""

from __future__ import annotations

import re
from time import sleep
from typing import TYPE_CHECKING

from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat

if TYPE_CHECKING:

    from typing_extensions import Self

    from screenpy.actor import Actor


class Pause:
    """Pause the Actor's Actions for a set amount of time.

    This class should only be used when absolutely necessary. Hard waits are
    the worst of all wait strategies; providing a reason will help explain
    why pausing is necessary. You must call one of the "..._because" methods
    to pass a reason for pausing. An :class:`~screenpy.exceptions.UnableToAct`
    exception will be raised if no reason was given.

    Examples::

        the_actor.attempts_to(
            Pause.for_(10).seconds_because("they're being dramatic.")
        )

        the_actor.attempts_to(
            Pause.for_(500).milliseconds_because("of a moment's hesitation.")
        )
    """

    time: float
    number: float
    unit: str
    reason: str

    @classmethod
    def for_(cls, number: float) -> Self:
        """Specify how many seconds or milliseconds to wait for."""
        return cls(number)

    def seconds_because(self, reason: str) -> Self:
        """Use seconds and provide a reason for the pause.

        Aliases:
            * ``second_because``
        """
        self.unit = f"second{'s' if self.number != 1 else ''}"
        self.reason = self._massage_reason(reason)
        return self

    second_because = seconds_because

    def milliseconds_because(self, reason: str) -> Self:
        """Use milliseconds and provide a reason for the pause."""
        self.unit = f"millisecond{'s' if self.number != 1 else ''}"
        self.time = self.time / 1000.0
        self.reason = self._massage_reason(reason)
        return self

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Pause for {self.number} {self.unit} {self.reason}."

    @beat("{} pauses for {number} {unit} {reason}.")
    def perform_as(self, _: Actor) -> None:
        """Direct the Actor to take their union-mandated break."""
        if not self.reason:
            msg = (
                "Cannot Pause without a reason. Use one of"
                " .seconds_because(), .second_because(), or .milliseconds_because()."
            )
            raise UnableToAct(msg)

        sleep(self.time)

    def _massage_reason(self, reason: str) -> str:
        """Apply some gentle massaging to the reason string."""
        if not reason.startswith("because"):
            reason = f"because {reason}"

        return re.sub(r"\W*$", "", reason)

    def __init__(self, number: float) -> None:
        self.number = number
        self.time = number
        self.unit = f"second{'s' if self.number != 1 else ''}"
        self.reason = ""
