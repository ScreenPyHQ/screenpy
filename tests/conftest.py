from typing import Generator
from unittest import mock

import pytest

from screenpy import AnActor, pacing
from screenpy.abilities import AuthenticateWith2FA, BrowseTheWeb, MakeAPIRequests
from screenpy.narration.narrator import Narrator


@pytest.fixture(scope="function")
def Tester() -> AnActor:
    """Provide an Actor with mocked web browsing abilities."""
    AuthenticateWith2FA_Mocked = mock.Mock(spec=AuthenticateWith2FA)
    AuthenticateWith2FA_Mocked.otp = mock.Mock()
    BrowseTheWeb_Mocked = mock.Mock(spec=BrowseTheWeb)
    BrowseTheWeb_Mocked.browser = mock.Mock()

    return AnActor.named("Tester").who_can(
        AuthenticateWith2FA_Mocked, BrowseTheWeb_Mocked
    )


@pytest.fixture(scope="function")
def APITester() -> AnActor:
    """Provide an Actor with mocked API testing abilities."""
    MakeAPIRequests_Mocked = mock.Mock(spec=MakeAPIRequests)
    MakeAPIRequests_Mocked.session = mock.Mock()

    return AnActor.named("Tester").who_can(MakeAPIRequests_Mocked)


@pytest.fixture(scope="function")
def mocked_narrator() -> Generator:
    """Mock out the Narrator for a test, replacing the old one afterwards."""
    MockNarrator = mock.MagicMock(spec=Narrator)
    old_narrator = pacing.the_narrator
    pacing.the_narrator = MockNarrator

    yield MockNarrator

    pacing.the_narrator = old_narrator
