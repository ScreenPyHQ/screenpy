"""
An action to send a PATCH request. An actor will need the ability to
MakeAPIRequests to use this action. This action can be performed like so:

    the_actor.attempts_to(SendPATCHRequest.to("https://www.example.com"))

    the_actor.attempts_to(
        SendPATCHRequest.to(https://www.example.com").with_(
            params={"query": "dramatic%20readings"}
        ),
    )
"""


from .send_api_request import SendAPIRequest


class SendPATCHRequest:
    """
    Send a PATCH request to a provided URL. A SendPATCHRequest action is
    expected to be instantiated in one of these ways:

        SendPATCHRequest.to("https://www.example.com"))

        SendPATCHRequest.to("https://www.example.com").with_(auth=(USER, PASS))

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def to(url: str) -> "SendAPIRequest":
        """
        Set the URL to send the PATCH request to.

        Args:
            url: the URL to which to send the PATCH request.
        """
        return SendAPIRequest("PATCH", url)
