from functools import wraps

import pytest


TRIVIAL = pytest.allure.severity_level.TRIVIAL
MINOR = pytest.allure.severity_level.MINOR
NORMAL = pytest.allure.severity_level.NORMAL
CRITICAL = pytest.allure.severity_level.CRITICAL
BLOCKER = pytest.allure.severity_level.BLOCKER


def step(desc, desc_attrs=[], severity=NORMAL):
    """
    Decorator to describe a step, and log things.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            actor = args[1] if len(args) > 1 else ""
            attrs = {arg: getattr(args[0], arg) for arg in desc_attrs}
            pytest.allure.severity(severity)
            with pytest.allure.step(desc.format(actor, **attrs)):
                func(*args, **kwargs)

        return wrapper

    return decorator
