from unittest import mock

import pytest

from screenpy.abilities import MakeAPIRequests
from screenpy.exceptions import RequestError


class TestMakeAPIRequests:
    def test_can_be_instantiated(self):
        mar1 = MakeAPIRequests()
        mar2 = MakeAPIRequests.using(None)

        assert isinstance(mar1, MakeAPIRequests)
        assert isinstance(mar2, MakeAPIRequests)

    def test_unexpected_http_method(self):
        """Unexpected HTTP method causes an exception"""
        mar = MakeAPIRequests()

        with pytest.raises(RequestError):
            mar.send("TEST_METHOD", "url")

    @pytest.mark.parametrize(
        "method", ["delete", "get", "head", "options", "patch", "post", "put"]
    )
    @mock.patch("screenpy.abilities.make_api_requests.Session")
    def test_http_method_calls_correct_session_method(self, mocked_session, method):
        mar = MakeAPIRequests()

        mar.send(method, "url")

        getattr(mar.session, method).assert_called_once()
