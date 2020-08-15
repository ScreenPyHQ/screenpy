"""
All the actions an actor can perform specific to API testing.
"""

from .send_api_request import SendAPIRequest


def generate_send_method_class(method):
    """
    Generates a class for a specific HTTP method call.
    """

    class SendMETHODRequest:
        "Will be programmatically replaced."

        @staticmethod
        def to(url: str) -> "SendAPIRequest":
            "Will be programmatically replaced."
            return SendAPIRequest(method, url)

    SendMETHODRequest.__doc__ = f"""
        Send a {method} request to a URL. Use a Send{method}Request action like so:

            Send{method}Request.to("https://www.example.com"))

            Send{method}Request.to("https://www.example.com").with_(auth=(USER, PASS))
    """
    SendMETHODRequest.to.__doc__ = f"""
        Set the URL to send the {method} request to.

        Args:
            url: the URL to which to send the {method} request.
    """

    return SendMETHODRequest


#: Send a DELETE request to a URL. Use a SendDELETERequest action like so:
#:
#:     SendDELETERequest.to("https://www.example.com"))
#:
#:     SendDELETERequest.to("https://www.example.com").with_(auth=(USER, PASS))
SendDELETERequest = generate_send_method_class("DELETE")

#: Send a GET request to a URL. Use a SendGETRequest action like so:
#:
#:     SendGETRequest.to("https://www.example.com"))
#:
#:     SendGETRequest.to("https://www.example.com").with_(auth=(USER, PASS))
SendGETRequest = generate_send_method_class("GET")

#: Send a HEAD request to a URL. Use a SendHEADRequest action like so:
#:
#:     SendHEADRequest.to("https://www.example.com"))
#:
#:     SendHEADRequest.to("https://www.example.com").with_(auth=(USER, PASS))
SendHEADRequest = generate_send_method_class("HEAD")

#: Send an OPTIONS request to a URL. Use a SendOPTIONSRequest action like so:
#:
#:     SendOPTIONSRequest.to("https://www.example.com"))
#:
#:     SendOPTIONSRequest.to("https://www.example.com").with_(auth=(USER, PASS))
SendOPTIONSRequest = generate_send_method_class("OPTIONS")

#: Send a PATCH request to a URL. Use a SendPATCHRequest action like so:
#:
#:     SendPATCHRequest.to("https://www.example.com"))
#:
#:     SendPATCHRequest.to("https://www.example.com").with_(auth=(USER, PASS))
SendPATCHRequest = generate_send_method_class("PATCH")

#: Send a POST request to a URL. Use a SendPOSTRequest action like so:
#:
#:     SendPOSTRequest.to("https://www.example.com"))
#:
#:     SendPOSTRequest.to("https://www.example.com").with_(auth=(USER, PASS))
SendPOSTRequest = generate_send_method_class("POST")

#: Send a PUT request to a URL. Use a SendPUTRequest action like so:
#:
#:     SendPUTRequest.to("https://www.example.com"))
#:
#:     SendPUTRequest.to("https://www.example.com").with_(auth=(USER, PASS))
SendPUTRequest = generate_send_method_class("PUT")

__all__ = [
    "SendDELETERequest",
    "SendGETRequest",
    "SendHEADRequest",
    "SendOPTIONSRequest",
    "SendPATCHRequest",
    "SendPOSTRequest",
    "SendPUTRequest",
]
