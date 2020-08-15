"""
An action to send an API request. This action will most likely be called by
one of the other Send*Request actions, rather than being called directly. An
actor will need the ability to MakeAPIRequests to use this action. This action
can be performed like so:

    the_actor.attempts_to(SendAPIRequest("GET", "https://www.example.com"))

    the_actor.attempts_to(
        SendAPIRequest("POST", "https://www.example.com").with_(
            data={"payload": True}
        ),
    )
"""


from screenpy.abilities import MakeAPIRequests
from screenpy.actor import Actor
from screenpy.pacing import aside, beat


class SendAPIRequest:
    """
    Send an API request. You can use this action class directly if you wish,
    but the Send{METHOD}Request classes are easier to read. If you do wish to
    use this class directly, you can do that like so:

        SendAPIRequest("GET", "http://www.example.com")

        SendAPIRequest("POST", "http://www.example.com").with_(data={"a": "b"})
    """

    def with_(self, **kwargs) -> "SendAPIRequest":
        """
        Set additional kwargs to send through to the session's request.

        Args:
            kwargs: keyword arguments that correspond to |request|'s API.
        """
        self.kwargs = kwargs
        return self

    @beat("{0} sends a {method} request to {url}")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to send a GET request to the stored URL.

        Args:
            the_actor: The |Actor| who will perform this action.
        """
        if self.kwargs:
            aside(f"... along with the following: {self.kwargs}")

        the_actor.uses_ability_to(MakeAPIRequests).to_send(
            self.method, self.url, **self.kwargs
        )

    def __init__(self, method: str, url: str) -> None:
        self.method = method.upper()
        self.url = url
        self.kwargs = {}
