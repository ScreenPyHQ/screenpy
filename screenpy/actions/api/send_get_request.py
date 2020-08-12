"""
An action to send a GET request. An actor will need the ability to
MakeAPIRequests to use this action. This action can be performed like so:

    the_actor.attempts_to(SendGETRequest("GET", "https://www.example.com"))

    the_actor.attempts_to(
        SendGETRequest("POST", "https://www.example.com").with_(
            params={"query": "dramatic%20readings"}
        ),
    )
"""


from .send_api_request import SendAPIRequest


class SendGETRequest:
    """
    Send a GET request to a provided URL. A SendGETRequest action is expected
    to be instantiated in one of these ways:

        SendGETRequest.to("https://www.example.com"))

        SendGETRequest.to("https://www.example.com").with_(auth=(USER, PASS))

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def to(url: str) -> "SendAPIRequest":
        """
        Set the URL to send the GET request to.

        Args:
            url: the URL to which to send the GET request.
        """
        return SendAPIRequest("GET", url)
