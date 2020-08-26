"""
An action to accept an alert.
"""

from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import aside, beat


class AcceptAlert:
    """Accept an alert!

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(AcceptAlert())
    """

    @beat("{} accepts the alert.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to accept the alert."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        alert = browser.switch_to.alert
        aside(f'... the alert says "{alert.text}"')
        alert.accept()
