from unittest import mock, TestCase

from screenpy.actor import Actor, AnActor


class TestActor(TestCase):
    def test_can_be_instantiated(self):
        """Actor can be instantiated"""
        a1 = Actor.named("test")
        a2 = Actor.named("test").can(None)
        a3 = Actor.named("test").who_can(None)
        a4 = AnActor.named("test")

        self.assertIsInstance(a1, Actor)
        self.assertIsInstance(a2, Actor)
        self.assertIsInstance(a3, Actor)
        self.assertIsInstance(a4, Actor)

    def test_remembers_abilities(self):
        """Actors remember abilities granted to them"""
        ability = 1
        actor = Actor.named("test").who_can(ability)

        self.assertEqual(actor.ability_to(int), ability)

    def test_forgets_abilities_when_exiting(self):
        """Actors forget their abilities when they exit."""
        ability = mock.MagicMock()
        ability.forget = mock.Mock()

        actor = Actor.named("test").who_can(ability)
        actor.exit()

        ability.forget.assert_called_once()
        self.assertEqual(len(actor.abilities), 0)
