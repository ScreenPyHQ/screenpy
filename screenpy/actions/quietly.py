"""
Quietly allows for "disabling" logging on successful actions & tests
"""
from __future__ import annotations

from typing import Any, TypeVar, overload

from hamcrest.core.base_matcher import Matcher
from typing_extensions import TypeAlias

from screenpy import settings
from screenpy.actor import Actor
from screenpy.pacing import the_narrator
from screenpy.protocols import Answerable, Performable, Resolvable

T = TypeVar("T")


class QuietlyMixin:
    """
    Quietly needs to mimic the ducks (i.e. objects) they are wrapping.
    All of the attributes from the "duck" should be exposed by the Quietly object.
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


class QuietlyPerformable(Performable, QuietlyMixin):
    """Act like the Performable passed in but kink the cable when performing"""

    def perform_as(self, actor: Actor) -> None:
        with the_narrator.mic_cable_kinked():
            self.duck.perform_as(actor)
            if not settings.DEBUG_QUIETLY:
                the_narrator.clear_backup()
            return

    def __init__(self, duck: Performable):
        self.duck = duck


class QuietlyAnswerable(Answerable, QuietlyMixin):
    """Act like the Answerable passed in but kink the cable when answering"""

    def answered_by(self, actor: Actor) -> Any:
        with the_narrator.mic_cable_kinked():
            thing = self.duck.answered_by(actor)
            if not settings.DEBUG_QUIETLY:
                the_narrator.clear_backup()
            return thing

    def __init__(self, duck: Answerable):
        self.duck = duck


class QuietlyResolvable(Resolvable, QuietlyMixin):
    """Act like the Resolvable passed in but kink the cable when resolving"""

    def resolve(self) -> Matcher:
        with the_narrator.mic_cable_kinked():
            res = self.duck.resolve()
            if not settings.DEBUG_QUIETLY:
                the_narrator.clear_backup()
            return res

    def __init__(self, duck: Resolvable):
        self.duck = duck


T_duck: TypeAlias = Performable | Answerable | Resolvable
T_Qu: TypeAlias = QuietlyAnswerable | QuietlyPerformable | QuietlyResolvable


@overload
def Quietly(duck: Performable) -> Performable | QuietlyPerformable:
    ...


@overload
def Quietly(duck: Answerable) -> Answerable | QuietlyAnswerable:
    ...


@overload
def Quietly(duck: Resolvable) -> Resolvable | QuietlyResolvable:
    ...


@overload
def Quietly(duck: T) -> T:
    ...


def Quietly(duck: T | T_duck) -> T | T_duck | T_Qu:
    """
    return one of the appropriate Quietly classes
    Skips creation if debug is enabled.
    """
    if settings.DEBUG_QUIETLY:
        return duck

    if isinstance(duck, Performable):
        return QuietlyPerformable(duck)
    if isinstance(duck, Answerable):
        return QuietlyAnswerable(duck)
    if isinstance(duck, Resolvable):
        return QuietlyResolvable(duck)

    return duck
