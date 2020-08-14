"""
An action to send a DELETE request. An actor will need the ability to
MakeAPIRequests to use this action. This action can be performed like so:

    the_actor.attempts_to(
        SendDELETERequest("DELETE", "https://www.example.com")
    )

    the_actor.attempts_to(
        SendDELETERequest("POST", "https://www.example.com").with_(
            params={"query": "dramatic%20readings"}
        ),
    )
"""


from .send_api_request import SendAPIRequest


class SendDELETERequest:
    """
    Send a DELETE request to a provided URL. A SendDELETERequest action is
    expected to be instantiated in one of these ways:

        SendDELETERequest.to("https://www.example.com"))

        SendDELETERequest.to("https://www.example.com").with_(auth=(USER, PASS))

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def to(url: str) -> "SendAPIRequest":
        """
        Set the URL to send the DELETE request to.

        Args:
            url: the URL to which to send the DELETE request.
        """
        return SendAPIRequest("DELETE", url)
