"""
An action to switch to a specific tab or window.
"""

from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import beat


class SwitchToTab:
    """Switch to a specified tab or window.

    Abilities Required:
        |BrowseTheWeb|

    Examples:
        the_actor.attempts_to(SwitchToTab(4))
    """

    @beat("{} switches to {description}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to switch to the specified tab."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        browser.switch_to.window(browser.window_handles[self.index])

    def __init__(self, number: int) -> None:
        self.index = number - 1
        self.description = f"tab #{number}" if number >= 1 else "the newest tab"
