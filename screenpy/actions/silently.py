"""
Silently allows for "disabling" logging on successful actions & tests
"""
from __future__ import annotations

from typing import Any, TypeVar, Union, overload

from hamcrest.core.base_matcher import Matcher
from typing_extensions import TypeAlias

from screenpy.actor import Actor
from screenpy.configuration import settings
from screenpy.exceptions import NotAnswerable, NotPerformable, NotResolvable
from screenpy.pacing import the_narrator
from screenpy.protocols import Answerable, Performable, Resolvable

T = TypeVar("T")


class SilentlyMixin:
    """
    Silently needs to mimic the ducks (i.e. objects) they are wrapping.
    All of the attributes from the "duck" should be exposed by the Silently object.
    """

    def __getattr__(self, key: Any) -> Any:
        try:
            return getattr(self.duck, key)
        except AttributeError as exc:
            msg = (
                f"{self.__class__.__name__}({self.duck.__class__.__name__}) "
                f"has no attribute '{key}'"
            )
            raise AttributeError(msg) from exc


class SilentlyPerformable(Performable, SilentlyMixin):
    """Calls the Performable passed in but kinks the cable prior performing"""

    def perform_as(self, actor: Actor) -> None:
        with the_narrator.mic_cable_kinked():
            self.duck.perform_as(actor)
            if not settings.UNABRIDGED_NARRATION:
                the_narrator.clear_backup()
            return

    def __init__(self, duck: Performable):
        if not isinstance(duck, Performable):
            raise NotPerformable(
                "SilentlyPerformable only works with Performable. "
                "Use `Silently` instead."
            )
        self.duck = duck


class SilentlyAnswerable(Answerable, SilentlyMixin):
    """Calls the Answerable passed in but kinks the cable prior to answering"""

    def answered_by(self, actor: Actor) -> Any:
        with the_narrator.mic_cable_kinked():
            thing = self.duck.answered_by(actor)
            if not settings.UNABRIDGED_NARRATION:
                the_narrator.clear_backup()
            return thing

    def __init__(self, duck: Answerable):
        if not isinstance(duck, Answerable):
            raise NotAnswerable(
                "SilentlyAnswerable only works with Answerable. Use `Silently` instead."
            )
        self.duck = duck


class SilentlyResolvable(Resolvable, SilentlyMixin):
    """Calls the Resolvable passed in but kinks the cable prior to resolving"""

    def resolve(self) -> Matcher:
        with the_narrator.mic_cable_kinked():
            res = self.duck.resolve()
            if not settings.UNABRIDGED_NARRATION:
                the_narrator.clear_backup()
            return res

    def __init__(self, duck: Resolvable):
        if not isinstance(duck, Resolvable):
            raise NotResolvable(
                "SilentlyResolvable only works with Resolvable. Use `Silently` instead."
            )
        self.duck = duck


T_duck: TypeAlias = Union[
    Answerable,
    Performable,
    Resolvable,
]
T_silent_duck: TypeAlias = Union[
    SilentlyAnswerable,
    SilentlyPerformable,
    SilentlyResolvable,
]


@overload
def Silently(duck: Performable) -> Union[Performable, SilentlyPerformable]:
    ...


@overload
def Silently(duck: Answerable) -> Union[Answerable, SilentlyAnswerable]:
    ...


@overload
def Silently(duck: Resolvable) -> Union[Resolvable, SilentlyResolvable]:
    ...


def Silently(duck: T_duck) -> Union[T_duck, T_silent_duck]:
    """
    Does not log the duck's behavior unless something goes wrong.

    Args:
        duck: Performable, Answerable, or Resolvable

    Returns:
        SilentlyPerformable, SilentlyAnswerable, or SilentlyResolvable
        unless settings.UNABRIDGED_NARRATION is enabled.


    Examples::

        actor.will(Silently(Click(BUTTON)))

        actor.shall(
            See(
                Silently(Text.of_the(WELCOME_BANNER)), ContainsTheText("Welcome!")
            )
        )

        actor.shall(
            See(
                Text.of_the(WELCOME_BANNER), Silently(ContainsTheText("Welcome!"))
            )
        )
    """
    if settings.UNABRIDGED_NARRATION:
        return duck

    if isinstance(duck, Performable):
        return SilentlyPerformable(duck)
    if isinstance(duck, Answerable):
        return SilentlyAnswerable(duck)
    if isinstance(duck, Resolvable):
        return SilentlyResolvable(duck)

    return duck
