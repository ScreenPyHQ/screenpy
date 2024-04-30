"""The User stand-in!

Actors are the stars of the show. They perform your Actions, ask Questions
about the state of the application, and assert Resolutions, all in the
service of perfoming their roles.
"""

from __future__ import annotations

from random import choice
from typing import TYPE_CHECKING, TypeVar

from .exceptions import UnableToPerform
from .pacing import aside
from .protocols import Forgettable
from .speech_tools import get_additive_description

if TYPE_CHECKING:
    from typing_extensions import Self

    from .protocols import Performable

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


class Actor:
    """Represents an Actor, holding their name and Abilities.

    Actors are the performers of your screenplay. They represent your users as
    they go about their business using your product.

    Examples::

        Perry = Actor.named("Perry")
    """

    abilities: list[Forgettable]
    ordered_cleanup_tasks: list[Performable]
    independent_cleanup_tasks: list[Performable]

    @classmethod
    def named(cls, name: str) -> Self:
        """Give a name to this Actor."""
        aside(choice(ENTRANCE_DIRECTIONS).format(actor=name))
        return cls(name)

    def who_can(self, *abilities: T_Ability) -> Self:
        """Add one or more Abilities to this Actor.

        Aliases:
            * ``can``
        """
        self.abilities.extend(abilities)
        return self

    can = who_can

    def has_ordered_cleanup_tasks(self, *tasks: Performable) -> Self:
        """Assign one or more tasks for the Actor to perform when exiting.

        The tasks given to this method must be performed successfully in
        order. If any task fails, any subsequent tasks will not be attempted
        and will be discarded.

        Aliases:
            * ``with_ordered_cleanup_tasks``
        """
        self.ordered_cleanup_tasks.extend(tasks)
        return self

    with_ordered_cleanup_tasks = has_ordered_cleanup_tasks

    def has_independent_cleanup_tasks(self, *tasks: Performable) -> Self:
        """Assign one or more tasks for the Actor to perform when exiting.

        The tasks included through this method are assumed to be independent;
        that is to say, all of them will be executed regardless of whether
        previous ones were successful.

        Aliases:
            * ``with_independent_cleanup_tasks``
        """
        self.independent_cleanup_tasks.extend(tasks)
        return self

    with_independent_cleanup_tasks = has_independent_cleanup_tasks

    def uses_ability_to(self, ability: type[T_Ability]) -> T_Ability:
        """Find the Ability referenced and return it, if the Actor is capable.

        Raises:
            UnableToPerform: the Actor doesn't possess the Ability.

        Aliases:
            * ``ability_to``
        """
        for a in self.abilities:
            if isinstance(a, ability):
                return a

        msg = f"{self} does not have the Ability to {ability}"
        raise UnableToPerform(msg)

    ability_to = uses_ability_to

    def has_ability_to(self, ability: type[T_Ability]) -> bool:
        """Ask whether the Actor has the Ability to do something."""
        try:
            self.ability_to(ability)
        except UnableToPerform:
            return False
        else:
            return True

    def attempts_to(self, *actions: Performable) -> None:
        """Perform a list of Actions, one after the other.

        Aliases:
            * ``was_able_to``
            * ``did``
            * ``will``
            * ``tries_to``
            * ``tried_to``
            * ``tries``
            * ``tried``
            * ``does``
            * ``should``
            * ``shall``
        """
        for action in actions:
            self.perform(action)

    was_able_to = did = attempts_to
    tries_to = tried_to = tries = tried = does = will = attempts_to
    shall = should = attempts_to

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
            except Exception as e:  # noqa: BLE001
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
        """Direct the Actor to clean up and forget all their Abilities.

        Aliases:
            * ``exit_stage_left``
            * ``exit_stage_right``
            * ``exit_through_vomitorium``
        """
        self.cleans_up()
        for ability in self.abilities:
            ability.forget()
        self.abilities = []

    exit_stage_left = exit_stage_right = exit_through_vomitorium = exit

    def __call__(self, *actions: Performable) -> None:
        """Alias for :meth:`attempts_to`."""
        return self.attempts_to(*actions)

    def __repr__(self) -> str:
        """The name of the Actor represents them."""
        return self.name

    def __init__(self, name: str) -> None:
        self.name = name
        self.abilities = []
        self.ordered_cleanup_tasks = []
        self.independent_cleanup_tasks = []
