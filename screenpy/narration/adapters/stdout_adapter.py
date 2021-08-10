"""
Logs the Narrator's narration using Python's standard logging library.
"""

import logging
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Generator, List, Optional

from screenpy import settings

# pylint: disable=unused-argument


class StdOutManager:
    """Handle the indentation for CLI logging."""

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

    @contextmanager
    def log(self, line: str) -> Generator:
        """Log a line, increasing the indent depth for nested logs."""
        self.logger.info(f"{self}{line}")
        try:
            with self._indent():
                yield
        finally:
            self._outdent()

    def __str__(self) -> str:
        """Allow this manager to be used directly for string formatting."""
        if self.enabled:
            return f"{len(self.depth) * self.whitespace}"
        return ""


class StdOutAdapter:
    """Adapt the Narrator's microphone to allow narration to stdout."""

    def __init__(self, stdout_manager: Optional["StdOutManager"] = None) -> None:
        if stdout_manager is None:
            stdout_manager = StdOutManager()
        self.manager = stdout_manager

    def act(
        self, func: Callable, line: str, gravitas: Optional[str] = None
    ) -> Generator:
        """Wrap the act, to log the stylized title."""

        @wraps(func)
        def func_wrapper(*args: Any, **kwargs: Any) -> Callable:
            """Wrap the func, so we log at the correct time."""
            self.manager.logger.info(f"ACT {line.upper()}")
            return func(*args, **kwargs)

        yield func_wrapper

    def scene(
        self, func: Callable, line: str, gravitas: Optional[str] = None
    ) -> Generator:
        """Wrap the scene, to log the stylized title."""

        @wraps(func)
        def func_wrapper(*args: Any, **kwargs: Any) -> Callable:
            """Wrap the func, so we log at the correct time."""
            self.manager.logger.info(f"Scene: {line.title()}")
            return func(*args, **kwargs)

        yield func_wrapper

    def beat(self, func: Callable, line: str) -> Generator:
        """Encapsulate the beat within the manager's log context."""
        with self.manager.log(line):
            yield func

    def aside(self, func: Callable, line: str) -> Generator:
        """Encapsulate the aside within the manager's log context."""
        with self.manager.log(line):
            yield func
