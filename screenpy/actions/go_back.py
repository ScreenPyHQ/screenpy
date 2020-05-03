"""
An action to press the browser back button. An actor must possess the ability
to BrowseTheWeb to perform this action. An actor performs this action like so:

    the_actor.attempts_to(GoBack())
"""


from ..abilities import BrowseTheWeb
from ..actor import Actor
from ..pacing import beat
from .base_action import BaseAction


class GoBack(BaseAction):
    """
    Press the browser back button. A GoBack action is expected to be
    instantiated on its own. Its invocation looks like:

        GoBack()

    It can then be passed along to the |Actor| to perform the action.
    """

    @beat("{} goes back.")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to press the browser back button.

        Args:
            the_actor: the |Actor| who will perform this action.

        Raises:
            |UnableToPerform|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        browser = the_actor.ability_to(BrowseTheWeb).browser
        browser.back()
