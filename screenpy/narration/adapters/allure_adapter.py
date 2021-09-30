"""
Applies Allure's decorators and contexts to the Narrator's narration.
"""

from typing import Any, Callable, Generator, List, Optional

import allure
from allure_commons._allure import StepContext
from allure_commons._core import plugin_manager
from allure_commons.utils import now
from allure_pytest.listener import AllureListener
from allure_pytest.utils import get_status, get_status_details

from screenpy.exceptions import UnableToNarrate
from screenpy.narration import narrator


class AllureAdapter:
    """Adapt the Narrator's microphone to allow narration to Allure."""

    step_stack: List[StepContext]

    GRAVITAS = {
        narrator.AIRY: allure.severity_level.TRIVIAL,
        narrator.LIGHT: allure.severity_level.MINOR,
        narrator.NORMAL: allure.severity_level.NORMAL,
        narrator.HEAVY: allure.severity_level.CRITICAL,
        narrator.EXTREME: allure.severity_level.BLOCKER,
    }

    def __init__(self) -> None:
        self.step_stack = []

    def act(
        self, func: Callable, line: str, gravitas: Optional[str] = None
    ) -> Generator:
        """Decorate the act with Allure's epic and severity decorators."""
        func = allure.epic(line)(func)
        if gravitas:
            func = allure.severity(self.GRAVITAS[gravitas])(func)
        yield func

    def scene(
        self, func: Callable, line: str, gravitas: Optional[str] = None
    ) -> Generator:
        """Decorate the scene with Allure's feature and severity decorators."""
        func = allure.feature(line)(func)
        if gravitas:
            func = allure.severity(self.GRAVITAS[gravitas])(func)
        yield func

    def beat(self, func: Callable, line: str) -> Generator:
        """Encapsulate the beat within Allure's step context."""
        allure_step = allure.step(line)
        try:
            with allure_step:
                self.step_stack.append(allure_step)
                yield func
                self.step_stack.pop()
        except KeyError as extra_stop_step:
            # We may have already stopped this step, so we expect a KeyError.
            if str(extra_stop_step) != f"'{allure_step.uuid}'":
                # ... but if it's a different KeyError, we want to reraise.
                raise

    def aside(self, func: Callable, line: str) -> Generator:
        """Encapsulate the aside within Allure's step context."""
        with allure.step(line):
            yield func

    def error(self, exc: Exception) -> None:
        """Stop the current step with the exception information.

        To do this, we need to extract Allure's Pytest plugin and stop the
        current step ourselves, attaching the exception information. This will
        cause a KeyError down the line, which we handle in ``beat`` above.
        """
        plugin = next(
            p for p in plugin_manager.get_plugins() if isinstance(p, AllureListener)
        )
        plugin.allure_logger.stop_step(
            self.step_stack[-1].uuid,
            stop=now(),
            status=get_status(exc),
            statusDetails=get_status_details(type(exc), exc, exc.__traceback__),
        )

    def attach(self, filepath: str, **kwargs: Any) -> None:
        """Attach a file to the Allure report."""
        attachment_type = kwargs.get("attachment_type")
        name = kwargs.get("name")
        extension = kwargs.get("extension")
        if attachment_type is None:
            raise UnableToNarrate(
                "AllureAdapter requires an attachment type to attach."
                " See https://docs.qameta.io/allure/#_attachments_5"
            )
        allure.attach.file(filepath, name, attachment_type, extension)
