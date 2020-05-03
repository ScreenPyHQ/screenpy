"""
Actors are the stars of the show. They perform your actions, ask questions
about the state of the application, and assert resolutions, all in the
service of perfoming their roles. You can give a curtain call for a new
actor like so:

    Perry = AnActor.named("Perry")
"""


from random import choice
from typing import Any, List, Text, Tuple

from hamcrest import assert_that

from .exceptions import UnableToPerform
from .pacing import aside

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

# For type-hinting
Ability = Any
Action = Any
Question = Any
Resolution = Any


class Actor:
    """
    Represents an actor, holding their name and abilities. Actors are the
    performers of your screenplay, they represent your users as they go
    about their business on your product.

    An actor is meant to be instantiated using its static |Actor.named|
    method. A typical invocation might look like:

        Perry = Actor.named("Perry")

    This will create the actor, ready to take on their first role.
    """

    name: str
    abilities: List[Ability]

    @staticmethod
    def named(name: Text) -> "Actor":
        """
        Name this actor.

        Args:
            name: the name of this new Actor.

        Returns:
            |Actor|
        """
        aside(choice(ENTRANCE_DIRECTIONS).format(actor=name))
        return Actor(name)

    def who_can(self, *abilities: Ability) -> "Actor":
        """
        Add one or more abilities to this actor.

        Args:
            abilities: The abilities this actor can use.

        Returns:
            |Actor|
        """
        self.abilities.extend(abilities)
        return self

    can = who_can

    def uses_ability_to(self, ability: Ability) -> Ability:
        """
        Find the ability referenced and return it, if the actor is capable.

        Args:
            ability: the ability to retrieve.

        Returns:
            The requested ability.

        Raises:
            |UnableToPerform|: the actor doesn't possess the ability.
        """
        for a in self.abilities:
            if isinstance(a, ability):
                return a

        raise UnableToPerform(f"{self} does not have the ability to {ability}")

    ability_to = uses_ability_to

    def attempts_to(self, *actions: Action) -> None:
        """
        Perform a list of actions, one after the other.

        Args:
            actions: the list of actions to perform.
        """
        for action in actions:
            self.perform(action)

    was_able_to = attempts_to

    def perform(self, action: Action) -> None:
        """
        Perform the given action.

        Args:
            action: the |Action| to perform.
        """
        action.perform_as(self)

    def should_see_the(self, *tests: Tuple[Question, Resolution]) -> None:
        """
        Ask a series of questions, asserting their expected answers.

        Args:
            tests: tuples of a |Question| and a |Resolution|.

        Raises:
            AssertionError: If the question's actual answer does not match
                the expected answer from the |Resolution|.
        """
        for question, test in tests:
            assert_that(question.answered_by(self), test)

    should_see = should_see_that = should_see_the

    def exit(self) -> None:
        """
        Direct the actor to forget all their abilities, ready to assume a new
        role when their next cue calls them.
        """
        for ability in self.abilities:
            ability.forget()
            self.abilities.remove(ability)

    exit_stage_left = exit_stage_right = exit_through_vomitorium = exit

    def __repr__(self) -> str:
        return self.name

    def __init__(self, name: str) -> None:
        self.name = name
        self.abilities = []
