"""
Investigate the status code of the last API response received.
"""

from screenpy import Actor
from screenpy.abilities import MakeAPIRequests
from screenpy.exceptions import UnableToAnswer
from screenpy.pacing import beat


class StatusCodeOfTheLastResponse:
    """Ask about the status code of the last API response received.

    Abilities Required:
        |MakeAPIRequests|

    Examples::

        the_actor.should(
            See.the(StatusCodeOfTheLastResponse(), IsEqualTo(200))
        )
    """

    def describe(self) -> str:
        """Describe the Question.."""
        return "The HTTP status code of the last response."

    @beat("{} examines the status code of the last response they received.")
    def answered_by(self, the_actor: Actor) -> float:
        """Direct the Actor to investigate the status code of the last response."""
        responses = the_actor.ability_to(MakeAPIRequests).responses
        if len(responses) < 1:
            raise UnableToAnswer(f"{the_actor} has not yet received any API responses.")
        return responses[-1].status_code
