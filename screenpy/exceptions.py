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


class AbilityError(ScreenPyError):
    """These errors are raised when an Ability fails in some way."""


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


class ResolutionError(ScreenPyError):
    """These errors are raised when a Resolution fails."""


class UnableToFormResolution(ResolutionError):
    """The Resolution is unable to be formed."""


class NotPerformable(ScreenPyError):
    """Does not conform to Performable Protocol"""


class NotAnswerable(ScreenPyError):
    """Does not conform to Answerable Protocol"""


class NotResolvable(ScreenPyError):
    """Does not conform to Resolvable Protocol"""
