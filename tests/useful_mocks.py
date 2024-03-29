from __future__ import annotations

from unittest import mock

from .unittest_protocols import Ability, Action, Question, Resolution


def get_mock_action_class() -> type:
    class FakeAction(Action):
        def __new__(cls) -> FakeAction:
            rt = mock.create_autospec(FakeAction, instance=True)
            rt.describe.return_value = "FakeAction"
            return rt

    return FakeAction


def get_mock_question_class() -> type:
    class FakeQuestion(Question):
        def __new__(cls) -> FakeQuestion:
            rt = mock.create_autospec(FakeQuestion, instance=True)
            rt.describe.return_value = "FakeQuestion"
            rt.answered_by.return_value = True
            return rt

    return FakeQuestion


def get_mock_resolution_class() -> type:
    class FakeResolution(Resolution):
        def __new__(cls) -> FakeResolution:
            rt = mock.create_autospec(FakeResolution, instance=True)
            rt.resolve.return_value = rt
            rt.describe.return_value = "FakeResolution"
            return rt

    return FakeResolution


def get_mock_ability_class() -> type:
    """Generate a mocked Ability class.

    This bit of wizardry creates a subclass of Ability that is auto_specced by
    mock, but still allows for usage in cases where `isinstance` is called
    without raising exceptions

    Examples::

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
        def __new__(cls) -> FakeAbility:
            return mock.create_autospec(FakeAbility)

    return FakeAbility
