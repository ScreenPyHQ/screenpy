from unittest import mock

from screenpy.actions import Debug
from screenpy.resolutions import BaseResolution
from tests.unittest_protocols import Ability, Action, Question


def get_mock_action(**kwargs):
    mock_action = mock.create_autospec(Debug(), _name="fakeaction", instance=True)
    mock_action.perform_as = mock.create_autospec(Debug().perform_as, **kwargs)
    mock_action.describe.return_value = "An African or a European swallow?"
    return mock_action


def get_mock_question():
    return mock.create_autospec(Question, instance=True)


def get_mock_resolution():
    return mock.create_autospec(BaseResolution, instance=True)


def get_mock_task():
    """Get a describable mock task."""
    task = mock.create_autospec(Action, instance=True)
    task.describe.return_value = "A mocked task."
    return task


def get_mock_ability():
    return mock.create_autospec(Ability, instance=True)
