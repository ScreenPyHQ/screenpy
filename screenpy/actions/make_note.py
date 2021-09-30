"""
Make a quick note about the answer to a Question.
"""

from typing import Any, Optional, Union

from screenpy import Actor, Director
from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat
from screenpy.protocols import Answerable


class MakeNote:
    """Make a note of a value or the answer to a Question.

    You can access noted values with a |direction| at any point during a test.

    Examples::

        the_actor.attempts_to(
            MakeNote.of_the(Text.of_the(WELCOME_BANNER)).as_("welcome message"),
            MakeNote.of_the(list_of_items).as_("items list"),
        )
    """

    key: Optional[str]

    @staticmethod
    def of(question: Union[Answerable, Any]) -> "MakeNote":
        """Supply the Question to answer and its arguments."""
        return MakeNote(question)

    of_the = of

    def as_(self, key: str) -> "MakeNote":
        """Set the key to use to recall this noted value."""
        self.key = key
        return self

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Make a note under {self.key}."

    @beat('{} jots something down under "{key}".')
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to take a note."""
        if self.key is None:
            raise UnableToAct("No key was provided to name this note.")

        if hasattr(self.question, "answered_by"):
            value = self.question.answered_by(the_actor)
        else:
            # must be a value instead of a question!
            value = self.question

        Director().notes(self.key, value)

    def __init__(
        self, question: Union[Answerable, Any], key: Optional[str] = None
    ) -> None:
        self.question = question
        self.key = key
