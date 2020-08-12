from unittest import mock

import pytest

from screenpy import AnActor
from screenpy.abilities import MakeAPIRequests


@pytest.fixture(scope="function")
def APITester():
    """Provides an actor with mocked abilities."""
    MakeAPIRequests_Mocked = mock.Mock(spec=MakeAPIRequests)
    MakeAPIRequests_Mocked.session = mock.Mock()

    return AnActor.named("Tester").who_can(MakeAPIRequests_Mocked)
