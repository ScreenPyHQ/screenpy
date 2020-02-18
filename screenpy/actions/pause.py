"""
An action to pause test execution for a specific time frame. An actor can
perform this action like so:

    the_actor.attempts_to(
        Pause.for_(10).seconds_because("this animation takes forever")
    )
"""


from time import sleep

from ..actor import Actor
from ..exceptions import UnableToActError
from ..pacing import beat
from .base_action import BaseAction


class Pause(BaseAction):
    """
    Pauses the actor's actions for a set amount of time. This class should
    only be used when absolutely necessary. You must call one of the
    "..._because" methods to pass in the reason for your pause; an
    |UnableToActError| will be raised if no reason was given when the
    actor attempts to perform this action.

    A Pause action is expected to be instantiated by its static
    |Pause.for_| method, followed by one of the methods that supply a
    reason (seconds_because, second_because, or milliseconds_because). A
    typical invocation might look like:

        Pause.for_(500).milliseconds_because("the welcome banner needs to hide.")

    It can then be passed along to the |Actor| to perform the action.
    """

    number: float
    time: float
    unit: str
    reason: str

    @staticmethod
    def for_(number: int) -> "Pause":
        """
        How many seconds or milliseconds to wait for.

        Args:
            number: the number of seconds or milliseconds to sleep for.

        Returns:
            |Pause|
        """
        return Pause(number)

    def seconds_because(self, reason: str) -> "Pause":
        """
        Tells the Pause instance to use seconds and provides a reason for
        the pause. Hard waits are the worst of all wait strategies, so
        providing a reason will help explain why it was necessary to use
        this strategy.

        Args:
            reason: the reason for needing to pause.

        Returns:
            |Pause|
        """
        if not reason.startswith("because"):
            reason = f"because {reason}"

        self.unit = "seconds"
        self.reason = reason
        return self

    def second_because(self, reason: str) -> "Pause":
        """Syntactic sugar for Pause.seconds_because"""
        return self.seconds_because(reason)

    def milliseconds_because(self, reason: str) -> "Pause":
        """
        Tells the Pause instance to use milliseconds and provides a reason
        for the pause. Hard waits are the worst of all wait strategies, so
        providing a reason will help explain why it was necessary to use
        this strategy.

        Args:
            reason: the reason for needing to pause.

        Returns:
            |Pause|
        """
        if not reason.startswith("because"):
            reason = f"because {reason}"

        self.unit = "milliseconds"
        self.time = self.time / 1000.0  # type: float
        self.reason = reason
        return self

    @beat("{} pauses for {number} {unit}... {reason}")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Asks the actor to take their union-mandated break.

        Args:
            the_actor: the |Actor| who will perform this action.

        Raises:
            |UnableToActError|: no reason was supplied.
        """
        if not self.reason:
            raise UnableToActError(
                "Cannot Pause without a reason. Use one of "
                ".seconds_because(), .second_because(), or .milliseconds_because()."
            )

        sleep(self.time)

    def __init__(self, number: float) -> None:
        self.number = number
        self.time = number
        self.unit = "seconds"
        self.reason = ""
