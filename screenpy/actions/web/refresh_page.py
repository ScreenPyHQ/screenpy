"""
An action to refresh the browser page. An actor must possess the ability to
BrowseTheWeb to perform this action. An actor performs this action like so:

    the_actor.attempts_to(RefreshPage())
"""


from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import beat


class RefreshPage:
    """
    Refresh the browser page! A RefreshPage action is expected to be
    instantiated on its own. Its invocation looks like:

        RefreshPage()

    It can then be passed along to the |Actor| to perform the action.
    """

    @beat("{} refreshes the page.")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to refresh the page.

        Args:
            the_actor: the |Actor| who will perform this action.

        Raises:
            |UnableToPerform|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        browser = the_actor.ability_to(BrowseTheWeb).browser
        browser.refresh()
