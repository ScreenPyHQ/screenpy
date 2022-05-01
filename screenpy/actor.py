"""
Actors are the stars of the show. They perform your Actions, ask Questions
about the state of the application, and assert Resolutions, all in the
service of perfoming their roles.
"""

import warnings
from random import choice
from typing import List, Text, Type, TypeVar

from .exceptions import UnableToPerform
from .pacing import aside
from .protocols import Forgettable, Performable
from .speech_tools import get_additive_description

ENTRANCE_DIRECTIONS = [
    "{actor} appears from behind the backdrop!",
    "{actor} arrives on stage!",
    "{actor} enters the frame!",
    "{actor} enters, from the vomitorium!",
    "{actor} enters, on a wire!",
    "{actor} enters, stage left!",
    "{actor} enters, stage right!",
    "{actor} gets over their stagefright!",
    "{actor} hears their cue!",
    "{actor} is ready for their close-up!",
    "{actor} makes their debut!",
    "The camera jump-cuts to {actor}!",
    "The camera pans to {actor}!",
    "The curtain rises to reveal {actor}!",
    "The spotlight shines on {actor}!",
]

T = TypeVar("T")


class Actor:
    """Represents an Actor, holding their name and Abilities.

    Actors are the performers of your screenplay. They represent your users as
    they go about their business using your product.

    Examples::

        Perry = Actor.named("Perry")
    """

    abilities: List[Forgettable]
    ordered_cleanup_tasks: List[Performable]
    independent_cleanup_tasks: List[Performable]

    @classmethod
    def named(cls, name: Text) -> "Actor":
        """Give a name to this Actor."""
        aside(choice(ENTRANCE_DIRECTIONS).format(actor=name))
        return cls(name)

    def who_can(self, *abilities: Forgettable) -> "Actor":
        """Add one or more Abilities to this Actor."""
        self.abilities.extend(abilities)
        return self

    can = who_can

    def has_cleanup_tasks(self, *tasks: Performable) -> "Actor":
        """Assign one or more tasks to the Actor to perform when exiting."""
        warnings.warn(
            "This method is deprecated."
            " Please use either `has_ordered_cleanup_tasks`"
            " or `has_independent_cleanup_tasks` instead.",
            DeprecationWarning,
        )
        return self.has_ordered_cleanup_tasks(*tasks)

    def has_ordered_cleanup_tasks(self, *tasks: Performable) -> "Actor":
        """Assign one or more tasks for the Actor to perform when exiting.

        The tasks given to this method must be performed successfully in
        order. If any task fails, any subsequent tasks will not be attempted
        and will be discarded.
        """
        self.ordered_cleanup_tasks.extend(tasks)
        return self

    has_cleanup_task = has_ordered_cleanup_tasks
    with_cleanup_task = with_ordered_cleanup_tasks = has_ordered_cleanup_tasks

    def has_independent_cleanup_tasks(self, *tasks: Performable) -> "Actor":
        """Assign one or more tasks for the Actor to perform when exiting.

        The tasks included through this method are assumed to be independent;
        that is to say, all of them will be executed regardless of whether
        previous ones were successful.
        """
        self.independent_cleanup_tasks.extend(tasks)
        return self

    with_independent_cleanup_tasks = has_independent_cleanup_tasks

    def uses_ability_to(self, ability: Type[T]) -> T:
        """Find the Ability referenced and return it, if the Actor is capable.

        Raises:
            UnableToPerform: the Actor doesn't possess the Ability.
        """
        for a in self.abilities:
            if isinstance(a, ability):
                return a

        raise UnableToPerform(f"{self} does not have the Ability to {ability}")

    ability_to = uses_ability_to

    def has_ability_to(self, ability: Type[Forgettable]) -> bool:
        """Ask whether the Actor has the Ability to do something."""
        try:
            self.ability_to(ability)
            return True
        except UnableToPerform:
            return False

    def attempts_to(self, *actions: Performable) -> None:
        """Perform a list of Actions, one after the other."""
        for action in actions:
            self.perform(action)

    was_able_to = should = attempts_to

    def perform(self, action: Performable) -> None:
        """Perform an Action."""
        action.perform_as(self)

    def cleans_up_ordered_tasks(self) -> None:
        """Perform ordered clean-up tasks."""
        try:
            for task in self.ordered_cleanup_tasks:
                self.perform(task)
        finally:
            self.ordered_cleanup_tasks = []

    def cleans_up_independent_tasks(self) -> None:
        """Perform independent clean-up tasks."""
        for task in self.independent_cleanup_tasks:
            try:
                self.perform(task)
            except Exception as e:  # pylint: disable=broad-except
                action = get_additive_description(task)
                msg = (
                    f"{self} encountered an error while attempting to {action}:"
                    f"\n    {e}"
                )
                aside(msg)

        self.independent_cleanup_tasks = []

    def cleans_up(self) -> None:
        """Perform any scheduled clean-up tasks."""
        self.cleans_up_independent_tasks()
        self.cleans_up_ordered_tasks()

    def exit(self) -> None:
        """Direct the Actor to forget all their Abilities."""
        self.cleans_up()
        for ability in self.abilities:
            ability.forget()
        self.abilities = []

    exit_stage_left = exit_stage_right = exit_through_vomitorium = exit

    def __repr__(self) -> str:
        return self.name

    def __init__(self, name: str) -> None:
        self.name = name
        self.abilities = []
        self.ordered_cleanup_tasks = []
        self.independent_cleanup_tasks = []
