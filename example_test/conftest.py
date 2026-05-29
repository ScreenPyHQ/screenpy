"""Fixtures for the example ScreenPy test suite."""

from collections.abc import Generator

import pytest

from screenpy import AnActor


@pytest.fixture
def Perry() -> Generator:
    """Provide an Actor named Perry for each test."""
    the_actor = AnActor.named("Perry")
    yield the_actor
    the_actor.exit()
