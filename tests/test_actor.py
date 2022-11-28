import warnings

import pytest

from screenpy import Actor, and_, given, given_that, then, when
from screenpy.exceptions import UnableToPerform
from useful_mocks import get_mock_task, get_mock_ability_class, get_mock_action_class

FakeAction = get_mock_action_class()
FakeAbility = get_mock_ability_class()
AnotherFakeAbility = get_mock_ability_class()


def test_can_be_instantiated() -> None:
    a1 = Actor.named("Tester")
    a2 = Actor.named("Tester").can(FakeAbility())
    a3 = Actor.named("Tester").who_can(FakeAbility())
    a4 = Actor.named("Tester").who_can(FakeAbility()).with_ordered_cleanup_tasks(FakeAction())

    assert isinstance(a1, Actor)
    assert isinstance(a2, Actor)
    assert isinstance(a3, Actor)
    assert isinstance(a4, Actor)


def test_calls_perform_as() -> None:
    action = FakeAction()
    actor = Actor.named("Tester")

    actor.attempts_to(action)

    action.perform_as.assert_called_once_with(actor)

    actor.should(action)
    actor.was_able_to(action)
    assert action.perform_as.call_count == 3


def test_complains_for_missing_abilities() -> None:
    actor = Actor.named("Tester")

    with pytest.raises(UnableToPerform):
        actor.ability_to(FakeAbility)


def test_has_ability() -> None:
    actor = Actor.named("Tester").who_can(FakeAbility())

    assert actor.has_ability_to(FakeAbility)
    assert not actor.has_ability_to(AnotherFakeAbility)


def test_find_abilities() -> None:
    ability = FakeAbility()
    actor = Actor.named("Tester").who_can(ability)

    assert actor.ability_to(FakeAbility) is ability


def test_performs_cleanup_tasks_when_exiting() -> None:
    mocked_ordered_task = get_mock_task()
    mocked_independent_task = get_mock_task()
    actor = Actor.named("Tester").with_ordered_cleanup_tasks(mocked_ordered_task)
    actor.has_independent_cleanup_tasks(mocked_independent_task)

    actor.exit()

    mocked_ordered_task.perform_as.assert_called_once_with(actor)
    mocked_independent_task.perform_as.assert_called_once_with(actor)
    assert len(actor.ordered_cleanup_tasks) == 0
    assert len(actor.independent_cleanup_tasks) == 0


def test_assert_has_cleanup_tasks_is_deprecated() -> None:
    actor = Actor.named("Tester")

    with warnings.catch_warnings(record=True) as w:
        actor.has_cleanup_tasks(FakeAction())

    assert issubclass(w[-1].category, DeprecationWarning)
    assert "has_ordered_cleanup_tasks" in str(w[-1])
    assert "has_independent_cleanup_tasks" in str(w[-1])


def test_clears_cleanup_tasks() -> None:
    mocked_task = get_mock_task()
    mocked_task_with_exception = get_mock_task()
    mocked_task_with_exception.perform_as.side_effect = ValueError(
        "I will not buy this record, it is scratched."
    )
    actor1 = Actor.named("Tester").with_ordered_cleanup_tasks(mocked_task)
    actor1.has_independent_cleanup_tasks(mocked_task)
    actor2 = Actor.named("Tester").with_ordered_cleanup_tasks(
        mocked_task_with_exception
    )
    actor2.has_independent_cleanup_tasks(mocked_task_with_exception)

    actor1.cleans_up()
    with pytest.raises(ValueError):
        actor2.cleans_up()

    assert len(actor1.ordered_cleanup_tasks) == 0
    assert len(actor2.ordered_cleanup_tasks) == 0
    assert len(actor1.independent_cleanup_tasks) == 0
    assert len(actor2.independent_cleanup_tasks) == 0


def test_ordered_cleanup_stops_at_first_exception() -> None:
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


def test_independent_cleanup_continues_through_exceptions() -> None:
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


def test_forgets_abilities_when_exiting() -> None:
    mocked_ability = FakeAbility()
    actor = Actor.named("Tester").who_can(mocked_ability)

    actor.exit_stage_left()

    mocked_ability.forget.assert_called_once()
    assert len(actor.abilities) == 0


def test_exit_stage_right() -> None:
    mocked_ability = FakeAbility()
    actor = Actor.named("Tester").who_can(mocked_ability)

    actor.exit_stage_right()

    mocked_ability.forget.assert_called_once()


def test_exit_through_vomitorium() -> None:
    mocked_ability = FakeAbility()
    actor = Actor.named("Tester").who_can(mocked_ability)

    actor.exit_through_vomitorium()

    mocked_ability.forget.assert_called_once()


def test_directives(Tester) -> None:
    assert given(Tester) == Tester
    assert given_that(Tester) == Tester
    assert when(Tester) == Tester
    assert then(Tester) == Tester
    assert and_(Tester) == Tester
