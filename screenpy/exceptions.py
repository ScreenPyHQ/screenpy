"""
Common exceptions for ScreenPy.
"""


class ScreenPyError(Exception):
    """The base exception for all of ScreenPy."""


class UnableToDirect(ScreenPyError):
    """The Director cannot direct."""


class UnableToNarrate(ScreenPyError):
    """The Narrator cannot narrate."""


class UnableToPerform(ScreenPyError):
    """The Actor lacks the Ability to perform an Action."""


class TargetingError(ScreenPyError):
    """There is an issue preventing Target acquisition."""


class AbilityError(ScreenPyError):
    """These errors are raised when an Ability fails in some way."""


class BrowsingError(AbilityError):
    """BrowseTheWeb encountered an error."""


class RequestError(AbilityError):
    """MakeAPIRequests encountered an error."""


class ActionError(ScreenPyError):
    """These errors are raised when an Action fails."""


class DeliveryError(ActionError):
    """The Action encountered an error while being performed."""


class UnableToAct(ActionError):
    """The Action is missing key information."""


class QuestionError(ScreenPyError):
    """These errors are raised when a Question fails."""


class UnableToAnswer(QuestionError):
    """The Question is not answerable."""
