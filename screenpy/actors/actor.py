from random import choice
from typing import List, Tuple

from hamcrest import assert_that

from ..pacing import aside, TRIVIAL
from .entrance_lines import ENTRANCE_DIRECTIONS


class UnableToPerformException(Exception):
    pass


class Actor(object):
    """
    Represents an actor, holding their name and abilities. Actors are the
    performers of your screenplay, they represent your users as they go
    about their business on your product.

    An actor is meant to be instantiated using its static
    :meth:`|Actor|.named` method. A typical invocation might look like:

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
            :class:`|Actor|`
        """
        aside(choice(ENTRANCE_DIRECTIONS).format(name), gravitas=TRIVIAL)
        return Actor(name)

    def can(self, *abilities: List["ability"]) -> "Actor":
        """
        Adds an ability to this actor.

        Args:
            abilities (list(ability)): The abilities this actor can do.

        Returns:
            :class:`|Actor|`
        """
        self.abilities.extend(abilities)
        return self

    def who_can(self, *abilities: List["ability"]) -> "Actor":
        """Syntactic sugar for :meth:`|Actor|.can`."""
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
            UnableToPerformException: if this actor is unable.
        """
        for a in self.abilities:
            if isinstance(a, ability):
                return a
        else:
            raise UnableToPerformException(
                "{} cannot perform the ability {}".format(self, ability)
            )

    def uses_ability_to(self, ability: "Ability") -> "Ability":
        """Syntactic sugar for :meth:`|Actor|.ability_to`."""
        return self.ability_to(ability)

    def attempts_to(self, *tasks: List["task"]) -> None:
        """
        Performs a list of tasks, one after the other.

        Args:
            tasks (list(task)): The list of tasks to perform.
        """
        for task in tasks:
            self.perform(task)

    def was_able_to(self, *tasks: List["Task"]) -> None:
        """Syntactic sugar for :meth:`|Actor|.attempts_to`."""
        return self.attempts_to(*tasks)

    def perform(self, task: "Task") -> None:
        """
        Performs the given task.

        Args:
            task (list(Task)): The task to perform.
        """
        task.perform_as(self)

    def should_see_that(self, *tests: List[Tuple["Question", "Resolution"]]) -> None:
        """
        Asks a series of questions, asserting that the expected answer
        resolves.

        Args:
            tests list(tuple(Question, Resolution)): A list of tuples of
                questions and :class:`|Resolution|`s.

        Raises:
            AssertionError: If the question's actual answer does not match
                the expected answer from the :class:`|Resolution|`.
        """
        for question, test in tests:
            assert_that(question.answered_by(self), test)

    def should_see_the(self, *tests: List[Tuple["Question", "Resolution"]]) -> None:
        """Syntactic sugar for :meth:`|Actor|.should_see_that`."""
        return self.should_see_that(*tests)

    def should_see(self, *tests: List[Tuple["Question", "Resolution"]]) -> None:
        """Syntactic sugar for :meth:`|Actor|.should_see_that`."""
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
        """Syntactic sugar for :meth:`|Actor|.exit`."""
        aside("{} bows and exits, stage right.".format(self), gravitas=TRIVIAL)
        self.exit()

    def exit_stage_left(self) -> None:
        """Syntactic sugar for :meth:`|Actor|.exit`."""
        aside("{} bows and exits, stage left.".format(self), gravitas=TRIVIAL)
        self.exit()

    def __repr__(self) -> str:
        return self.name

    def __init__(self, name: str) -> None:
        self.name = name
        self.abilities = []


# Natural-language-enabling syntactic sugar
AnActor = Actor
