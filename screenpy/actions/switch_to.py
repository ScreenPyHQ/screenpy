"""
An action to switch the driver's frame of reference. An actor must possess
the ability to BrowseTheWeb to perform this action. An actor performs this
action like so:

    the_actor.attempts_to(SwitchTo.the(ORDERS_FRAME))

    the_actor.attempts_to(SwitchTo(THE_ORDERS_FRAME))

    the_actor.attempts_to(SwitchTo.default())
"""


from typing import Optional

from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import beat
from screenpy.target import Target


class SwitchTo:
    """
    Switch to an element, most likely an iframe, or back to default. A
    SwitchTo action is expected to be instantiated by its static
    |SwitchTo.the| or |SwitchTo.default| methods, or on its own with a target.
    Typical invocations might look like:

        SwitchTo(THE_ORDERS_FRAME)

        SwitchTo.the(ORDERS_FRAME)

        SwitchTo.default()

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def the(target: Target) -> "SwitchTo":
        """
        Specify the target to switch to.

        Args:
            target: the |Target| describing the element to switch to.

        Returns:
            |SwitchTo|
        """
        return SwitchTo(target)

    @staticmethod
    def default() -> "SwitchTo":
        """
        Switch back to the default frame, the browser window.

        Returns:
            |SwitchTo|
        """
        return SwitchTo(None)

    @beat("{0} switches to the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to switch to the specified element, or back to
        the default.

        Args:
            the_actor: The |Actor| who will perform this action.

        Raises:
            |UnableToPerform|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        browser = the_actor.ability_to(BrowseTheWeb).browser
        if self.target is None:
            browser.switch_to.default_content()
        else:
            browser.switch_to.frame(self.target.found_by(the_actor))

    def __init__(self, target: Optional[Target]) -> None:
        self.target = target
