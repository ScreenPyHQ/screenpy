"""
An action to pause test execution for a specific time frame.
"""

from time import sleep

from selenium.webdriver.common.action_chains import ActionChains

from screenpy.actor import Actor
from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat


class Pause:
    """Pause the actor's actions for a set amount of time.

    This class should only be used when absolutely necessary. Hard waits are
    the worst of all |wait strategies|; providing a reason will help explain
    why pausing is necessary. You must call one of the "..._because" methods
    to pass in the reason for your pause; an |UnableToAct| will be raised if
    no reason was given.

    Examples::

        the_actor.attempts_to(
            Pause.for_(10).seconds_because("the alert banner needs to hide.")
        )
    """

    time: float

    @staticmethod
    def for_(number: int) -> "Pause":
        """Specify how many seconds or milliseconds to wait for."""
        return Pause(number)

    def _massage_reason(self, reason: str) -> str:
        """Apply some gentle massaging to the reason string."""
        if not reason.startswith("because"):
            reason = f"because {reason}"

        if reason[-1] in [".", ".", "!"]:
            reason = reason[:-1]

        return reason

    def seconds_because(self, reason: str) -> "Pause":
        """Use seconds and provide a reason for the pause."""
        self.unit = f"second{'s' if self.number != 1 else ''}"
        self.reason = self._massage_reason(reason)
        return self

    second_because = seconds_because

    def milliseconds_because(self, reason: str) -> "Pause":
        """Use milliseconds and provide a reason for the pause."""
        self.unit = f"millisecond{'s' if self.number != 1 else ''}"
        self.time = self.time / 1000.0
        self.reason = self._massage_reason(reason)
        return self

    @beat("{} pauses for {number} {unit} {reason}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to take their union-mandated break."""
        if not self.reason:
            raise UnableToAct(
                "Cannot Pause without a reason. Use one of "
                ".seconds_because(), .second_because(), or .milliseconds_because()."
            )

        sleep(self.time)

    @beat("  Pause for {number} {unit} ({reason})!")
    def add_to_chain(self, _: Actor, the_chain: ActionChains) -> None:
        """Add the Pause action to an in-progress |Chain| of actions."""
        the_chain.pause(self.time)

    def __init__(self, number: float) -> None:
        self.number = number
        self.time = number
        self.unit = f"second{'s' if self.number != 1 else ''}"
        self.reason = ""
