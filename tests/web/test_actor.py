from unittest import mock

import pytest

from screenpy import Actor, AnActor
from screenpy.exceptions import UnableToPerform


def test_can_be_instantiated():
    """Actor can be instantiated"""
    a1 = Actor.named("test")
    a2 = Actor.named("test").can(None)
    a3 = Actor.named("test").who_can(None)
    a4 = AnActor.named("test")

    assert isinstance(a1, Actor)
    assert isinstance(a2, Actor)
    assert isinstance(a3, Actor)
    assert isinstance(a4, Actor)


def test_complains_for_missing_abilities():
    """Actors throw an exception if they are missing an ability"""
    actor = AnActor.named("Tester")

    with pytest.raises(UnableToPerform):
        actor.ability_to(1)


def test_remembers_abilities():
    """Actors remember abilities granted to them"""
    ability = 1
    actor = Actor.named("test").who_can(ability)

    assert actor.ability_to(int) is ability


def test_forgets_abilities_when_exiting():
    """Actors forget their abilities when they exit"""
    mocked_ability = mock.Mock()
    mocked_ability.forget = mock.Mock()
    actor = Actor.named("test").who_can(mocked_ability)

    actor.exit()

    mocked_ability.forget.assert_called_once()
    assert len(actor.abilities) == 0
