from screenpy.abilities import MakeAPIRequests
from screenpy.actions.api.send_api_request import SendAPIRequest


class TestSendAPIRequest:
    def test_parameters_passed_to_session(self, APITester):
        """All the given args and kwargs are passed to the session"""
        method = "GET"
        url = "TEST_URL"
        kwargs = {"test": "kwargs"}

        APITester.attempts_to(SendAPIRequest(method, url).with_(**kwargs))

        mocked_mar = APITester.ability_to(MakeAPIRequests)
        mocked_mar.to_send.assert_called_once_with(method, url, **kwargs)
