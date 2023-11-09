"""ScreenPy uses a structural subtyping faciliated by Protocols.

These protocols define the expected methods each of the -ables in ScreenPy
will need to implement to satisfy the protocol.

For example, any class that implements ``perform_as`` is a Performable and
can be an Action, any class that implements ``answered_by`` is an Answerable
and can be a Question, etc. For more information on structural subtyping, see
https://mypy.readthedocs.io/en/stable/protocols.html
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from typing import Any, Callable, Generator

    from hamcrest.core.base_matcher import Matcher

    from .actor import Actor


# pylint: disable=unused-argument


@runtime_checkable
class Answerable(Protocol):
    """Questions are Answerable."""

    # ANN401 ignored here so any Question can fulfill this protocol.
    def answered_by(self, the_actor: Actor) -> Any:  # noqa: ANN401
        """Pose the Question to the Actor, who will attempt to answer.

        Args:
            the_actor: the Actor who will answer this Question.

        Returns:
            The answer, based on the sleuthing the Actor has done.
        """


@runtime_checkable
class Describable(Protocol):
    """Classes that describe themselves are Describable."""

    def describe(self) -> str:
        """Describe the Describable in the present tense."""


@runtime_checkable
class ErrorKeeper(Protocol):
    """Classes that save exceptions for later are ErrorKeeper(s)."""

    caught_exception: Exception | None


@runtime_checkable
class Forgettable(Protocol):
    """Abilities are Forgettable."""

    def forget(self) -> None:
        """Clean up the Ability, assuming it will not be used again.

        This may involve closing database connections, quitting browsers,
        deleting data from an API, etc.
        """


@runtime_checkable
class Performable(Protocol):
    """Actions and Tasks are Performable."""

    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to perform this Action.

        Args:
            the_actor: the Actor who will perform this Action.
        """


@runtime_checkable
class Resolvable(Protocol):
    """Resolutions are Resolvable."""

    def resolve(self) -> Matcher:
        """Form the Matcher for an assertion.

        Returns:
            Matcher: the Matcher this Resolution uses for the expected value.
        """


@runtime_checkable
class Adapter(Protocol):
    """Required functions for an adapter to the Narrator's microphone.

    Adapters allow the :ref:`Narrator <narrator api>`'s microphone to
    broadcast to multiple reporting tools, such as stdout or Allure.

    Each of the methods described below correspond to the ``screenpy.pacing``
    decorators of the same name. The Narrator expects each of these methods to
    yield the function back. This allows each adapter to modify the function
    in whatever ways it needs to while allowing the adapters before and after
    to do the same.

    Adapters must follow the function signatures exactly, even if the adapter
    does not use one or more of the parameters. The Narrator passes these
    arguments in as keyword arguments, so they must not be renamed.
    """

    def act(self, func: Callable, line: str, gravitas: str | None = None) -> Generator:
        """Handle narrating an Act, which designates a group of tests."""

    def scene(
        self, func: Callable, line: str, gravitas: str | None = None
    ) -> Generator:
        """Handle narrating a Scene, which designates a subgroup of tests."""

    def beat(self, func: Callable, line: str, gravitas: str | None = None) -> Generator:
        """Handle narrating a Beat, which is a step in a test."""

    def aside(
        self, func: Callable, line: str, gravitas: str | None = None
    ) -> Generator:
        """Handle narrating an Aside, which can happen any time."""

    def error(self, exc: Exception) -> None:
        """React to an exception being thrown, probably during a beat."""

    # ANN401 ignored here to allow for new adapters to use any kwargs.
    def attach(self, filepath: str, **kwargs: Any) -> None:  # noqa: ANN401
        """Handle attaching a file.

        Pass keyword arguments for specific adapters' needs.
        """
