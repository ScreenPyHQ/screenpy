"""
An action to send an API request.
"""

from screenpy.abilities import MakeAPIRequests
from screenpy.actor import Actor
from screenpy.pacing import aside, beat


class SendAPIRequest:
    """Send an API request.

    You can use this action class directly if you wish, but the
    Send{METHOD}Request classes are easier to read.

    Abilities Required:
        |MakeAPIRequests|

    Examples::

        the_actor.attempts_to(SendAPIRequest("GET", "http://www.example.com"))

        the_actor.attempts_to(
            SendAPIRequest("POST", "http://www.example.com").with_(
                data={"screenplay": "Citizen Kane"}
            )
        )
    """

    def with_(self, **kwargs) -> "SendAPIRequest":
        """Set additional kwargs to send through to the session's request.

        Args:
            kwargs: keyword arguments that correspond to |request|'s API.
        """
        self.kwargs = kwargs
        return self

    @beat("{} sends a {method} request to {url}")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to send an API request to the stored URL."""
        if self.kwargs:
            aside(f"... along with the following: {self.kwargs}")

        the_actor.uses_ability_to(MakeAPIRequests).to_send(
            self.method, self.url, **self.kwargs
        )

    def __init__(self, method: str, url: str) -> None:
        self.method = method.upper()
        self.url = url
        self.kwargs = {}
