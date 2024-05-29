"""Tell an Actor to Stop!"""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.configuration import settings
from screenpy.exceptions import DeliveryError
from screenpy.pacing import beat
from screenpy.speech_tools import get_additive_description

from .eventually import Eventually
from .see import See
from .silently import Silently

if TYPE_CHECKING:
    from typing_extensions import Self

    from screenpy import Actor
    from screenpy.protocols import Answerable, Resolvable


class Stop:
    """Stop until a condition is met.

    The condition could be a Question and a Resolution, or it could be you (the
    test runner) pressing ``enter`` on your keyboard.

    If this Action is used directly (like ``Stop()``), the Actor will stop until
    you press enter to continue the test. In this way it can be used to assess
    the current state of the system under test, similar to :ref:`Debug`.

    If this Action is passed a Question and a Resolution, it will tell the Actor
    to stop until the condition is met. This is essentially the same as
    :ref:`Eventually` (:ref:`See` (...)), but does not carry the connotation of a
    test assertion.

    Examples::

        the_actor(Stops())

        the_actor.attempts_to(Stop.until_the(TotalCakesBaked(), IsEqualTo(20)))

        the_actor.will(Stop.until_the(AudienceTension(), IsGreaterThan(9000)))
    """

    @classmethod
    def until_the(cls, question: Answerable, resolution: Resolvable) -> Self:
        """Specify the condition to wait for."""
        return cls(question, resolution)

    def __init__(
        self, question: Answerable | None = None, resolution: Resolvable | None = None
    ) -> None:
        self.question = question
        self.resolution = resolution

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Stop until {self.description_to_log}."

    @property
    def question_to_log(self) -> str:
        """Represent the Question in a log-friendly way."""
        return get_additive_description(self.question)

    @property
    def resolution_to_log(self) -> str:
        """Represent the Resolution in a log-friendly way."""
        return get_additive_description(self.resolution)

    @property
    def description_to_log(self) -> str:
        """Represent the Action in a log-friendly way."""
        if self.question is None and self.resolution is None:
            return "they hear your cue"
        return f"{self.question_to_log} is {self.resolution_to_log}"

    @beat("{} stops until {description_to_log}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to stop until the condition is met."""
        if self.question is None or self.resolution is None:
            msg = (
                "\n\nThe Actor stops suddenly, waiting for your cue..."
                "\n (press enter to continue): "
            )
            input(msg)
            return

        try:
            the_actor.attempts_to(
                Silently(Eventually(See.the(self.question, self.resolution)))
            )
        except DeliveryError as caught_exception:
            msg = (
                f"{the_actor} stopped for {settings.TIMEOUT} seconds, but"
                f" {self.question_to_log} was never {self.resolution_to_log}."
            )
            raise DeliveryError(msg) from caught_exception
