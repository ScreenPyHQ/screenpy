"""
Press the browser back button.
"""

from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import beat


class GoBack:
    """Press the browser back button.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(GoBack())
    """

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return "Go back."

    @beat("{} goes back.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to press their browser's back button."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        browser.back()
