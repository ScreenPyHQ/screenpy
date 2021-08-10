"""
Applies Allure's decorators and contexts to the Narrator's narration.
"""

from typing import Callable, Generator, Optional

import allure

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
