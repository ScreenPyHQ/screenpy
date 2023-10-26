"""Common exceptions for ScreenPy."""


class ScreenPyError(Exception):
    """The base exception for all of ScreenPy."""


class UnableToDirect(ScreenPyError):
    """Raised by the Director."""


class UnableToNarrate(ScreenPyError):
    """Raised by the Narrator."""


class UnableToPerform(ScreenPyError):
    """The Actor lacks the Ability to perform an Action."""


class AbilityError(ScreenPyError):
    """Raised by an Ability."""


class ActionError(ScreenPyError):
    """Raised by an Action."""


class DeliveryError(ActionError):
    """The Action encountered an error while being performed."""


class UnableToAct(ActionError):
    """The Action is missing key information or is misconfigured."""


class QuestionError(ScreenPyError):
    """Raised by a Question."""


class UnableToAnswer(QuestionError):
    """The Question encountered an error while being answered."""


class ResolutionError(ScreenPyError):
    """Raised by a Resolution."""


class UnableToFormResolution(ResolutionError):
    """The Resolution is unable to produce its Matcher."""


class NotPerformable(ScreenPyError):
    """Does not conform to Performable Protocol."""


class NotAnswerable(ScreenPyError):
    """Does not conform to Answerable Protocol."""


class NotResolvable(ScreenPyError):
    """Does not conform to Resolvable Protocol."""
