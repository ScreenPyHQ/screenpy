"""
An action to send a OPTIONS request. An actor will need the ability to
MakeAPIRequests to use this action. This action can be performed like so:

    the_actor.attempts_to(SendOPTIONSRequest.to("https://www.example.com"))

    the_actor.attempts_to(
        SendOPTIONSRequest.to(https://www.example.com").with_(
            params={"query": "dramatic%20readings"}
        ),
    )
"""


from .send_api_request import SendAPIRequest


class SendOPTIONSRequest:
    """
    Send a OPTIONS request to a provided URL. A SendOPTIONSRequest action is
    expected to be instantiated in one of these ways:

        SendOPTIONSRequest.to("https://www.example.com"))

        SendOPTIONSRequest.to("https://www.example.com").with_(auth=(USER, PASS))

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def to(url: str) -> "SendAPIRequest":
        """
        Set the URL to send the OPTIONS request to.

        Args:
            url: the URL to which to send the OPTIONS request.
        """
        return SendAPIRequest("OPTIONS", url)
