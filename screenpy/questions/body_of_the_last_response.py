"""
A question to facilitate API testing by asking about the JSON body of the last
response received by the actor.
"""

from json.decoder import JSONDecodeError
from typing import Union

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

    def answered_by(self, the_actor: Actor) -> Union[dict, str]:
        """
        Direct the actor to investigate the last response from an API request.

        Returns:
            dict: the JSON body of the last response.
            str: the text body of the last response, if it's not JSON.
        """
        responses = the_actor.ability_to(MakeAPIRequests).responses
        if len(responses) < 1:
            raise UnableToAnswer(f"{the_actor} has not yet received any API responses.")
        try:
            return responses[-1].json()
        except JSONDecodeError:
            return responses[-1].text
