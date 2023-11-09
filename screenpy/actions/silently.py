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


def Silently(duck: T) -> T:
    """Silence the duck.

    Any Performable, Answerable, or Resolvable wrapped in Silently will not be
    narrated by the Narrator, unless an exception is raised.

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

    # mypy really doesn't like monkeypatching
    # See https://github.com/python/mypy/issues/2427

    if isinstance(duck, Performable):
        original_perform_as = duck.perform_as

        def perform_as(self: Performable, actor: Actor) -> None:  # noqa: ARG001
            """Direct the Actor to perform silently."""
            with the_narrator.mic_cable_kinked():
                original_perform_as(actor)
                if not settings.UNABRIDGED_NARRATION:
                    the_narrator.clear_backup()
                return

        duck.perform_as = MethodType(perform_as, duck)  # type: ignore[method-assign]

    if isinstance(duck, Answerable):
        original_answered_by = duck.answered_by

        # ANN401 ignored here to follow the Answerable protocol.
        def answered_by(self: Answerable, actor: Actor) -> Any:  # noqa: ARG001, ANN401
            """Direct the Actor to answer the question silently."""
            with the_narrator.mic_cable_kinked():
                thing = original_answered_by(actor)
                if not settings.UNABRIDGED_NARRATION:
                    the_narrator.clear_backup()
                return thing

        duck.answered_by = MethodType(answered_by, duck)  # type: ignore[method-assign]

    if isinstance(duck, Resolvable):
        original_resolve = duck.resolve

        def resolve(self: Resolvable) -> Matcher:  # noqa: ARG001
            """Produce the Matcher to make the assertion, silently."""
            with the_narrator.mic_cable_kinked():
                res = original_resolve()
                if not settings.UNABRIDGED_NARRATION:
                    the_narrator.clear_backup()
                return res

        duck.resolve = MethodType(resolve, duck)  # type: ignore[method-assign]

    return duck
