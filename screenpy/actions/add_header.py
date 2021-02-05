"""
Add headers to an actor's API session.
"""

from screenpy import Actor
from screenpy.abilities import MakeAPIRequests
from screenpy.pacing import aside, beat


class AddHeader:
    """Add one or more headers to the actor's API session.

    Abilities Required:
        |MakeAPIRequests|

    Examples::

        the_actor.attempts_to(AddHeader(Authorization=TOKEN_AUTH_STRING))
    """

    @beat("{} adds some headers to their session.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to add the given headers to their session."""
        aside(f"... the headers are:\n{self.headers}")
        session = the_actor.ability_to(MakeAPIRequests).session
        session.headers.update(self.headers)

    def __init__(self, **headers: str) -> None:
        self.headers = headers
