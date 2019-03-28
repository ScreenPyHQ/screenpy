from typing import Callable, Any
from functools import wraps
import re

import allure


TRIVIAL = allure.severity_level.TRIVIAL
MINOR = allure.severity_level.MINOR
NORMAL = allure.severity_level.NORMAL
CRITICAL = allure.severity_level.CRITICAL
BLOCKER = allure.severity_level.BLOCKER


Function = Callable[[Any], Any]


def act(title: str, gravitas=NORMAL) -> Callable[[Function], Function]:
    """
    Decorator to mark an "act" (a feature). Use the same title to group
    your individual "scenes" (test cases) together under the same act in
    the allure report.

    Args:
        title (str): the title of this "act" (the feature name).
        gravitas: how serious this act is (the log level).

    Returns:
        Decorated function
    """

    def decorator(func: Function) -> Function:
        @wraps(func)
        @allure.feature(title)
        def wrapper(*args, **kwargs) -> Any:
            allure.severity(gravitas)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def scene(title: str, gravitas=NORMAL) -> Callable[[Function], Function]:
    """
    Decorator to mark a "scene" (a user story).

    Args:
        title (str): the title of this "scene" (the user story summary).
        gravitas: how serious this scene is (the log level).

    Returns:
        Decorated function
    """

    def decorator(func: Function) -> Function:
        @wraps(func)
        @allure.story(title)
        def wrapper(*args, **kwargs) -> Any:
            allure.severity(gravitas)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def beat(line: str, gravitas=NORMAL) -> Callable[[Function], Function]:
    """
    Decorator to describe a "beat" (a step in a test). A beat's line can
    contain markers for replacement via str.format(), which will be
    figured out from the decorated method's class.

    Args:
        line (str): the line spoken during this "beat" (the test step
            description).
        gravitas: how serious this beat is (the log level).

    Returns:
        Decorated function
    """

    def decorator(func: Function) -> Function:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            actor = args[1] if len(args) > 1 else ""

            markers = re.findall(r"\{([^0-9\}]+)}", line)
            cues = {mark: getattr(args[0], mark) for mark in markers}

            allure.severity(gravitas)
            with allure.step(line.format(actor, **cues)):
                retval = func(*args, **kwargs)
                if retval is not None:
                    aside(retval, gravitas=TRIVIAL)
            return retval

        return wrapper

    return decorator


def aside(line: str, gravitas=NORMAL) -> None:
    """
    A line spoken in a stage whisper to the audience. Or, in this case,
    a quick message to log.

    Args:
        line (str): the line spoken in this aside (the log text).
        gravitas: how serious this aside is (the log level).
    """
    allure.severity(gravitas)
    with allure.step(line):
        # Can't just straight up call, have to enter or decorate
        pass
