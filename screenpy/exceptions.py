"""
Common exceptions for ScreenPy.
"""


class ScreenPyError(Exception):
    """The base exception for all of ScreenPy."""


class UnableToPerform(ScreenPyError):
    """Raised when an actor lacks the ability to perform an action."""


class TargetingError(ScreenPyError):
    """Raised when there is an issue preventing target acquisition."""


class AbilityError(ScreenPyError):
    """These errors are raised when an ability fails in some way."""


class BrowsingError(AbilityError):
    """Raised when BrowseTheWeb encounters an error."""


class RequestError(AbilityError):
    """Raised when MakeAPIRequests encounters an error."""


class ActionError(ScreenPyError):
    """These errors are raised when an action fails."""


class DeliveryError(ActionError):
    """Raised when an action encounters an error while being performed."""


class UnableToAct(ActionError):
    """Raised when an action is missing direction."""


class QuestionError(ScreenPyError):
    """These errors are raised when a question fails."""


class UnableToAnswer(QuestionError):
    """The actor cannot answer the question."""
