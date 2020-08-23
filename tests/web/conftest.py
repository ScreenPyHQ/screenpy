from unittest import mock

import pytest

from screenpy import AnActor
from screenpy.abilities import AuthenticateWith2FA, BrowseTheWeb, MakeAPIRequests


@pytest.fixture(scope="function")
def Tester():
    """Provides an actor with mocked abilities."""
    AuthenticateWith2FA_Mocked = mock.Mock(spec=AuthenticateWith2FA)
    AuthenticateWith2FA_Mocked.otp = mock.Mock()
    BrowseTheWeb_Mocked = mock.Mock(spec=BrowseTheWeb)
    BrowseTheWeb_Mocked.browser = mock.Mock()

    return AnActor.named("Tester").who_can(
        AuthenticateWith2FA_Mocked, BrowseTheWeb_Mocked
    )


@pytest.fixture(scope="function")
def APITester():
    """Provides an actor with mocked abilities."""
    MakeAPIRequests_Mocked = mock.Mock(spec=MakeAPIRequests)
    MakeAPIRequests_Mocked.session = mock.Mock()

    return AnActor.named("Tester").who_can(MakeAPIRequests_Mocked)
