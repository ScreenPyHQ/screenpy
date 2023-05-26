"""
Log the answer to a Question or other Answerable.
"""

from typing import Type, TypeVar

from screenpy.actor import Actor
from screenpy.pacing import aside, beat
from screenpy.protocols import Answerable
from screenpy.speech_tools import get_additive_description

from .see import T_Q

SelfLog = TypeVar("SelfLog", bound="Log")


class Log:
    """Log the answer to a Question, or anything.

    Probably most useful for debugging a test, or for announcing the
    answer to a question for the record.

    Examples::
        the_actor.attempts_to(Log(HowManyBirdsAreInTheSky()))

        the_actor.attempts_to(Log.the(Number.of(SNAKES_ON_THE_PLANE)))
    """

    @classmethod
    def the(cls: Type[SelfLog], question: T_Q) -> SelfLog:
        """Supply the Question to answer."""
        return cls(question)

    @beat("{} examines {question_to_log}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to announce the answer to the Question."""
        if isinstance(self.question, Answerable):
            self.question.answered_by(the_actor)
        else:
            # must be a value instead of a question!
            aside(f"the value is: {self.question}")

    def __init__(self, question: T_Q) -> None:
        self.question = question
        self.question_to_log = get_additive_description(self.question)
