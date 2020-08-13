"""
An action to send a HEAD request. An actor will need the ability to
MakeAPIRequests to use this action. This action can be performed like so:

    the_actor.attempts_to(SendHEADRequest("HEAD", "https://www.example.com"))

    the_actor.attempts_to(
        SendHEADRequest("POST", "https://www.example.com").with_(
            params={"query": "dramatic%20readings"}
        ),
    )
"""


from .send_api_request import SendAPIRequest


class SendHEADRequest:
    """
    Send a HEAD request to a provided URL. A SendHEADRequest action is expected
    to be instantiated in one of these ways:

        SendHEADRequest.to("https://www.example.com"))

        SendHEADRequest.to("https://www.example.com").with_(auth=(USER, PASS))

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def to(url: str) -> "SendAPIRequest":
        """
        Set the URL to send the HEAD request to.

        Args:
            url: the URL to which to send the HEAD request.
        """
        return SendAPIRequest("HEAD", url)
