import pytest

from screenpy.actions.api import (
    SendDELETERequest,
    SendGETRequest,
    SendHEADRequest,
    SendOPTIONSRequest,
    SendPOSTRequest,
)
from screenpy.actions.api.send_api_request import SendAPIRequest


@pytest.mark.parametrize(
    "request_class",
    [
        SendDELETERequest,
        SendGETRequest,
        SendHEADRequest,
        SendOPTIONSRequest,
        SendPOSTRequest,
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
