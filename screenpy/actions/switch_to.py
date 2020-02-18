"""
An action to switch the driver's frame of reference. An actor must possess
the ability to BrowseTheWeb to perform this action. An actor performs this
action like so:

    the_actor.attempts_to(SwitchTo.the(ORDERS_FRAME))

    the_actor.attempts_to(SwitchTo(THE_ORDERS_FRAME))

    the_actor.attempts_to(SwitchTo.default())
"""


from typing import Optional

from ..abilities import BrowseTheWeb
from ..actor import Actor
from ..pacing import beat
from ..target import Target
from .base_action import BaseAction


class SwitchTo(BaseAction):
    """
    Switches to something, most likely an iframe, or back to default. A
    SwitchTo action is expected to be instantiated by its static
    |SwitchTo.the| or |SwitchTo.default| methods, or on its own. A typical
    invocation might look like:

        SwitchTo.the(ORDERS_FRAME)

        SwitchTo.default()

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def the(target: Target) -> "SwitchTo":
        """
        Provide the element to switch to.

        Args:
            target: the |Target| describing the element to switch to.

        Returns:
            |SwitchTo|
        """
        return SwitchTo(target)

    @staticmethod
    def default() -> "SwitchTo":
        """
        Switches back to the default frame, the browser window.

        Returns:
            |SwitchTo|
        """
        return SwitchTo(None)

    @beat("{0} switches to the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Asks the actor to perform the SwitchTo action.

        Args:
            the_actor: The |Actor| who will perform this action.

        Raises:
            |UnableToPerformError|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        if self.target is None:
            the_actor.uses_ability_to(BrowseTheWeb).to_switch_to_default()
        else:
            the_actor.uses_ability_to(BrowseTheWeb).to_switch_to(self.target)

    def __init__(self, target: Optional[Target]) -> None:
        self.target = target
