from unittest import mock

import pytest

from screenpy import AnActor
from screenpy.abilities import BrowseTheWeb


@pytest.fixture(scope="function")
def Tester():
    """
    Provides an actor with a mocked BrowseTheWeb ability.
    """
    BrowseTheWeb_Mocked = mock.Mock(spec=BrowseTheWeb)
    return AnActor.named("Tester").who_can(BrowseTheWeb_Mocked)
