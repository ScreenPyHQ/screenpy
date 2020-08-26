"""
An action to switch the driver's frame of reference.
"""

from typing import Optional

from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import beat
from screenpy.target import Target


class SwitchTo:
    """Switch to an element, most likely an iframe, or back to default.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(SwitchTo(THE_ORDERS_FRAME))

        the_actor.attempts_to(SwitchTo.the(ORDERS_FRAME))

        the_actor.attempts_to(SwitchTo.default())
    """

    @staticmethod
    def the(target: Target) -> "SwitchTo":
        """Target an element, probably an iframe, to switch to."""
        return SwitchTo(target, str(target))

    @staticmethod
    def default() -> "SwitchTo":
        """Switch back to the default frame, the browser window."""
        return SwitchTo(None, "default frame")

    @beat("{} switches to the {frame_to_log}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to switch to an element or back to default."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        if self.target is None:
            browser.switch_to.default_content()
        else:
            browser.switch_to.frame(self.target.found_by(the_actor))

    def __init__(self, target: Optional[Target], frame_to_log: str) -> None:
        self.target = target
        self.frame_to_log = frame_to_log
