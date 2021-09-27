"""
Applies Allure's decorators and contexts to the Narrator's narration.
"""

from typing import Any, Callable, Generator, Optional

import allure

from screenpy.exceptions import UnableToNarrate
from screenpy.narration import narrator


class AllureAdapter:
    """Adapt the Narrator's microphone to allow narration to Allure."""

    GRAVITAS = {
        narrator.AIRY: allure.severity_level.TRIVIAL,
        narrator.LIGHT: allure.severity_level.MINOR,
        narrator.NORMAL: allure.severity_level.NORMAL,
        narrator.HEAVY: allure.severity_level.CRITICAL,
        narrator.EXTREME: allure.severity_level.BLOCKER,
    }

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
        with allure.step(line):
            yield func

    def aside(self, func: Callable, line: str) -> Generator:
        """Encapsulate the aside within Allure's step context."""
        with allure.step(line):
            yield func

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
