"""
An action to respond to a prompt.
"""

from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import aside, beat


class RespondToThePrompt:
    """
    Respond to a javascript prompt by entering the specified text and
    accepting the prompt.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(
            RespondToThePrompt.with_("Roger, Roger. What's your vector, Victor?")
        )
    """

    @staticmethod
    def with_(text: str) -> "RespondToThePrompt":
        """Provide the text to enter into the prompt."""
        return RespondToThePrompt(text)

    @beat('{} responds to the prompt with "{text}".')
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to respond to the prompt using the given text."""
        browser = the_actor.uses_ability_to(BrowseTheWeb).browser
        alert = browser.switch_to.alert
        aside(f"... the alert says {alert.text}")
        alert.send_keys(self.text)
        alert.accept()

    def __init__(self, text: str) -> None:
        self.text = text
