"""
Make an assertion using a Question and a Resolution.
"""

from hamcrest import assert_that

from screenpy import Actor
from screenpy.protocols import Answerable
from screenpy.resolutions import BaseResolution


class See:
    """See if a Question gives the expected answer.

    This is a very important Action in ScreenPy. It is the way to perform
    test assertions. See the |Question| and |Resolution| documentation.

    Examples::

        the_actor.should(
            See(TheText.of_the(WELCOME_MESSAGE), ReadsExactly("Welcome!")),
            See.the(Number.of(BALLOONS), IsEqualTo(3)),
        )
    """

    @staticmethod
    def the(question: Answerable, resolution: BaseResolution) -> "See":
        """Supply the |Question| and |Resolution| to assert."""
        return See(question, resolution)

    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to make an observation."""
        assert_that(self.question.answered_by(the_actor), self.resolution)

    def __init__(self, question: Answerable, resolution: BaseResolution) -> None:
        self.question = question
        self.resolution = resolution
