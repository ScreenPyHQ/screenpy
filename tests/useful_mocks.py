from typing import Any
from unittest import mock

from screenpy import BaseResolution
from unittest_protocols import Ability, Action, Question


def get_mock_action_class() -> Any:
    class FakeAction(Action):
        def __new__(cls, *args, **kwargs):
            rt = mock.create_autospec(FakeAction, instance=True)
            rt.describe.return_value = None
            return rt
    return FakeAction


def get_mock_question_class() -> Any:
    class FakeQuestion(Question):
        def __new__(cls, *args, **kwargs):
            rt = mock.create_autospec(Question, instance=True)
            rt.describe.return_value = None
            rt.answered_by.return_value = True
            return rt
    return FakeQuestion


def get_mock_resolution_class() -> Any:
    class FakeResolution(BaseResolution):
        def __new__(cls, *args, **kwargs):
            rt = mock.create_autospec(BaseResolution, instance=True)
            return rt
    return FakeResolution


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
