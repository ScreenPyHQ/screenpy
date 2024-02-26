"""Eventually perform a Task or Action, trying until a set timeout."""

from __future__ import annotations

import time
from traceback import format_tb
from typing import TYPE_CHECKING

from screenpy.configuration import settings
from screenpy.exceptions import DeliveryError, UnableToAct
from screenpy.pacing import beat, the_narrator
from screenpy.speech_tools import get_additive_description

if TYPE_CHECKING:
    from screenpy.actor import Actor
    from screenpy.protocols import Performable


class Eventually:
    """Retry a performable that will eventually (hopefully) succeed.

    ``Eventually`` ignores all errors for the duration of its attempt. If the
    Actor is not able to complete the given Action or Task within the timeout
    period, a ``DeliveryError`` is raised (from the last caught exception).

    Examples::

        the_actor.should(
            Eventually(
                See.the(Text.of_the(WELCOME_BANNER), ContainsTheText("Welcome!"))
            ),
        )

        the_actor.attempts_to(
            Eventually(Click.on_the(BUTTON)).trying_every(100).milliseconds()
        )

        the_actor.was_able_to(
            Eventually(DismissAlert())
            .trying_for(5)
            .seconds()
            .polling_every(500)
            .milliseconds(),
        )
    """

    performable: Performable
    caught_error: Exception | None
    timeout: float

    class _TimeframeBuilder:
        """Build a timeframe, combining numbers and units."""

        def __init__(
            self, eventually: Eventually, amount: float, attribute: str
        ) -> None:
            self.eventually = eventually
            self.amount = amount
            self.attribute = attribute
            setattr(self.eventually, self.attribute, self.amount)

        def milliseconds(self) -> Eventually:
            """Set the timeout in milliseconds."""
            setattr(self.eventually, self.attribute, self.amount / 1000)
            return self.eventually

        millisecond = milliseconds

        def seconds(self) -> Eventually:
            """Set the timeout in seconds."""
            setattr(self.eventually, self.attribute, self.amount)
            return self.eventually

        second = seconds

        def perform_as(self, the_actor: Actor) -> None:
            """Just in case the author forgets to use a unit method."""
            the_actor.attempts_to(self.eventually)

    def for_(self, amount: float) -> _TimeframeBuilder:
        """Set for how long the actor should continue trying.

        Aliases:
            * ``trying_for_no_longer_than``
            * ``trying_for``
            * ``waiting_for``
        """
        return self._TimeframeBuilder(self, amount, "timeout")

    trying_for_no_longer_than = trying_for = waiting_for = for_

    def polling(self, amount: float) -> _TimeframeBuilder:
        """Adjust the polling frequency.

        Aliases:
            * ``polling_every``
            * ``trying_every``
        """
        self.poll = amount
        return self._TimeframeBuilder(self, amount, "poll")

    polling_every = trying_every = polling

    @property
    def performable_to_log(self) -> str:
        """Represent the Performable in a log-friendly way."""
        return get_additive_description(self.performable)

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Eventually {self.performable_to_log}."

    @beat("{} tries to {performable_to_log}, eventually.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to just keep trying."""
        if self.poll > self.timeout:
            msg = "Poll period must be less than or equal to timeout."
            raise UnableToAct(msg)

        end_time = time.time() + self.timeout

        count = 0
        with the_narrator.mic_cable_kinked():
            while True:
                the_narrator.clear_backup()
                try:
                    the_actor.attempts_to(self.performable)
                except Exception as exc:  # noqa: BLE001
                    self.caught_error = exc
                    if not any(same_exception(exc, c) for c in self.unique_errors):
                        self.unique_errors.append(exc)
                else:
                    return

                count += 1
                time.sleep(self.poll)
                if time.time() > end_time:
                    break

        unique_errors_message = "\n    ".join(
            f"{e.__class__.__name__}: {e}" for e in self.unique_errors
        )
        msg = (
            f"{the_actor} tried to Eventually {self.performable_to_log} {count} times"
            f" over {self.timeout} seconds, but got:\n    {unique_errors_message}"
        )
        raise DeliveryError(msg) from self.caught_error

    def __init__(self, performable: Performable) -> None:
        self.performable = performable
        self.caught_error = None
        self.unique_errors: list[BaseException] = []
        self.timeout = settings.TIMEOUT
        self.poll = settings.POLLING


def same_exception(exc1: BaseException, exc2: BaseException) -> bool:
    """Compare two exceptions to see if they match."""
    return (
        isinstance(exc1, type(exc2))
        and (str(exc1) == str(exc2))
        and (format_tb(exc1.__traceback__) == format_tb(exc2.__traceback__))
    )
