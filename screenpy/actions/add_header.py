"""
Add headers to an actor's API session.
"""

from typing import Iterable, Union

from screenpy import Actor
from screenpy.abilities import MakeAPIRequests
from screenpy.pacing import aside, beat


class AddHeader:
    """Add one or more headers to the actor's API session.

    Abilities Required:
        |MakeAPIRequests|

    Examples::

        the_actor.attempts_to(AddHeader(Authorization=TOKEN_AUTH_STRING))

        the_actor.attempts_to(
            AddHeader(Authorization=TOKEN_AUTH_STRING).which_should_be_kept_secret()
        )

        the_actor.attempts_to(AddHeader({"Authorization": TOKEN_AUTH_STRING}))

        the_actor.attempts_to(AddHeader("Authorization", TOKEN_AUTH_STRING))
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

    def __init__(
        self, *header_pairs: Union[str, Iterable], **header_kwargs: str
    ) -> None:
        self.headers = dict()
        if len(header_pairs) == 1:
            self.headers = dict(header_pairs[0])  # type: ignore
        elif header_pairs and len(header_pairs) % 2 == 0:
            self.headers = dict(zip(header_pairs[0::2], header_pairs[1::2]))
        elif header_pairs:
            raise ValueError("AddHeader received an odd-number of key-value pairs.")

        if header_kwargs:
            self.headers.update(header_kwargs)

        self.secret = False
        self.secret_log = ""
