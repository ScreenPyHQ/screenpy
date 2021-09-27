"""
Investigate the body of the last API response received by the Actor.
"""

from json.decoder import JSONDecodeError
from typing import Union

from screenpy import Actor
from screenpy.abilities import MakeAPIRequests
from screenpy.exceptions import UnableToAnswer
from screenpy.pacing import beat


class BodyOfTheLastResponse:
    """Ask about the body of the last API response received by the Actor.

    Abilities Required:
        |MakeAPIRequests|

    Examples::

        the_actor.should(
            See.the(BodyOfTheLastResponse(), ContainsTheEntry(play="Hamlet"))
        )

        the_actor.should(
            See.the(BodyOfTheLastResponse(), ReadsExactly("To be, or not to be"))
        )
    """

    def describe(self) -> str:
        """Describe the Question.."""
        return "The body of the last response."

    @beat("{} examines the body of the last response they received.")
    def answered_by(self, the_actor: Actor) -> Union[dict, str]:
        """Direct the Actor to investigate the body of the last response."""
        responses = the_actor.ability_to(MakeAPIRequests).responses
        if len(responses) < 1:
            raise UnableToAnswer(f"{the_actor} has not yet received any API responses.")
        try:
            return responses[-1].json()
        except JSONDecodeError:
            return responses[-1].text
