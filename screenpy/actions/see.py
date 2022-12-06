"""
Make an assertion using a Question and a Resolution.
"""

from typing import Type, TypeVar, Union

from hamcrest import assert_that

from screenpy import Actor
from screenpy.pacing import aside, beat
from screenpy.protocols import Answerable, ErrorKeeper
from screenpy.resolutions import BaseResolution
from screenpy.speech_tools import get_additive_description

SelfSee = TypeVar("SelfSee", bound="See")
T_Q = Union[Answerable, object]


class See:
    """See if a value or the answer to a Question matches the Resolution.

    This is a very important Action in ScreenPy. It is the way to perform
    test assertions. For more information, see the documentation for
    :ref:`Questions` and :ref:`Resolutions`.

    Examples::

        the_actor.should(
            See(TheText.of_the(WELCOME_MESSAGE), ReadsExactly("Welcome!")),
        )

        the_actor.should(
            See.the(list_of_items, ContainsTheItem("juice extractor")),
        )
    """

    question: T_Q
    question_to_log: str
    resolution: BaseResolution
    resolution_to_log: str

    @classmethod
    def the(cls: Type[SelfSee], question: T_Q, resolution: BaseResolution) -> SelfSee:
        """Supply the Question (or value) and Resolution to test."""
        return cls(question, resolution)

    def describe(self: SelfSee) -> str:
        """Describe the Action in present tense."""
        return f"See if {self.question_to_log} is {self.resolution_to_log}."

    @beat("{} sees if {question_to_log} is {resolution_to_log}.")
    def perform_as(self: SelfSee, the_actor: Actor) -> None:
        """Direct the Actor to make an observation."""
        if isinstance(self.question, Answerable):
            value: object = self.question.answered_by(the_actor)
        else:
            # must be a value instead of a question!
            value = self.question
            aside(f"the actual value is: {value}")

        reason = ""
        if isinstance(self.question, ErrorKeeper):
            reason = f"{self.question.caught_exception}"

        assert_that(value, self.resolution, reason)

    def __init__(self: SelfSee, question: T_Q, resolution: BaseResolution) -> None:
        self.question = question
        self.question_to_log = get_additive_description(question)
        self.resolution = resolution
        self.resolution_to_log = resolution.get_line()
