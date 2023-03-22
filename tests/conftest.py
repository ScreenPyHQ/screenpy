from typing import Any, Callable, Generator
from unittest import mock

import pytest

from screenpy import Actor, Narrator, pacing, settings


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
    old_narrator = Narrator._instance
    Narrator._instance = mock_narrator
    # update pacing since we forced a new instance of Narrator
    pacing.the_narrator = mock_narrator

    yield mock_narrator

    Narrator._instance = old_narrator
    pacing.the_narrator = old_narrator


def mock_settings(**new_settings) -> Callable:
    """Mock one or more settings for the duration of a test."""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            old_settings = {key: getattr(settings, key) for key in new_settings.keys()}
            for key, value in new_settings.items():
                setattr(settings, key, value)

            try:
                func(*args, **kwargs)
            finally:
                for key, value in old_settings.items():
                    setattr(settings, key, value)

        return wrapper

    return decorator
