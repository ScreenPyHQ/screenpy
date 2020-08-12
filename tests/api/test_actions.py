from screenpy.actions.api import SendGETRequest
from screenpy.actions.api.send_api_request import SendAPIRequest


class TestSendGETRequest:
    def test_can_be_instantiated(self):
        """SendGETRequest instantiation gives back SendAPIRequest"""
        sgr1 = SendGETRequest.to("url")
        sgr2 = SendGETRequest.to("url").with_(some="kwarg")

        assert isinstance(sgr1, SendAPIRequest)
        assert isinstance(sgr2, SendAPIRequest)
