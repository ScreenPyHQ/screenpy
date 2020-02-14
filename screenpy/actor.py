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

from .exceptions import ScreenPyError
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


class UnableToPerformError(ScreenPyError):
    """
    Raised when an actor does not have the ability to perform the
    action they attempted.
    """


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
        Names this actor, logs their entrance, and returns the instance.

        Args:
            name: the name of this new Actor.

        Returns:
            |Actor|
        """
        aside(choice(ENTRANCE_DIRECTIONS).format(actor=name))
        return Actor(name)

    def who_can(self, *abilities: Ability) -> "Actor":
        """
        Adds an ability to this actor.

        Args:
            abilities: The abilities this actor can do.

        Returns:
            |Actor|
        """
        self.abilities.extend(abilities)
        return self

    def can(self, *abilities: Ability) -> "Actor":
        """Syntactic sugar for |Actor.who_can|."""
        return self.who_can(*abilities)

    def uses_ability_to(self, ability: Ability) -> Ability:
        """
        Finds the ability referenced and returns it, if the actor is able
        to do it.

        Args:
            ability: the ability to retrieve.

        Returns:
            The requested ability.

        Raises:
            |UnableToPerformError|: the actor doesn't possess the ability.
        """
        for a in self.abilities:
            if isinstance(a, ability):
                return a

        raise UnableToPerformError(f"{self} does not have the ability to {ability}")

    def ability_to(self, ability: Ability) -> Ability:
        """Syntactic sugar for |Actor.uses_ability_to|."""
        return self.uses_ability_to(ability)

    def attempts_to(self, *actions: Action) -> None:
        """
        Performs a list of actions, one after the other.

        Args:
            actions: the list of actions to perform.
        """
        for action in actions:
            self.perform(action)

    def was_able_to(self, *actions: Action) -> None:
        """Syntactic sugar for |Actor.attempts_to|."""
        return self.attempts_to(*actions)

    def perform(self, action: Action) -> None:
        """
        Performs the given action.

        Args:
            action: the |Action| to perform.
        """
        action.perform_as(self)

    def should_see_the(self, *tests: Tuple[Question, Resolution]) -> None:
        """
        Asks a series of questions, asserting that the expected answer
        resolves.

        Args:
            tests: tuples of a |Question| and a |Resolution|.

        Raises:
            AssertionError: If the question's actual answer does not match
                the expected answer from the |Resolution|.
        """
        for question, test in tests:
            assert_that(question.answered_by(self), test)

    def should_see_that(self, *tests: Tuple[Question, Resolution]) -> None:
        """Syntactic sugar for |Actor.should_see_the|."""
        return self.should_see_the(*tests)

    def should_see(self, *tests: Tuple[Question, Resolution]) -> None:
        """Syntactic sugar for |Actor.should_see_the|."""
        return self.should_see_the(*tests)

    def exit(self) -> None:
        """
        The actor forgets all of their abilities, ready to assume a new
        role when their next cue calls them.
        """
        for ability in self.abilities:
            ability.forget()
            self.abilities.remove(ability)

    def exit_stage_right(self) -> None:
        """Syntactic sugar for |Actor.exit|."""
        aside(f"{self} bows and exits, stage right.")
        self.exit()

    def exit_stage_left(self) -> None:
        """Syntactic sugar for |Actor.exit|."""
        aside(f"{self} bows and exits, stage left.")
        self.exit()

    def __repr__(self) -> str:
        return self.name

    def __init__(self, name: str) -> None:
        self.name = name
        self.abilities = []
