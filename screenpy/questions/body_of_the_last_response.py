"""
A question to facilitate API testing by asking about the JSON body of the last
response received by the actor.
"""

from screenpy import Actor
from screenpy.abilities import MakeAPIRequests
from screenpy.exceptions import UnableToAnswer


class BodyOfTheLastResponse:
    """
    Ask about the JSON body of the last response received by the actor.

    Examples:
        the_actor.should_see_the(
            (BodyOfTheLastResponse(), ContainsTheEntry(play="Hamlet"))
        )

    Abilities Required:
        |MakeAPIRequests|
    """

    def answered_by(self, the_actor: Actor) -> dict:
        """
        Direct the actor to investigate the last response from an API request.

        Returns:
            the JSON body of the last response, as a dict.
        """
        responses = the_actor.ability_to(MakeAPIRequests).responses
        if len(responses) < 1:
            raise UnableToAnswer(f"{the_actor} has not yet received any API responses.")
        return responses[-1].json()
