from unittest import mock

import pytest

from screenpy import Actor
from screenpy.exceptions import UnableToPerform


def test_can_be_instantiated():
    a1 = Actor.named("Tester")
    a2 = Actor.named("Tester").can(None)
    a3 = Actor.named("Tester").who_can(None)
    a4 = Actor.named("Tester").who_can(None).with_cleanup_task(None)

    assert isinstance(a1, Actor)
    assert isinstance(a2, Actor)
    assert isinstance(a3, Actor)
    assert isinstance(a4, Actor)


def test_calls_perform_as():
    action = mock.Mock()
    actor = Actor.named("Tester")

    actor.attempts_to(action)

    action.perform_as.assert_called_once_with(actor)


def test_complains_for_missing_abilities():
    actor = Actor.named("Tester")

    with pytest.raises(UnableToPerform):
        actor.ability_to(1)


def test_has_ability():
    actor = Actor.named("Tester").who_can(1)

    assert actor.has_ability_to(int)
    assert not actor.has_ability_to(float)


def test_find_abilities():
    ability = 1
    actor = Actor.named("Tester").who_can(ability)

    assert actor.ability_to(int) is ability


def test_performs_cleanup_tasks_when_exiting():
    mocked_task = mock.Mock()
    actor = Actor.named("Tester").with_cleanup_task(mocked_task)

    actor.exit()

    mocked_task.perform_as.assert_called_once_with(actor)
    assert len(actor.cleanup_tasks) == 0


def test_clears_cleanup_tasks():
    mocked_task = mock.Mock()
    mocked_task_with_exception = mock.Mock()
    mocked_task_with_exception.perform_as.side_effect = ValueError(
        "I will not buy this record, it is scratched."
    )
    actor1 = Actor.named("Tester").with_cleanup_task(mocked_task)
    actor2 = Actor.named("Tester").with_cleanup_task(mocked_task_with_exception)

    actor1.cleans_up()
    with pytest.raises(ValueError):
        actor2.cleans_up()

    assert len(actor1.cleanup_tasks) == 0
    assert len(actor2.cleanup_tasks) == 0


def test_forgets_abilities_when_exiting():
    mocked_ability = mock.Mock()
    actor = Actor.named("Tester").who_can(mocked_ability)

    actor.exit()

    mocked_ability.forget.assert_called_once()
    assert len(actor.abilities) == 0
