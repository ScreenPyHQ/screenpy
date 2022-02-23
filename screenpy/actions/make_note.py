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

    You can access noted values with :ref:`directions` at any point during a
    test, except immediately after making the note. See
    https://screenpy-docs.readthedocs.io/en/latest/cookbook.html#using-makenote.

    Examples::

        the_actor.attempts_to(
            MakeNote.of_the(Number.of(BALLOONS)).as_("excitement gauge"),
        )

        the_actor.attempts_to(MakeNote.of_the(items).as_("items list"))
    """

    key: Optional[str]

    @classmethod
    def of(cls, question: Union[Answerable, Any]) -> "MakeNote":
        """Supply the Question to answer and its arguments."""
        return cls(question)

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
