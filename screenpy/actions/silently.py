"""Skip logging of successful Actions and tests."""

from __future__ import annotations

from typing import Any, TypeVar, Union, overload

from hamcrest.core.base_matcher import Matcher

from screenpy.actor import Actor
from screenpy.configuration import settings
from screenpy.exceptions import NotAnswerable, NotPerformable, NotResolvable
from screenpy.pacing import the_narrator
from screenpy.protocols import Answerable, Performable, Resolvable

T = TypeVar("T")


class SilentlyMixin:
    """Passthrough to the duck which is being silenced.

    Silently needs to mimic the ducks (i.e. objects) they are wrapping.
    All of the attributes from the "duck" should be exposed by the Silently object.
    """

    def __getattr__(self, key: Any) -> Any:
        """Passthrough to the silenced duck's getattr."""
        try:
            return getattr(self.duck, key)
        except AttributeError as exc:
            msg = (
                f"{self.__class__.__name__}({self.duck.__class__.__name__}) "
                f"has no attribute '{key}'"
            )
            raise AttributeError(msg) from exc


class SilentlyPerformable(Performable, SilentlyMixin):
    """Perform the Performable, but quietly."""

    def perform_as(self, actor: Actor) -> None:
        """Direct the Actor to perform silently."""
        with the_narrator.mic_cable_kinked():
            self.duck.perform_as(actor)
            if not settings.UNABRIDGED_NARRATION:
                the_narrator.clear_backup()
            return

    def __init__(self, duck: Performable):
        if not isinstance(duck, Performable):
            msg = (
                "SilentlyPerformable only works with Performables."
                " Use `Silently` instead."
            )
            raise NotPerformable(msg)
        self.duck = duck


class SilentlyAnswerable(Answerable, SilentlyMixin):
    """Answer the Answerable, but quietly."""

    def answered_by(self, actor: Actor) -> Any:
        """Direct the Actor to answer the question silently."""
        with the_narrator.mic_cable_kinked():
            thing = self.duck.answered_by(actor)
            if not settings.UNABRIDGED_NARRATION:
                the_narrator.clear_backup()
            return thing

    def __init__(self, duck: Answerable):
        if not isinstance(duck, Answerable):
            msg = (
                "SilentlyAnswerable only works with Answerables."
                " Use `Silently` instead."
            )
            raise NotAnswerable(msg)
        self.duck = duck


class SilentlyResolvable(Resolvable, SilentlyMixin):
    """Resolve the Resolvable, but quietly."""

    def resolve(self) -> Matcher:
        """Produce the Matcher to make the assertion, silently."""
        with the_narrator.mic_cable_kinked():
            res = self.duck.resolve()
            if not settings.UNABRIDGED_NARRATION:
                the_narrator.clear_backup()
            return res

    def __init__(self, duck: Resolvable):
        if not isinstance(duck, Resolvable):
            msg = (
                "SilentlyResolvable only works with Resolvables."
                " Use `Silently` instead."
            )
            raise NotResolvable(msg)
        self.duck = duck


T_duck = Union[
    Answerable,
    Performable,
    Resolvable,
]
T_silent_duck = Union[
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
    """Silence the duck.

    Any Performable, Answerable, or Resolvable wrapped in Silently will not be
    narrated by the Narrator, unless an exception is raised.

    Args:
        duck: Performable, Answerable, or Resolvable

    Returns:
        SilentlyPerformable, SilentlyAnswerable, or SilentlyResolvable
        unless settings.UNABRIDGED_NARRATION is enabled.


    Examples::

        the_actor.will(Silently(Click.on(THE_BUTTON)))

        the_actor.shall(
            See(
                Silently(Text.of_the(WELCOME_BANNER)), ContainsTheText("Welcome!")
            )
        )

        the_actor.shall(
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
