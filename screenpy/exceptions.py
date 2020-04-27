"""
Common exceptions for ScreenPy.
"""


class ScreenPyError(Exception):
    """The base exception for all of ScreenPy."""


class UnableToPerform(ScreenPyError):
    """Raised when an actor lacks the ability to perform an action."""


class AbilityError(ScreenPyError):
    """These errors are raised when an ability fails in some way."""


class ActionError(ScreenPyError):
    """These errors are raised when an action fails."""


class DeliveryError(ActionError):
    """Raised when an action encounters an error while being performed."""


class UnableToAct(ActionError):
    """Raised when an action is missing direction."""
