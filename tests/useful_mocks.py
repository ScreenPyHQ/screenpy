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


def get_mock_ability() -> mock.Mock:
    return mock.create_autospec(Ability, instance=True)


class FakeAbility:
    def forget(self):
        return


class AnotherFakeAbility:
    def forget(self):
        return


class FakeQuestion:
    def answered_by(self, the_actor) -> bool:
        return True

    def describe(self) -> str:
        return "Fake question"
