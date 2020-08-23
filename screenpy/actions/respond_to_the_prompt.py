"""
An action to respond to a prompt. An actor must possess the ability to
BrowseTheWeb to perform this action. An actor performs this action like
so:

    the_actor.attempts_to(
        RespondToThePrompt.with_("Roger, Roger. What's your vector, Victor?")
    )
"""

from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import aside, beat


class RespondToThePrompt:
    """
    Respond to a javascript prompt by entering the specified text and
    accepting the prompt. RespondToThePrompt is expected to be
    instantiated using its |RespondToThePrompt.with_| static method. A
    typical instantiation might look like:

        RespondToThePrompt.with_("Roger, Roger. What's your vector, Victor?")

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def with_(text: str) -> "RespondToThePrompt":
        """
        Provide the text to enter into the prompt.

        Args:
            text: the text to enter.

        Returns:
            |RespondToThePrompt|
        """
        return RespondToThePrompt(text)

    @beat('{0} responds to the prompt with "{text}".')
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to respond to the prompt using the given text.

        Args:
            the_actor: The |Actor| who will perform this action.

        Raises:
            |UnableToPerform|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        browser = the_actor.uses_ability_to(BrowseTheWeb).browser
        alert = browser.switch_to.alert
        aside(f"... the alert says {alert.text}")
        alert.send_keys(self.text)
        alert.accept()

    def __init__(self, text: str) -> None:
        self.text = text
