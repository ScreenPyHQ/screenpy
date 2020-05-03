"""
Provides decorators to group your tests into acts (features) and scenes
(cases), and provide the gravitas (severity) of those groupings. This will
both use Allure's marking to group the tests together for those reports
and also set the logging severity for Python's built-in logging library.
"""


import logging
import re
from enum import Enum
from functools import wraps
from typing import Any, Callable

import allure

TRIVIAL = allure.severity_level.TRIVIAL
MINOR = allure.severity_level.MINOR
NORMAL = allure.severity_level.NORMAL
CRITICAL = allure.severity_level.CRITICAL
BLOCKER = allure.severity_level.BLOCKER


Function = Callable[..., Any]
logger = logging.getLogger("screenpy")


def act(title: str, gravitas: Enum = NORMAL) -> Callable[[Function], Function]:
    """
    Decorator to mark an "act". Use the same title to group your tests under
    the same "epic" in Allure's behavior view, and gravitas to group the tests
    by "severity".

    Args:
        title: the title of this "act" (the feature/epic name).
        gravitas: how serious this act is (the severity level).

    Returns:
        Decorated function
    """

    def decorator(func: Function) -> Function:
        @allure.epic(title)
        @allure.severity(gravitas)
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger.info(f"ACT {title.upper()}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def scene(title: str, gravitas: Enum = NORMAL) -> Callable[[Function], Function]:
    """
    Decorator to mark a "scene". Use the same title to group your tests under
    the same "feature" in Allure's behavior view, and gravitas to group the
    tests by "severity".

    Args:
        title: the title of this "scene" (the feature).
        gravitas: how serious this scene is (the severity level).

    Returns:
        Decorated function
    """

    def decorator(func: Function) -> Function:
        @allure.feature(title)
        @allure.severity(gravitas)
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger.info(f"Scene: {title.title()}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def beat(line: str) -> Callable[[Function], Function]:
    """
    Decorator to describe a "beat" (a step in a test). A beat's line can
    contain markers for replacement via str.format(), which will be
    figured out from the properties of a decorated method's class.

    Args:
        line: the line spoken during this "beat" (the step description).

    Returns:
        Decorated function
    """

    def decorator(func: Function) -> Function:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            actor = args[1] if len(args) > 1 else ""

            markers = re.findall(r"\{([^0-9\}]+)}", line)
            cues = {mark: getattr(args[0], mark) for mark in markers}
            completed_line = line.format(actor, **cues)

            logger.info(completed_line)
            with allure.step(completed_line):
                retval = func(*args, **kwargs)
                if retval is not None:
                    aside(str(retval))
            return retval

        return wrapper

    return decorator


def aside(line: str) -> None:
    """
    A line spoken in a stage whisper to the audience. Or, a message to log.

    Args:
        line: the line spoken in this aside (the log text).
        gravitas: how serious this aside is (the severity level).
    """
    logger.info(line)
    with allure.step(line):
        # Can't call method directly, have to enter or decorate
        pass
