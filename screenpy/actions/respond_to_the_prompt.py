"""
Respond to a prompt.
"""

from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import aside, beat


class RespondToThePrompt:
    """Enter text into and accept a javascript prompt.

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

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f'Respond to the prompt with "{self.text}".'

    @beat('{} responds to the prompt with "{text}".')
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to respond to the prompt using the given text."""
        browser = the_actor.uses_ability_to(BrowseTheWeb).browser
        alert = browser.switch_to.alert
        aside(f"... the alert says {alert.text}")
        alert.send_keys(self.text)
        alert.accept()

    def __init__(self, text: str) -> None:
        self.text = text
