"""Skip logging of successful Actions and tests."""

from __future__ import annotations

from types import MethodType
from typing import TYPE_CHECKING

from screenpy.configuration import settings
from screenpy.pacing import the_narrator
from screenpy.protocols import Answerable, Performable, Resolvable

if TYPE_CHECKING:
    from typing import Any, TypeVar

    from hamcrest.core.base_matcher import Matcher

    from screenpy.actor import Actor

    T = TypeVar("T")


# mypy really doesn't like monkeypatching
# See https://github.com/python/mypy/issues/2427
# mypy: disable-error-code="method-assign"


def _silence_performable(performing_duck: Performable) -> None:
    """Handle silencing a performable.

    Args:
        performing_duck: the Performable to silence
    """
    original_perform_as = performing_duck.perform_as

    def perform_as(self: Performable, actor: Actor) -> None:  # noqa: ARG001
        """Direct the Actor to perform silently."""
        with the_narrator.mic_cable_kinked():
            original_perform_as(actor)
            if not settings.UNABRIDGED_NARRATION:
                the_narrator.clear_backup()
            return

    performing_duck.perform_as = MethodType(perform_as, performing_duck)
    performing_duck._silenced = True  # type: ignore[attr-defined] # noqa: SLF001


def _silence_answerable(answering_duck: Answerable) -> None:
    """Handle silencing an Answerable.

    Args:
        answering_duck: the Answerable to silence
    """
    original_answered_by = answering_duck.answered_by

    # ANN401 ignored here to follow the Answerable protocol.
    def answered_by(self: Answerable, actor: Actor) -> Any:  # noqa: ARG001, ANN401
        """Direct the Actor to answer the question silently."""
        with the_narrator.mic_cable_kinked():
            thing = original_answered_by(actor)
            if not settings.UNABRIDGED_NARRATION:
                the_narrator.clear_backup()
            return thing

    answering_duck.answered_by = MethodType(answered_by, answering_duck)
    answering_duck._silenced = True  # type: ignore[attr-defined] # noqa: SLF001


def _silence_resolvable(resolving_duck: Resolvable) -> None:
    """Handle silencing a Resolvable.

    Args:
        resolving_duck: the Resolvable to silence
    """
    original_resolve = resolving_duck.resolve

    def resolve(self: Resolvable) -> Matcher:  # noqa: ARG001
        """Produce the Matcher to make the assertion, silently."""
        with the_narrator.mic_cable_kinked():
            res = original_resolve()
            if not settings.UNABRIDGED_NARRATION:
                the_narrator.clear_backup()
            return res

    resolving_duck.resolve = MethodType(resolve, resolving_duck)
    resolving_duck._silenced = True  # type: ignore[attr-defined] # noqa: SLF001


def Silently(duck: T) -> T:  # noqa: N802  # we want Silently to look like an Action.
    """Silence the duck.

    Any Performable, Answerable, or Resolvable wrapped in Silently will not be
    narrated by the Narrator, unless an exception is raised. Technically, this
    is a function, but it is meant to look and be used like an Action.

    Args:
        duck: Performable, Answerable, or Resolvable

    Returns:
        Performable, Answerable, or Resolvable

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
        _silence_performable(duck)

    if isinstance(duck, Answerable):
        _silence_answerable(duck)

    if isinstance(duck, Resolvable):
        _silence_resolvable(duck)

    return duck
