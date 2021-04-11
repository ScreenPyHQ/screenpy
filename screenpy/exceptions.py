"""
Common exceptions for ScreenPy.
"""


class ScreenPyError(Exception):
    """The base exception for all of ScreenPy."""


class UnableToPerform(ScreenPyError):
    """Raised when an Actor lacks the Ability to perform an Action."""


class TargetingError(ScreenPyError):
    """Raised when there is an issue preventing Target acquisition."""


class AbilityError(ScreenPyError):
    """These errors are raised when an Ability fails in some way."""


class BrowsingError(AbilityError):
    """Raised when BrowseTheWeb encounters an error."""


class RequestError(AbilityError):
    """Raised when MakeAPIRequests encounters an error."""


class ActionError(ScreenPyError):
    """These errors are raised when an Action fails."""


class DeliveryError(ActionError):
    """Raised when an Action encounters an error while being performed."""


class UnableToAct(ActionError):
    """Raised when an Action is missing direction."""


class QuestionError(ScreenPyError):
    """These errors are raised when a Question fails."""


class UnableToAnswer(QuestionError):
    """The Actor cannot answer the Question."""
