"""
Refresh the browser page.
"""

from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import beat


class RefreshPage:
    """Refresh the browser page!

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(RefreshPage())
    """

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return "Refresh the page."

    @beat("{} refreshes the page.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to refresh the page."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        browser.refresh()
