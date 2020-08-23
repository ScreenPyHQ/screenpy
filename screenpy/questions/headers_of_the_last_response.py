"""
A question to investigate the headers of the last response received by the
actor, using their ability to MakeAPIRequests.
"""

from typing import MutableMapping

from screenpy import Actor
from screenpy.abilities import MakeAPIRequests
from screenpy.exceptions import UnableToAnswer


class HeadersOfTheLastResponse:
    """
    Ask about the headers of the last API response received by the actor.

    Abilities Required:
        |MakeAPIRequests|

    Examples:
        the_actor.should_see_the(
            (HeadersOfTheLastResponse(), ContainKey("Content-Type"))
        )
    """

    def answered_by(self, the_actor: Actor) -> MutableMapping[str, str]:
        """Direct the actor to investigate the headers of the last response."""
        responses = the_actor.ability_to(MakeAPIRequests).responses
        if len(responses) < 1:
            raise UnableToAnswer(f"{the_actor} has not yet received any API responses.")
        return responses[-1].headers
