import pytest

from screenpy.actions.api import (
    generate_send_method_class,
    SendDELETERequest,
    SendGETRequest,
    SendHEADRequest,
    SendOPTIONSRequest,
    SendPATCHRequest,
    SendPOSTRequest,
    SendPUTRequest,
)
from screenpy.actions.api.send_api_request import SendAPIRequest


def test_generate_send_method_class_docstring():
    """Generated class and method's docstring both contain method name."""
    test_method = "TEST"

    SendTESTMethod = generate_send_method_class(test_method)

    assert test_method in SendTESTMethod.__doc__
    assert test_method in SendTESTMethod.to.__doc__


@pytest.mark.parametrize(
    "request_class",
    [
        SendDELETERequest,
        SendGETRequest,
        SendHEADRequest,
        SendOPTIONSRequest,
        SendPATCHRequest,
        SendPOSTRequest,
        SendPUTRequest,
    ],
)
def test_can_be_instantiated(request_class):
    """Send{METHOD}Request instantiation gives back SendAPIRequest"""
    sr1 = request_class.to("url")
    sr2 = request_class.to("url").with_(some="kwarg")

    assert isinstance(sr1, SendAPIRequest)
    assert isinstance(sr2, SendAPIRequest)


class TestSendAPIRequest:
    def test_can_be_instantiated(self):
        """SendAPIRequest can be instantiated"""
        sar1 = SendAPIRequest("GET", "test")
        sar2 = SendAPIRequest("GET", "test").with_(some="kwarg")

        assert isinstance(sar1, SendAPIRequest)
        assert isinstance(sar2, SendAPIRequest)

    def test_stores_kwargs(self):
        """kwargs are stored to send in the request later"""
        test_kwargs = {"test": "kwarg"}
        sar = SendAPIRequest("GET", "test").with_(**test_kwargs)

        assert sar.kwargs == test_kwargs
