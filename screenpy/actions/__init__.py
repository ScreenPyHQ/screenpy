"""
Actions are what the actors do, possibly requiring use of their abilities.
Ask your actors to perform actions by passing the actions into their
|Actor.was_able_to| or |Actor.attempts_to| method.
"""

from .accept_alert import AcceptAlert
from .add_header import AddHeader
from .chain import Chain
from .clear import Clear
from .click import Click
from .debug import Debug
from .dismiss_alert import DismissAlert
from .double_click import DoubleClick
from .enter import Enter
from .enter_2fa_token import Enter2FAToken
from .go_back import GoBack
from .go_forward import GoForward
from .hold_down import HoldDown
from .move_mouse import MoveMouse
from .open import Open
from .pause import Pause
from .refresh_page import RefreshPage
from .release import Release
from .respond_to_the_prompt import RespondToThePrompt
from .right_click import RightClick
from .select import Select, SelectByIndex, SelectByText, SelectByValue
from .send_api_request import SendAPIRequest
from .set_headers import SetHeaders
from .switch_to import SwitchTo
from .switch_to_tab import SwitchToTab
from .wait import Wait

# Natural-language-enabling syntactic sugar
AddHeaders = AddHeader
ContextClick = RightClick
Hover = MoveMouse
Press = Enter
Refresh = Reload = ReloadPage = RefreshPage
RespondToPrompt = RespondToThePrompt
Sleep = Pause
SwitchToWindow = SwitchToTab
Visit = Open


def generate_send_method_class(method: str) -> object:
    """
    Generates a class for a specific HTTP method call.
    """

    class SendMETHODRequest:
        "Will be programmatically replaced."

        @staticmethod
        def to(url: str) -> "SendAPIRequest":
            "Will be programmatically replaced."
            return SendAPIRequest(method, url)

    SendMETHODRequest.__doc__ = f"""Send a {method} request to a URL.

Abilities Required:
    |MakeAPIRequests|

Examples::

    the_actor.attempts_to(Send{method}Request.to("https://www.example.com")))

    the_actor.attempts_to(
        Send{method}Request.to("https://www.example.com").with_(auth=(USER, PASS)
    )
"""
    SendMETHODRequest.to.__doc__ = f"""Set the URL to send the {method} request to."""

    return SendMETHODRequest


#: Send a DELETE request to a URL.
#:
#: Abilities Required:
#:     |MakeAPIRequests|
#:
#: Examples::
#:
#:     the_actor.attempts_to(SendDELETERequest.to("https://www.example.com")))
#:
#:     the_actor.attempts_to(
#:         SendDELETERequest.to("https://www.example.com").with_(auth=(USER, PASS))
#:     )
SendDELETERequest = generate_send_method_class("DELETE")

#: Send a GET request to a URL.
#:
#: Abilities Required:
#:     |MakeAPIRequests|
#:
#: Examples::
#:
#:     the_actor.attempts_to(SendGETRequest.to("https://www.example.com")))
#:
#:     the_actor.attempts_to(
#:         SendGETRequest.to("https://www.example.com").with_(auth=(USER, PASS))
#:     )
SendGETRequest = generate_send_method_class("GET")

#: Send a HEAD request to a URL.
#:
#: Abilities Required:
#:     |MakeAPIRequests|
#:
#: Examples::
#:
#:     the_actor.attempts_to(SendHEADRequest.to("https://www.example.com")))
#:
#:     the_actor.attempts_to(
#:         SendHEADRequest.to("https://www.example.com").with_(auth=(USER, PASS))
#:     )
SendHEADRequest = generate_send_method_class("HEAD")

#: Send an OPTIONS request to a URL.
#:
#: Abilities Required:
#:     |MakeAPIRequests|
#:
#: Examples::
#:
#:     the_actor.attempts_to(SendOPTIONSRequest.to("https://www.example.com")))
#:
#:     the_actor.attempts_to(
#:         SendOPTIONSRequest.to("https://www.example.com").with_(auth=(USER, PASS))
#:     )
SendOPTIONSRequest = generate_send_method_class("OPTIONS")

#: Send a PATCH request to a URL.
#:
#: Abilities Required:
#:     |MakeAPIRequests|
#:
#: Examples::
#:
#:     the_actor.attempts_to(SendPATCHRequest.to("https://www.example.com")))
#:
#:     the_actor.attempts_to(
#:         SendPATCHRequest.to("https://www.example.com").with_(auth=(USER, PASS))
#:     )
SendPATCHRequest = generate_send_method_class("PATCH")

#: Send a POST request to a URL.
#:
#: Abilities Required:
#:     |MakeAPIRequests|
#:
#: Examples::
#:
#:     the_actor.attempts_to(SendPOSTRequest.to("https://www.example.com")))
#:
#:     the_actor.attempts_to(
#:         SendPOSTRequest.to("https://www.example.com").with_(auth=(USER, PASS))
#:     )
SendPOSTRequest = generate_send_method_class("POST")

#: Send a PUT request to a URL.
#:
#: Abilities Required:
#:     |MakeAPIRequests|
#:
#: Examples::
#:
#:     the_actor.attempts_to(SendPUTRequest.to("https://www.example.com")))
#:
#:     the_actor.attempts_to(
#:         SendPUTRequest.to("https://www.example.com").with_(auth=(USER, PASS))
#:     )
SendPUTRequest = generate_send_method_class("PUT")


__all__ = [
    "AcceptAlert",
    "AddHeader",
    "AddHeaders",
    "Chain",
    "Clear",
    "Click",
    "ContextClick",
    "Debug",
    "DismissAlert",
    "DoubleClick",
    "Enter",
    "Enter2FAToken",
    "GoBack",
    "GoForward",
    "HoldDown",
    "Hover",
    "MoveMouse",
    "Open",
    "Pause",
    "Press",
    "Refresh",
    "RefreshPage",
    "Release",
    "Reload",
    "ReloadPage",
    "RespondToPrompt",
    "RespondToThePrompt",
    "RightClick",
    "Select",
    "SelectByIndex",
    "SelectByText",
    "SelectByValue",
    "SendDELETERequest",
    "SendGETRequest",
    "SendHEADRequest",
    "SendOPTIONSRequest",
    "SendPATCHRequest",
    "SendPOSTRequest",
    "SendPUTRequest",
    "SetHeaders",
    "Sleep",
    "SwitchTo",
    "SwitchToTab",
    "SwitchToWindow",
    "Visit",
    "Wait",
]
