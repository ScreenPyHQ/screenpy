"""
Log the answer to a Question or other Answerable.
"""

from screenpy.actor import Actor
from screenpy.pacing import beat
from screenpy.protocols import Answerable
from screenpy.speech_tools import get_additive_description


class Log:
    """Log the answer to a Question.

    Probably most useful for debugging a test, or for announcing the
    answer to a question for the record.

    Examples::
        the_actor.attempts_to(Log.the(Number.of(SNAKES_ON_THE_PLANE)))
    """

    @beat("{} examines {question_to_log}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to find the answer to the Question."""
        self.question.answered_by(the_actor)

    def __init__(self, question: Answerable) -> None:
        self.question = question
        self.question_to_log = get_additive_description(self.question)
