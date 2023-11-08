"""Log the answer to a Question or other Answerable, or a value."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from screenpy.pacing import aside, beat
from screenpy.protocols import Answerable
from screenpy.speech_tools import get_additive_description, represent_prop

if TYPE_CHECKING:
    from screenpy.actor import Actor

    from .see import T_Q


SelfLog = TypeVar("SelfLog", bound="Log")


class Log:
    """Log the answer to a Question, or anything.

    Probably most useful for debugging a test, or for announcing the
    answer to a Question for the record.

    Examples::
        the_actor.attempts_to(Log(HowManyBirdsAreInTheSky()))

        the_actor.attempts_to(Log.the(Number.of(SNAKES_ON_THE_PLANE)))
    """

    @classmethod
    def the(cls: type[SelfLog], question: T_Q) -> SelfLog:
        """Supply the Question to answer."""
        return cls(question)

    @beat("{} examines {question_to_log}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to announce the answer to the Question."""
        if isinstance(self.question, Answerable):
            self.question.answered_by(the_actor)
        else:
            # must be a value instead of a Question!
            aside(f"the value is: {represent_prop(self.question)}")

    def __init__(self, question: T_Q) -> None:
        self.question = question
        self.question_to_log = get_additive_description(self.question)
