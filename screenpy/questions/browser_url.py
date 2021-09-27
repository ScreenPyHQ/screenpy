"""
Investigate the current url of an Actor's browser.
"""

from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import beat


class BrowserURL:
    """Ask what the url of the browser's active window is.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.should(See.the(BrowserURL(), ContainsTheText("/screenplays")))
    """

    def describe(self) -> str:
        """Describe the Question.."""
        return "The browser URL."

    @beat("{} reads the URL from their browser.")
    def answered_by(self, the_actor: Actor) -> str:
        """Direct the Actor to investigate the browser's current URL."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        return browser.current_url
