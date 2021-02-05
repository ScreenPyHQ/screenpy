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

    def which_should_be_kept_secret(self) -> "AddHeader":
        """Indicate the added headers should not be written to the log."""
        self.secret = True
        self.secret_log = " secret"
        return self

    secretly = which_should_be_kept_secret

    @beat("{} adds some{secret_log} headers to their session.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to add the given headers to their session."""
        if not self.secret:
            aside(f"... the headers are:\n{self.headers}")
        session = the_actor.ability_to(MakeAPIRequests).session
        session.headers.update(self.headers)

    def __init__(self, **headers: str) -> None:
        self.headers = headers
        self.secret = False
        self.secret_log = ""
