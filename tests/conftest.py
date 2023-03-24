from typing import Any, Generator
from unittest import mock

import pytest

from screenpy import Actor, Narrator, pacing


@pytest.fixture(scope="function")
def Tester() -> Generator[Actor, None, None]:
    """Provide an Actor with mocked web browsing abilities."""
    the_actor = Actor.named("Tester")
    yield the_actor
    the_actor.exit()


@pytest.fixture(scope="function")
def mocked_narrator() -> Generator[mock.MagicMock, Any, None]:
    """Mock out the Narrator for a test, replacing the old one afterwards."""
    mock_narrator = mock.create_autospec(Narrator, instance=True)
    old_narrator = pacing.the_narrator
    pacing.the_narrator = mock_narrator

    yield mock_narrator

    pacing.the_narrator = old_narrator
