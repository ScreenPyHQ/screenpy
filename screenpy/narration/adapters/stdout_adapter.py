"""
Logs the Narrator's narration using Python's standard logging library.
"""

import logging
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Generator, List, Optional

from screenpy import settings
from screenpy.narration import narrator

# pylint: disable=unused-argument


class StdOutManager:
    """Handle the indentation, formatting, and log action for CLI logging."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger("screenpy")
        self.depth: List[str] = []
        self.whitespace = settings.INDENT_SIZE * settings.INDENT_CHAR
        self.enabled = settings.INDENT_LOGS

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
        indent = len(self.depth) * self.whitespace if self.enabled else ""
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

    handled_exception: Optional[Exception]

    GRAVITAS = {
        narrator.AIRY: logging.DEBUG,
        narrator.LIGHT: logging.INFO,
        narrator.NORMAL: logging.WARNING,
        narrator.HEAVY: logging.CRITICAL,
        narrator.EXTREME: logging.ERROR,
    }

    def __init__(self, stdout_manager: Optional["StdOutManager"] = None) -> None:
        if stdout_manager is None:
            stdout_manager = StdOutManager()
        self.manager = stdout_manager
        self.handled_exception = None

    def act(
        self, func: Callable, line: str, gravitas: Optional[str] = None
    ) -> Generator:
        """Wrap the act, to log the stylized title."""

        @wraps(func)
        def func_wrapper(*args: Any, **kwargs: Any) -> Callable:
            """Wrap the func, so we log at the correct time."""
            if gravitas is None:
                level = self.GRAVITAS[narrator.LIGHT]
            else:
                level = self.GRAVITAS[gravitas]
            self.manager.log(f"ACT {line.upper()}", level)
            return func(*args, **kwargs)

        yield func_wrapper

    def scene(
        self, func: Callable, line: str, gravitas: Optional[str] = None
    ) -> Generator:
        """Wrap the scene, to log the stylized title."""

        @wraps(func)
        def func_wrapper(*args: Any, **kwargs: Any) -> Callable:
            """Wrap the func, so we log at the correct time."""
            if gravitas is None:
                level = self.GRAVITAS[narrator.LIGHT]
            else:
                level = self.GRAVITAS[gravitas]
            self.manager.log(f"Scene: {line.title()}", level)
            return func(*args, **kwargs)

        yield func_wrapper

    def beat(
        self, func: Callable, line: str, gravitas: Optional[str] = None
    ) -> Generator:
        """Encapsulate the beat within the manager's log context."""
        if not gravitas:
            gravitas = narrator.LIGHT
        with self.manager.log_context(line, self.GRAVITAS[gravitas]):
            yield func

    def aside(
        self, func: Callable, line: str, gravitas: Optional[str] = None
    ) -> Generator:
        """Encapsulate the aside within the manager's log context."""
        if not gravitas:
            gravitas = narrator.LIGHT
        with self.manager.log_context(line, self.GRAVITAS[gravitas]):
            yield func

    def error(self, exc: Exception) -> None:
        """Log information about the error."""
        if exc is not self.handled_exception:
            self.manager.log(
                f"***ERROR***\n\n{exc.__class__.__name__}: {exc}",
                self.GRAVITAS[narrator.EXTREME],
            )
            self.handled_exception = exc

    def attach(self, filepath: str, **kwargs: Any) -> None:
        """Log a mention of an attached file."""
        self.manager.log(f"See reference file: {filepath}")
