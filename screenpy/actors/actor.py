from random import choice
from typing import List, Tuple

from hamcrest import assert_that

from ..pacing import aside, TRIVIAL
from .entrance_lines import ENTRANCE_DIRECTIONS


class UnableToPerformException(Exception):
    """
    Raised when an actor does not possess the ability to perform the
    action they attempted.
    """

    pass


class Actor:
    """
    Represents an actor, holding their name and abilities. Actors are the
    performers of your screenplay, they represent your users as they go
    about their business on your product.

    An actor is meant to be instantiated using its static |Actor.named|
    method. A typical invocation might look like:

        perry = Actor.named("Perry")

    This will create the actor, ready to take on their first role.
    """

    @staticmethod
    def named(name: str) -> "Actor":
        """
        Names this actor, logs their entrance, and returns the instance.

        Args:
            name (str): The name of this new Actor.

        Returns:
            |Actor|
        """
        aside(choice(ENTRANCE_DIRECTIONS).format(name), gravitas=TRIVIAL)
        return Actor(name)

    def can(self, *abilities: List["ability"]) -> "Actor":
        """
        Adds an ability to this actor.

        Args:
            abilities (list(ability)): The abilities this actor can do.

        Returns:
            |Actor|
        """
        self.abilities.extend(abilities)
        return self

    def who_can(self, *abilities: List["ability"]) -> "Actor":
        """Syntactic sugar for |Actor.can|."""
        return self.can(*abilities)

    def ability_to(self, ability: "ability") -> "ability":
        """
        Finds the ability referenced and returns it, if the actor is able
        to do it.

        Args:
            ability (Ability): The ability to perform.

        Returns:
            The requested ability.

        Raises:
            |UnableToPerformException|: if this actor is unable.
        """
        for a in self.abilities:
            if isinstance(a, ability):
                return a
        else:
            raise UnableToPerformException(
                "{} does not have the ability to {}".format(self, ability)
            )

    def uses_ability_to(self, ability: "Ability") -> "Ability":
        """Syntactic sugar for |Actor.ability_to|."""
        return self.ability_to(ability)

    def attempts_to(self, *actions: List["Action"]) -> None:
        """
        Performs a list of actions, one after the other.

        Args:
            actions (list(Action)): The list of actions to perform.
        """
        for action in actions:
            self.perform(action)

    def was_able_to(self, *actions: List["Action"]) -> None:
        """Syntactic sugar for |Actor.attempts_to|."""
        return self.attempts_to(*actions)

    def perform(self, action: "Action") -> None:
        """
        Performs the given action.

        Args:
            action (list(Action)): The |Action| to perform.
        """
        action.perform_as(self)

    def should_see_that(self, *tests: List[Tuple["Question", "Resolution"]]) -> None:
        """
        Asks a series of questions, asserting that the expected answer
        resolves.

        Args:
            tests list(tuple(Question, Resolution)): A list of tuples of
                a question and a |Resolution|.

        Raises:
            AssertionError: If the question's actual answer does not match
                the expected answer from the |Resolution|.
        """
        for question, test in tests:
            assert_that(question.answered_by(self), test)

    def should_see_the(self, *tests: List[Tuple["Question", "Resolution"]]) -> None:
        """Syntactic sugar for |Actor.should_see_that|."""
        return self.should_see_that(*tests)

    def should_see(self, *tests: List[Tuple["Question", "Resolution"]]) -> None:
        """Syntactic sugar for |Actor.should_see_that|."""
        return self.should_see_that(*tests)

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
        aside("{} bows and exits, stage right.".format(self), gravitas=TRIVIAL)
        self.exit()

    def exit_stage_left(self) -> None:
        """Syntactic sugar for |Actor.exit|."""
        aside("{} bows and exits, stage left.".format(self), gravitas=TRIVIAL)
        self.exit()

    def __repr__(self) -> str:
        return self.name

    def __init__(self, name: str) -> None:
        self.name = name
        self.abilities = []


# Natural-language-enabling syntactic sugar
AnActor = Actor
