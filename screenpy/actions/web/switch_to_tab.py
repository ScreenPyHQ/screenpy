"""
An action to switch to a specific tab or window. An actor must possess the
ability to BrowseTheWeb to perform this action. An actor performs this action
like so:

    the_actor.attempts_to(SwitchToTab.on_top())

    the_actor.attempts_to(SwitchToTab(2))
"""


from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import beat


class SwitchToTab:
    """
    Switch to a specified tab or window. A SwitchToTab action is expected to
    be instantiated either with the number of the tab or window or its static
    |SwitchToTab.on_top| method. A typical invocation might look like this:

        SwitchToTab(4)

        SwitchToTab.on_top()

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def on_top() -> "SwitchToTab":
        """
        Specifies that the actor should switch to the newest tab or window.

        Returns:
            |SwitchToTab|
        """
        return SwitchToTab(0)

    @beat("{} switches to {description}.")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to switch to the specified tab.

        Args:
            the_actor: The |Actor| who will perform the action.

        Raises:
            |UnableToPerform|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        browser = the_actor.ability_to(BrowseTheWeb).browser
        browser.switch_to.window(browser.window_handles[self.index])

    def __init__(self, number: int) -> None:
        self.index = number - 1
        self.description = f"tab #{number}" if number >= 1 else "the newest tab"
