"""Logs the Narrator's narration using Python's standard logging library."""

from __future__ import annotations

import logging
from contextlib import contextmanager
from functools import wraps
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Callable, Generator, TypeVar

from ..gravitas import AIRY, EXTREME, HEAVY, LIGHT, NORMAL
from .configuration import settings

# pylint: disable=unused-argument

if TYPE_CHECKING:
    from typing_extensions import ParamSpec

    P = ParamSpec("P")
    T = TypeVar("T")
    Function = Callable[P, T]


class StdOutManager:
    """Handle the indentation, formatting, and log action for CLI logging."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or logging.getLogger("screenpy")
        self.depth: list[str] = []

    @contextmanager
    def _indent(self) -> Generator:
        """Increase the indentation level."""
        # We want this indentation to last until we explicitly call _outdent.
        # Keeping something created in this context alive in our depth gauge
        # will persist the context until we pop it off and discard it later!
        marker = "depth marker"
        self.depth.append(marker)
        yield marker

    def _outdent(self) -> None:
        """Decrease the indentation level."""
        if self.depth:
            self.depth.pop()

    def log(self, line: str, level: int = logging.INFO) -> None:
        """Log a line!"""
        whitespace = settings.INDENT_SIZE * settings.INDENT_CHAR
        indent = len(self.depth) * whitespace if settings.INDENT_LOGS else ""
        self.logger.log(level, f"{indent}{line}")

    @contextmanager
    def log_context(self, line: str, level: int = logging.INFO) -> Generator:
        """Log a line, increasing the indent depth for nested logs."""
        self.log(line, level)
        try:
            with self._indent():
                yield
        finally:
            self._outdent()


class StdOutAdapter:
    """Adapt the Narrator's microphone to allow narration to stdout.

    Examples::

        the_narrator.attach_adapter(StdOutAdapter())
    """

    handled_exception: Exception | None

    GRAVITAS = MappingProxyType(  # makes it immutable
        {
            AIRY: logging.DEBUG,
            LIGHT: logging.INFO,
            NORMAL: logging.WARNING,
            HEAVY: logging.CRITICAL,
            EXTREME: logging.ERROR,
        }
    )

    def __init__(self, stdout_manager: StdOutManager | None = None) -> None:
        if stdout_manager is None:
            stdout_manager = StdOutManager()
        self.manager = stdout_manager
        self.handled_exception = None

    def act(self, func: Callable, line: str, gravitas: str | None = None) -> Generator:
        """Wrap the act, to log the stylized title."""

        @wraps(func)
        def func_wrapper(*args: P.args, **kwargs: P.kwargs) -> Function:
            """Wrap the func, so we log at the correct time."""
            if gravitas is None:
                level = self.GRAVITAS[LIGHT]
            else:
                level = self.GRAVITAS[gravitas]
            self.manager.log(f"ACT {line.upper()}", level)
            return func(*args, **kwargs)

        yield func_wrapper

    def scene(
        self, func: Callable, line: str, gravitas: str | None = None
    ) -> Generator:
        """Wrap the scene, to log the stylized title."""

        @wraps(func)
        def func_wrapper(*args: P.args, **kwargs: P.kwargs) -> Function:
            """Wrap the func, so we log at the correct time."""
            if gravitas is None:
                level = self.GRAVITAS[LIGHT]
            else:
                level = self.GRAVITAS[gravitas]
            self.manager.log(f"Scene: {line.title()}", level)
            return func(*args, **kwargs)

        yield func_wrapper

    def beat(self, func: Callable, line: str, gravitas: str | None = None) -> Generator:
        """Encapsulate the beat within the manager's log context."""
        if not gravitas:
            gravitas = LIGHT
        with self.manager.log_context(line, self.GRAVITAS[gravitas]):
            yield func

    def aside(
        self, func: Callable, line: str, gravitas: str | None = None
    ) -> Generator:
        """Encapsulate the aside within the manager's log context."""
        if not gravitas:
            gravitas = LIGHT
        with self.manager.log_context(line, self.GRAVITAS[gravitas]):
            yield func

    def error(self, exc: Exception) -> None:
        """Log information about the error."""
        if exc is not self.handled_exception:
            self.manager.log(
                f"***ERROR***\n\n{exc.__class__.__name__}: {exc}",
                self.GRAVITAS[EXTREME],
            )
            self.handled_exception = exc

    # ANN401 ignored here to allow for new adapters to use any kwargs.
    def attach(self, filepath: str, **__: Any) -> None:  # noqa: ANN401
        """Log a mention of an attached file."""
        self.manager.log(f"See reference file: {filepath}")
