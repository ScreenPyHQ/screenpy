"""
Actors are the stars of the show. They perform your Actions, ask Questions
about the state of the application, and assert Resolutions, all in the
service of perfoming their roles.
"""

import warnings
from random import choice
from typing import List, Type, TypeVar

from .exceptions import UnableToPerform
from .pacing import aside
from .protocols import Forgettable, Performable
from .speech_tools import get_additive_description

# pylint: disable=too-many-public-methods

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

T_Ability = TypeVar("T_Ability", bound=Forgettable)
SelfActor = TypeVar("SelfActor", bound="Actor")


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
    def named(cls: Type[SelfActor], name: str) -> SelfActor:
        """Give a name to this Actor."""
        aside(choice(ENTRANCE_DIRECTIONS).format(actor=name))
        return cls(name)

    def who_can(self: SelfActor, *abilities: T_Ability) -> SelfActor:
        """Add one or more Abilities to this Actor.

        Aliases:
            * :meth:`~screenpy.actor.Actor.can`
        """
        self.abilities.extend(abilities)
        return self

    def can(self: SelfActor, *abilities: T_Ability) -> SelfActor:
        """Alias for :meth:`~screenpy.actor.Actor.who_can`."""
        return self.who_can(*abilities)

    def has_cleanup_tasks(self: SelfActor, *tasks: Performable) -> SelfActor:
        """Assign one or more tasks to the Actor to perform when exiting."""
        warnings.warn(
            "This method is deprecated and will be removed in ScreenPy 4.2.0."
            " Please use either `has_ordered_cleanup_tasks`"
            " or `has_independent_cleanup_tasks` instead.",
            DeprecationWarning,
        )
        return self.has_ordered_cleanup_tasks(*tasks)

    def has_ordered_cleanup_tasks(self: SelfActor, *tasks: Performable) -> SelfActor:
        """Assign one or more tasks for the Actor to perform when exiting.

        The tasks given to this method must be performed successfully in
        order. If any task fails, any subsequent tasks will not be attempted
        and will be discarded.

        Aliases:
            * :meth:`~screenpy.actor.Actor.with_ordered_cleanup_tasks`
        """
        self.ordered_cleanup_tasks.extend(tasks)
        return self

    def with_ordered_cleanup_tasks(self: SelfActor, *tasks: Performable) -> SelfActor:
        """Alias for :meth:`~screenpy.actor.Actor.has_ordered_cleanup_tasks`."""
        return self.has_ordered_cleanup_tasks(*tasks)

    def has_independent_cleanup_tasks(
        self: SelfActor, *tasks: Performable
    ) -> SelfActor:
        """Assign one or more tasks for the Actor to perform when exiting.

        The tasks included through this method are assumed to be independent;
        that is to say, all of them will be executed regardless of whether
        previous ones were successful.

        Aliases:
            * :meth:`~screenpy.actor.Actor.with_independent_cleanup_tasks`
        """
        self.independent_cleanup_tasks.extend(tasks)
        return self

    def with_independent_cleanup_tasks(
        self: SelfActor, *tasks: Performable
    ) -> SelfActor:
        """Alias for :meth:`~screenpy.actor.Actor.has_independent_cleanup_tasks`."""
        return self.has_independent_cleanup_tasks(*tasks)

    def uses_ability_to(self: SelfActor, ability: Type[T_Ability]) -> T_Ability:
        """Find the Ability referenced and return it, if the Actor is capable.

        Raises:
            UnableToPerform: the Actor doesn't possess the Ability.

        Aliases:
            * :meth:`~screenpy.actor.Actor.ability_to`
        """
        for a in self.abilities:
            if isinstance(a, ability):
                return a

        raise UnableToPerform(f"{self} does not have the Ability to {ability}")

    def ability_to(self: SelfActor, ability: Type[T_Ability]) -> T_Ability:
        """Alias for :meth:`~screenpy.actor.Actor.uses_ability_to`."""
        return self.uses_ability_to(ability)

    def has_ability_to(self: SelfActor, ability: Type[T_Ability]) -> bool:
        """Ask whether the Actor has the Ability to do something."""
        try:
            self.ability_to(ability)
            return True
        except UnableToPerform:
            return False

    def attempts_to(self: SelfActor, *actions: Performable) -> None:
        """Perform a list of Actions, one after the other.

        Aliases:
            * :meth:`~screenpy.actor.Actor.was_able_to`
            * :meth:`~screenpy.actor.Actor.should`
        """
        for action in actions:
            self.perform(action)

    def was_able_to(self: SelfActor, *actions: Performable) -> None:
        """Alias for :meth:`~screenpy.actor.Actor.attempts_to`, for test setup."""
        return self.attempts_to(*actions)

    def should(self: SelfActor, *actions: Performable) -> None:
        """Alias for :meth:`~screenpy.actor.Actor.attempts_to`, for test assertions."""
        return self.attempts_to(*actions)

    def perform(self: SelfActor, action: Performable) -> None:
        """Perform an Action."""
        action.perform_as(self)

    def cleans_up_ordered_tasks(self: SelfActor) -> None:
        """Perform ordered clean-up tasks."""
        try:
            for task in self.ordered_cleanup_tasks:
                self.perform(task)
        finally:
            self.ordered_cleanup_tasks = []

    def cleans_up_independent_tasks(self: SelfActor) -> None:
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

    def cleans_up(self: SelfActor) -> None:
        """Perform any scheduled clean-up tasks."""
        self.cleans_up_independent_tasks()
        self.cleans_up_ordered_tasks()

    def exit(self: SelfActor) -> None:
        """Direct the Actor to forget all their Abilities.

        Aliases:
            * :meth:`~screenpy.actor.Actor.exit_stage_left`
            * :meth:`~screenpy.actor.Actor.exit_stage_right`
            * :meth:`~screenpy.actor.Actor.exit_through_vomitorium`
        """
        self.cleans_up()
        for ability in self.abilities:
            ability.forget()
        self.abilities = []

    def exit_stage_left(self: SelfActor) -> None:
        """Alias for :meth:`~screenpy.actor.Actor.exit`."""
        return self.exit()

    def exit_stage_right(self: SelfActor) -> None:
        """Alias for :meth:`~screenpy.actor.Actor.exit`."""
        return self.exit()

    def exit_through_vomitorium(self: SelfActor) -> None:
        """Alias for :meth:`~screenpy.actor.Actor.exit`."""
        return self.exit()

    def __repr__(self: SelfActor) -> str:
        return self.name

    def __init__(self: SelfActor, name: str) -> None:
        self.name = name
        self.abilities = []
        self.ordered_cleanup_tasks = []
        self.independent_cleanup_tasks = []
