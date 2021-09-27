"""
Clear text from an input.
"""

from selenium.common.exceptions import WebDriverException

from screenpy.actor import Actor
from screenpy.exceptions import DeliveryError
from screenpy.pacing import beat
from screenpy.target import Target


class Clear:
    """Clear the text from an input field.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(Clear.the_text_from_the(NAME_INPUT))
    """

    @staticmethod
    def the_text_from_the(target: Target) -> "Clear":
        """Specify the Target from which to clear the text."""
        return Clear(target)

    the_text_from = the_text_from_the

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Clear the text from the {self.target}."

    @beat("{} clears text from the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to clear the text from the input field."""
        element = self.target.found_by(the_actor)

        try:
            element.clear()
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to clear "
                f"{self.target}: {e.__class__.__name__}"
            )
            raise DeliveryError(msg) from e

    def __init__(self, target: Target) -> None:
        self.target = target
