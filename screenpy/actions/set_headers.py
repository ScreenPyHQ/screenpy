"""
Set the headers on the Actor's API session.
"""

from typing import Iterable, Union

from screenpy import Actor
from screenpy.abilities import MakeAPIRequests
from screenpy.pacing import aside, beat


class SetHeaders:
    """Set the headers of the Actor's API session to this specific set.

    Note this will remove all other headers on your session.

    Abilities Required:
        |MakeAPIRequests|

    Examples::

        the_actor.attempts_to(SetHeaders(Cookies="csrf_token=1234"))

        the_actor.attempst_to(SetHeaders.to(Cookies="csrf_token=1234"))

        the_actor.attempts_to(
            SetHeaders(Cookies="csrf_token=1234").which_should_be_kept_secret()
        )

        the_actor.attempts_to(SetHeaders({"Cookies": "csrf_token=1234"}))

        the_actor.attempts_to(SetHeaders("Cookies", "csrf_token=1234"))
    """

    @staticmethod
    def to(**kwargs: str) -> "SetHeaders":
        """Specify the headers to set."""
        return SetHeaders(**kwargs)

    def which_should_be_kept_secret(self) -> "SetHeaders":
        """Indicate these headers should not be written to the log."""
        self.secret = True
        self.secret_log = " secret"
        return self

    secretly = which_should_be_kept_secret

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Set the{self.secret_log} headers of a session."

    @beat("{} sets the{secret_log} headers of their session.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to set the headers for their API session."""
        if not self.secret:
            aside(f"... the headers are:\n{self.headers}")
        session = the_actor.ability_to(MakeAPIRequests).session
        session.headers.clear()
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
            raise ValueError("SetHeader received an odd-number of key-value pairs.")

        if header_kwargs:
            self.headers.update(header_kwargs)

        self.secret = False
        self.secret_log = ""
