"""
Utility functions which should be helpful while writing unit tests for
ScreenPy extensions.
"""

from typing import Any, Callable

from . import settings


def mock_settings(**new_settings: Any) -> Callable:
    """Mock one or more settings for the duration of a test.

    Examples::

        @mock_settings(INDENT_LOGS=False)
        def test_something_about_logging():
            ...
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> None:
            old_settings = {key: getattr(settings, key) for key in new_settings}
            for key, value in new_settings.items():
                setattr(settings, key, value)

            try:
                func(*args, **kwargs)
            finally:
                for key, value in old_settings.items():
                    setattr(settings, key, value)

        return wrapper

    return decorator
