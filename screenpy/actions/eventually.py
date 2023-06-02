"""
Eventually perform a Task or Action, trying until a set timeout.
"""

import time
from typing import Dict, Optional

from screenpy.actor import Actor
from screenpy.configuration import settings
from screenpy.exceptions import DeliveryError
from screenpy.pacing import beat, the_narrator
from screenpy.protocols import Performable
from screenpy.speech_tools import get_additive_description


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
    caught_error: Optional[Exception]
    timeout: float

    class _TimeframeBuilder:
        """
        Allows caller of Eventually to tack on waiting for specific time
        frames in seconds or milliseconds.
        """

        def __init__(
            self, eventually: "Eventually", amount: float, attribute: str
        ) -> None:
            self.eventually = eventually
            self.amount = amount
            self.attribute = attribute
            setattr(self.eventually, self.attribute, self.amount)

        def milliseconds(self) -> "Eventually":
            """Set the timeout in milliseconds."""
            setattr(self.eventually, self.attribute, self.amount / 1000)
            return self.eventually

        millisecond = milliseconds

        def seconds(self) -> "Eventually":
            """Set the timeout in seconds."""
            setattr(self.eventually, self.attribute, self.amount)
            return self.eventually

        second = seconds

        def perform_as(self, the_actor: "Actor") -> None:
            """Just in case the author forgets to use a unit method."""
            the_actor.attempts_to(self.eventually)

    def for_(self, amount: float) -> _TimeframeBuilder:
        """Set for how long the actor should continue trying.

        Aliases:
            * :meth:`~screenpy.actions.Eventually.trying_for_no_longer_than`
            * :meth:`~screenpy.actions.Eventually.trying_for`
            * :meth:`~screenpy.actions.Eventually.waiting_for`
        """
        return self._TimeframeBuilder(self, amount, "timeout")

    def trying_for_no_longer_than(self, amount: float) -> _TimeframeBuilder:
        """Alias for :meth:`~screenpy.actions.Eventually.for_`."""
        return self.for_(amount)

    def trying_for(self, amount: float) -> _TimeframeBuilder:
        """Alias for :meth:`~screenpy.actions.Eventually.for_`."""
        return self.for_(amount)

    def waiting_for(self, amount: float) -> _TimeframeBuilder:
        """Alias for :meth:`~screenpy.actions.Eventually.for_`."""
        return self.for_(amount)

    def polling(self, amount: float) -> _TimeframeBuilder:
        """Adjust the polling frequency.

        Aliases:
            * :meth:`~screenpy.actions.Eventually.polling_every`
            * :meth:`~screenpy.actions.Eventually.trying_every`
        """
        self.poll = amount
        return self._TimeframeBuilder(self, amount, "poll")

    def polling_every(self, amount: float) -> _TimeframeBuilder:
        """Alias for :meth:`~screenpy.actions.Eventually.polling`."""
        return self.polling(amount)

    def trying_every(self, amount: float) -> _TimeframeBuilder:
        """Alias for :meth:`~screenpy.actions.Eventually.polling`."""
        return self.polling(amount)

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Eventually {self.performable_to_log}."

    @beat("{} tries to {performable_to_log}, eventually.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to just keep trying."""
        if self.poll > self.timeout:
            raise ValueError("poll must be less than or equal to timeout")

        end_time = time.time() + self.timeout

        count = 0
        with the_narrator.mic_cable_kinked():
            while True:
                the_narrator.clear_backup()
                try:
                    the_actor.attempts_to(self.performable)
                    return
                except Exception as exc:  # pylint: disable=broad-except
                    self.caught_error = exc
                    self.unique_errors[exc] = None

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

    def __init__(self, performable: Performable):
        self.performable = performable
        self.performable_to_log = get_additive_description(self.performable)
        self.caught_error = None
        self.unique_errors: Dict[Exception, None] = {}
        self.timeout = settings.TIMEOUT
        self.poll = settings.POLLING
