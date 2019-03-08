from functools import wraps

import allure


TRIVIAL = allure.severity_level.TRIVIAL
MINOR = allure.severity_level.MINOR
NORMAL = allure.severity_level.NORMAL
CRITICAL = allure.severity_level.CRITICAL
BLOCKER = allure.severity_level.BLOCKER


def act(desc, severity=NORMAL):
    """
    Decorator to mark an "act" (a feature).
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            allure.severity(severity)
            with allure.feature(desc):
                return func(*args, **kwargs)

        return wrapper

    return decorator


def scene(desc, severity=NORMAL):
    """
    Decorator to mark a "scene" (a user story).
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            allure.severity(severity)
            with allure.story(desc):
                return func(*args, **kwargs)

        return wrapper

    return decorator


def beat(desc, desc_attrs=[], severity=NORMAL):
    """
    Decorator to describe a "beat" (a step in a test).
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            actor = args[1] if len(args) > 1 else ""
            attrs = {arg: getattr(args[0], arg) for arg in desc_attrs}
            allure.severity(severity)
            with allure.step(desc.format(actor, **attrs)):
                return func(*args, **kwargs)

        return wrapper

    return decorator
