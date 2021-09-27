"""
Switch to a specific tab or window.
"""

from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import beat


class SwitchToTab:
    """Switch to a specified tab or window.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(SwitchToTab(4))
    """

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Switch to tab #{self.number}."

    @beat("{} switches to tab #{number}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to switch to the specified tab."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        browser.switch_to.window(browser.window_handles[self.number - 1])

    def __init__(self, number: int) -> None:
        self.number = number
