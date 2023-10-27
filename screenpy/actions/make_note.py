"""Make a quick note about the answer to a Question."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.director import Director
from screenpy.exceptions import UnableToAct
from screenpy.pacing import aside, beat
from screenpy.protocols import Answerable, ErrorKeeper
from screenpy.speech_tools import represent_prop

if TYPE_CHECKING:
    from typing import TypeVar, Union

    from screenpy.actor import Actor

    SelfMakeNote = TypeVar("SelfMakeNote", bound="MakeNote")
    T_Q = Union[Answerable, object]


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

    key: str | None
    question: T_Q

    @classmethod
    def of(cls: type[SelfMakeNote], question: T_Q) -> SelfMakeNote:
        """Supply the Question to answer and its arguments.

        Aliases:
            * :meth:`~screenpy.actions.MakeNote.of_the`
        """
        return cls(question)

    @classmethod
    def of_the(cls: type[SelfMakeNote], question: T_Q) -> SelfMakeNote:
        """Alias for :meth:`~screenpy.actions.MakeNote.of`."""
        return cls.of(question)

    def as_(self: SelfMakeNote, key: str) -> SelfMakeNote:
        """Set the key to use to recall this noted value."""
        self.key = key
        return self

    def describe(self: SelfMakeNote) -> str:
        """Describe the Action in present tense."""
        return f"Make a note under {represent_prop(self.key)}."

    @beat("{} jots something down under {key_to_log}.")
    def perform_as(self: SelfMakeNote, the_actor: Actor) -> None:
        """Direct the Actor to take a note."""
        if self.key is None:
            msg = "No key was provided to name this note."
            raise UnableToAct(msg)

        if isinstance(self.question, Answerable):
            value: object = self.question.answered_by(the_actor)
        else:
            # must be a value instead of a question!
            value = self.question

        if isinstance(self.question, ErrorKeeper):
            aside(f"Making note of {self.question}...")
            aside(f"Caught Exception: {self.question.caught_exception}")

        Director().notes(self.key, value)

    def __init__(
        self: SelfMakeNote,
        question: T_Q,
        key: str | None = None,
    ) -> None:
        self.question = question
        self.key = key
        self.key_to_log = represent_prop(key)
