"""
A question to discover the text of an alert.
"""

from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import beat


class TextOfTheAlert:
    """Ask what text appears in the alert.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.should_see_the(
            (TextOfTheAlert(), ReadsExactly("Danger, Will Robinson!"))
        )
    """

    @beat("{} reads the text from the alert.")
    def answered_by(self, the_actor: Actor) -> str:
        """Direct the actor to read off the alert's text."""
        browser = the_actor.uses_ability_to(BrowseTheWeb).browser
        return browser.switch_to.alert.text
