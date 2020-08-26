"""
An action to press the browser back button.
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

    @beat("{} goes back.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to press their browser's back button."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        browser.back()
