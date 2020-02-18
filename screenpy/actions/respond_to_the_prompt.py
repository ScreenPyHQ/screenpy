"""
An action to respond to a prompt. An actor must possess the ability to
BrowseTheWeb to perform this action. An actor performs this action like
so:

    the_actor.attempts_to(
        RespondToThePrompt.with_(
            "I am big. It’s the pictures that got small."
        )
    )
"""

from ..abilities import BrowseTheWeb
from ..actor import Actor
from ..pacing import aside, beat
from .base_action import BaseAction


class RespondToThePrompt(BaseAction):
    """
    Responds to a javascript prompt by entering the specified text and
    accepting the prompt. RespondToThePrompt is expected to be
    instantiated using its |RespondToThePrompt.with_| static method. A
    typical instantiation might look like:

        RespondToThePrompt.with_("I am big. It’s the pictures that got small.")

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def with_(text: str) -> "RespondToThePrompt":
        """
        Specifies the text to enter into the prompt.

        Args:
            text: the text to enter.

        Returns:
            |RespondToThePrompt|
        """
        return RespondToThePrompt(text)

    @beat('{0} responds to the prompt with "{text}".')
    def perform_as(self, the_actor: Actor) -> None:
        """
        Asks the actor to perform the RespondToPrompt action.

        Args:
            the_actor: The |Actor| who will perform this action.

        Raises:
            |BrowsingError|: no alert was present.
            |UnableToPerformError|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        alert = the_actor.uses_ability_to(BrowseTheWeb).to_switch_to_alert()
        aside(f"... the alert says {alert.text}")
        alert.send_keys(self.text)
        alert.accept()

    def __init__(self, text: str) -> None:
        self.text = text
