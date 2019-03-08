from functools import wraps
import re

import allure


TRIVIAL = allure.severity_level.TRIVIAL
MINOR = allure.severity_level.MINOR
NORMAL = allure.severity_level.NORMAL
CRITICAL = allure.severity_level.CRITICAL
BLOCKER = allure.severity_level.BLOCKER


def act(line, severity=NORMAL):
    """
    Decorator to mark an "act" (a feature).
    """

    def decorator(func):
        @wraps(func)
        @allure.feature(line)
        def wrapper(*args, **kwargs):
            allure.severity(severity)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def scene(line, severity=NORMAL):
    """
    Decorator to mark a "scene" (a user story).
    """

    def decorator(func):
        @wraps(func)
        @allure.story(line)
        def wrapper(*args, **kwargs):
            allure.severity(severity)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def beat(line, severity=NORMAL):
    """
    Decorator to describe a "beat" (a step in a test). A beat's line can
    contain markers for replacement via str.format(), which will be.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            actor = args[1] if len(args) > 1 else ""

            markers = re.findall(r"\{([^0-9\}]+)}", line)
            cues = {mark: getattr(args[0], mark) for mark in markers}

            allure.severity(severity)
            with allure.step(line.format(actor, **cues)):
                retval = func(*args, **kwargs)
                if retval is not None:
                    aside(retval, severity=TRIVIAL)
            return retval

        return wrapper

    return decorator


def aside(line, severity=NORMAL):
    """
    A line spoken in a stage whisper to the audience. Or, in this case,
    a quick log for a step.
    """
    allure.severity(severity)
    with allure.step(line):
        # Can't just straight up call, have to enter or decorate
        pass
