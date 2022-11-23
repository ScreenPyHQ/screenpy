from typing import Any
from unittest import mock

from screenpy.actions import Debug
from screenpy.resolutions import BaseResolution
from unittest_protocols import Ability, Action, Question


def get_mock_action(**kwargs) -> mock.Mock:
    mock_action = mock.create_autospec(Debug(), _name="fakeaction", instance=True)
    mock_action.perform_as = mock.create_autospec(Debug().perform_as, **kwargs)
    mock_action.describe.return_value = "An African or a European swallow?"
    return mock_action


def get_mock_question() -> mock.Mock:
    question = mock.create_autospec(Question, instance=True)
    question.describe.return_value = "Description of Mocked Question"
    question.answered_by.return_value = True
    return question


def get_mock_resolution() -> mock.Mock:
    return mock.create_autospec(BaseResolution, instance=True)


def get_mock_task() -> mock.Mock:
    """Get a describable mock task."""
    task = mock.create_autospec(Action, instance=True)
    task.describe.return_value = "A mocked task."
    return task


def get_mock_ability_class() -> Any:
    """
    This bit of wizardry creates a subclass of Ability that is auto_specced by mock, but
    still allows for usage in cases where `isinstance` is called without raising exceptions

        MyFakeAbility = get_mock_ability_class()
        fa = MyFakeAbility()
        isinstance(fa, MyFakeAbility)
        fa.forget()
        fa.forget.assert_called_once()

        A = get_mock_ability_class()
        B = get_mock_ability_class()
        a = A()
        b = B()
        a != b
    """
    class FakeAbility(Ability):
        def __new__(cls, *args, **kwargs):
            return mock.create_autospec(FakeAbility, *args, **kwargs)
    return FakeAbility
