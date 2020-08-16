import pytest

from screenpy.questions import BodyOfTheLastResponse
from screenpy.abilities import MakeAPIRequests
from screenpy.exceptions import UnableToAnswer


class TestBodyOfTheLastResponse:
    def test_can_be_instantiated(self):
        botlr = BodyOfTheLastResponse()

        assert isinstance(botlr, BodyOfTheLastResponse)

    def test_raises_error_if_no_responses(self, APITester):
        """Raises UnableToAnswer if no responses yet"""
        botlr = BodyOfTheLastResponse()
        APITester.ability_to(MakeAPIRequests).responses = []

        with pytest.raises(UnableToAnswer):
            botlr.answered_by(APITester)
