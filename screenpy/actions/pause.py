"""
An action to pause test execution for a specific time frame. An actor can
perform this action like so:

    the_actor.attempts_to(
        Pause.for_(10).seconds_because("this animation takes forever")
    )
"""


from time import sleep

from screenpy.actor import Actor
from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat
from selenium.webdriver.common.action_chains import ActionChains


class Pause:
    """
    Pause the actor's actions for a set amount of time. This class should only
    be used when absolutely necessary. You must call one of the "..._because"
    methods to pass in the reason for your pause; an |UnableToAct| will be
    raised if no reason was given.

    A Pause action is expected to be instantiated by its static
    |Pause.for_| method, followed by one of the methods that supply a
    reason (seconds_because, second_because, or milliseconds_because). A
    typical invocation might look like:

        Pause.for_(500).milliseconds_because("the welcome banner needs to hide.")

    It can then be passed along to the |Actor| or added to a |Chain| to
    perform the action.
    """

    time: float

    @staticmethod
    def for_(number: int) -> "Pause":
        """
        Specify how many seconds or milliseconds to wait for.

        Args:
            number: the number of seconds or milliseconds to sleep for.

        Returns:
            |Pause|
        """
        return Pause(number)

    def seconds_because(self, reason: str) -> "Pause":
        """
        Use seconds and provide a reason for the pause. Hard waits are the
        worst of all wait strategies, so providing a reason will help explain
        why it was necessary to use this strategy.

        Args:
            reason: the reason for needing to pause.

        Returns:
            |Pause|
        """
        if not reason.startswith("because"):
            reason = f"because {reason}"

        self.unit = f"second{'s' if self.number != 1 else ''}"
        self.reason = reason
        return self

    second_because = seconds_because

    def milliseconds_because(self, reason: str) -> "Pause":
        """
        Use milliseconds and provide a reason for the pause. Hard waits are
        the worst of all wait strategies, so providing a reason will help
        explain why it was necessary to use this strategy.

        Args:
            reason: the reason for needing to pause.

        Returns:
            |Pause|
        """
        if not reason.startswith("because"):
            reason = f"because {reason}"

        self.unit = f"millisecond{'s' if self.number != 1 else ''}"
        self.time = self.time / 1000.0
        self.reason = reason
        return self

    @beat("{} pauses for {number} {unit} {reason}")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to take their union-mandated break.

        Args:
            the_actor: the |Actor| who will perform this action.

        Raises:
            |UnableToAct|: no reason was supplied.
        """
        if not self.reason:
            raise UnableToAct(
                "Cannot Pause without a reason. Use one of "
                ".seconds_because(), .second_because(), or .milliseconds_because()."
            )

        sleep(self.time)

    @beat("  Pause for {number} {unit} ({reason})!")
    def add_to_chain(self, _: Actor, the_chain: ActionChains) -> None:
        """
        Add the Pause action to an in-progress |Chain| of actions.

        Args:
            _: the |Actor| who will be performing the action chain (unused).
            the_chain: the |ActionChains| instance that is being built.
        """
        the_chain.pause(self.time)

    def __init__(self, number: float) -> None:
        self.number = number
        self.time = number
        self.unit = f"second{'s' if self.number != 1 else ''}"
        self.reason = ""
