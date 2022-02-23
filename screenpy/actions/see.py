"""
Make an assertion using a Question and a Resolution.
"""

from typing import Any, Union

from hamcrest import assert_that

from screenpy import Actor
from screenpy.pacing import aside, beat
from screenpy.protocols import Answerable
from screenpy.resolutions import BaseResolution
from screenpy.speech_tools import get_additive_description


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

    @classmethod
    def the(cls, question: Union[Answerable, Any], resolution: BaseResolution) -> "See":
        """Supply the Question (or value) and Resolution to test."""
        return cls(question, resolution)

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"See if {self.question_to_log} is {self.resolution_to_log}."

    @beat("{} sees if {question_to_log} is {resolution_to_log}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to make an observation."""
        if hasattr(self.question, "answered_by"):
            value = self.question.answered_by(the_actor)
        else:
            # must be a value instead of a question!
            value = self.question
            aside(f"the actual value is: {value}")

        assert_that(value, self.resolution)

    def __init__(
        self, question: Union[Answerable, Any], resolution: BaseResolution
    ) -> None:
        self.question = question
        self.question_to_log = get_additive_description(question)
        self.resolution = resolution
        self.resolution_to_log = resolution.get_line()
