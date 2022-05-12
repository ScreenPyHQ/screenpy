import warnings
from unittest import mock

import pytest

from screenpy import Actor
from screenpy.exceptions import UnableToPerform


def get_mock_task():
    """Get a describable mock task."""
    task = mock.Mock()
    task.describe.return_value = "A mocked task."
    return task


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
    mocked_ordered_task = get_mock_task()
    mocked_independent_task = get_mock_task()
    actor = Actor.named("Tester").with_cleanup_task(mocked_ordered_task)
    actor.has_independent_cleanup_tasks(mocked_independent_task)

    actor.exit()

    mocked_ordered_task.perform_as.assert_called_once_with(actor)
    mocked_independent_task.perform_as.assert_called_once_with(actor)
    assert len(actor.ordered_cleanup_tasks) == 0
    assert len(actor.independent_cleanup_tasks) == 0


def test_assert_has_cleanup_tasks_is_deprecated():
    actor = Actor.named("Tester")

    with warnings.catch_warnings(record=True) as w:
        actor.has_cleanup_tasks(None)

    assert issubclass(w[-1].category, DeprecationWarning)
    assert "has_ordered_cleanup_tasks" in str(w[-1])
    assert "has_independent_cleanup_tasks" in str(w[-1])


def test_clears_cleanup_tasks():
    mocked_task = get_mock_task()
    mocked_task_with_exception = get_mock_task()
    mocked_task_with_exception.perform_as.side_effect = ValueError(
        "I will not buy this record, it is scratched."
    )
    actor1 = Actor.named("Tester").with_cleanup_task(mocked_task)
    actor1.has_independent_cleanup_tasks(mocked_task)
    actor2 = Actor.named("Tester").with_cleanup_task(mocked_task_with_exception)
    actor2.has_independent_cleanup_tasks(mocked_task_with_exception)

    actor1.cleans_up()
    with pytest.raises(ValueError):
        actor2.cleans_up()

    assert len(actor1.ordered_cleanup_tasks) == 0
    assert len(actor2.ordered_cleanup_tasks) == 0
    assert len(actor1.independent_cleanup_tasks) == 0
    assert len(actor2.independent_cleanup_tasks) == 0


def test_ordered_cleanup_stops_at_first_exception():
    mocked_task = get_mock_task()
    mocked_task_with_exception = get_mock_task()
    mocked_task_with_exception.perform_as.side_effect = ValueError(
        "Good night, a-ding ding ding ding..."
    )
    actor1 = Actor.named("Tester").with_ordered_cleanup_tasks(
        mocked_task_with_exception, mocked_task
    )

    with pytest.raises(ValueError):
        actor1.cleans_up()

    mocked_task.perform_as.assert_not_called()


def test_independent_cleanup_continues_through_exceptions():
    mocked_task = get_mock_task()
    mocked_task_with_exception = get_mock_task()
    mocked_task_with_exception.perform_as.side_effect = ValueError(
        "Sir Robin ran away."
    )
    actor1 = Actor.named("Tester").with_independent_cleanup_tasks(
        mocked_task_with_exception, mocked_task
    )

    actor1.cleans_up()

    mocked_task_with_exception.perform_as.assert_called_once()
    mocked_task.perform_as.assert_called_once()


def test_forgets_abilities_when_exiting():
    mocked_ability = mock.Mock()
    actor = Actor.named("Tester").who_can(mocked_ability)

    actor.exit()

    mocked_ability.forget.assert_called_once()
    assert len(actor.abilities) == 0
