"""
Actors are the stars of the show. They perform your actions, ask questions
about the state of the application, and assert resolutions, all in the
service of perfoming their roles.
"""

from random import choice
from typing import List, Text, Tuple, Type, TypeVar

from hamcrest import assert_that

from .exceptions import UnableToPerform
from .pacing import aside
from .protocols import Answerable, Forgettable, Performable
from .resolutions.base_resolution import BaseResolution

ENTRANCE_DIRECTIONS = [
    "{actor} arrives on stage!",
    "{actor} enters, from the vomitorium!",
    "{actor} enters, on a wire!",
    "{actor} enters, stage left!",
    "{actor} enters, stage right!",
    "{actor} enters the frame!",
    "{actor} gets over their stagefright!",
    "{actor} hears their cue!",
    "{actor} is ready for their close-up!",
    "{actor} makes their debut!",
    "The camera pans to {actor}!",
    "The camera jump-cuts to {actor}!",
]

T = TypeVar("T")


class Actor:
    """Represents an actor, holding their name and abilities.

    Actors are the performers of your screenplay, they represent your users as
    they go about their business using your product.

    Examples::

        Perry = Actor.named("Perry")
    """

    abilities: List[Forgettable]

    @staticmethod
    def named(name: Text) -> "Actor":
        """Give a name to this actor."""
        aside(choice(ENTRANCE_DIRECTIONS).format(actor=name))
        return Actor(name)

    def who_can(self, *abilities: Forgettable) -> "Actor":
        """Add one or more abilities to this actor."""
        self.abilities.extend(abilities)
        return self

    can = who_can

    def uses_ability_to(self, ability: Type[T]) -> T:
        """Find the ability referenced and return it, if the actor is capable.

        Raises:
            |UnableToPerform|: the actor doesn't possess the ability.
        """
        for a in self.abilities:
            if isinstance(a, ability):
                return a

        raise UnableToPerform(f"{self} does not have the ability to {ability}")

    ability_to = uses_ability_to

    def has_ability_to(self, ability: Type[Forgettable]) -> bool:
        """Ask whether the actor has the ability to do something."""
        try:
            self.ability_to(ability)
            return True
        except UnableToPerform:
            return False

    def attempts_to(self, *actions: Performable) -> None:
        """Perform a list of actions, one after the other."""
        for action in actions:
            self.perform(action)

    was_able_to = attempts_to

    def perform(self, action: Performable) -> None:
        """Perform an action."""
        action.perform_as(self)

    def should_see_the(self, *tests: Tuple[Answerable, BaseResolution]) -> None:
        """Ask a series of questions, asserting their resolutions.

        Raises:
            AssertionError: if any of the |Question| + |Resolution| pairs do
                not match.
        """
        for question, resolution in tests:
            assert_that(question.answered_by(self), resolution)

    should_see = should_see_that = should_see_the

    def should_see_any_of(self, *tests: Tuple[Answerable, BaseResolution]) -> None:
        """Ask a series of questions, at least one of which should be true.

        Raises:
            AssertionError: if none of the |Question| + |Resolution| pairs match.
        """
        none_passed = True
        for question, resolution in tests:
            try:
                assert_that(question.answered_by(self), resolution)
                none_passed = False
            except AssertionError:
                pass

        if none_passed:
            raise AssertionError(f"{self} did not find any expected answers!")

    def exit(self) -> None:
        """Direct the actor to forget all their abilities."""
        for ability in self.abilities:
            ability.forget()
            self.abilities.remove(ability)

    exit_stage_left = exit_stage_right = exit_through_vomitorium = exit

    def __repr__(self) -> str:
        return self.name

    def __init__(self, name: str) -> None:
        self.name = name
        self.abilities = []
