from time import sleep

from screenpy.actor import Actor, UnableToPerformException
from screenpy.pacing import beat


class Pause:
    """
    Pauses the actor's actions for a set amount of time. This class should
    only be used when absolutely necessary, and make sure to supply a
    reason to the `because` method! An UnableToPerformException will be
    raised if it was not called.

    A Pause action is expected to be instantiated by its static
    |Pause.for_| method. A typical invocation might look like:

        Pause.for_(500).milliseconds().because(
            "the animation to hide the welcome banner needs to finish."
        )

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def for_(number: int) -> "Pause":
        """
        How many seconds or milliseconds to wait for.

        Args:
            number (int): the number of seconds or milliseconds to sleep for.

        Returns:
            Pause
        """
        return Pause(number)

    def seconds(self) -> "Pause":
        """
        Tells the Pause instance to use seconds.

        This is the default behavior, so it's not strictly necessary to
        call this method.
        """
        self.unit = "seconds"
        return self

    def second(self) -> "Pause":
        """Syntactic sugar for Pause.seconds"""
        return self.seconds()

    def milliseconds(self) -> "Pause":
        """
        Tells the Pause instance to use milliseconds.
        """
        self.unit = "milliseconds"
        self.time = self.time / 1000.0
        return self

    def because(self, reason: str) -> "Pause":
        """
        Supply a reason for this pause. Hard waits are the worst of all
        waits, so it helps to document exactly why this wait needs to
        happen.

        If this method is not called, an UnableToPerformException will be
        raised.

        Args:
            reason (str): the reason for needing to pause.
        """
        if not reason.startswith("because"):
            reason = f"because {reason}"

        self.reason = reason
        return self

    @beat("{} pauses for {number} {unit}... {reason}")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Asks the actor to take their union-mandated break.

        Args:
            the_actor (Actor): the actor who will perform this action.

        Raises:
            UnableToPerformException: if "because" was not called.
        """
        if not self.reason:
            raise UnableToPerformException(
                "Cannot Pause without a reason. You need to call .because('')"
            )

        sleep(self.time)

    def __init__(self, number: int) -> None:
        self.number = number
        self.time = number
        self.unit = "seconds"
        self.reason = ""
