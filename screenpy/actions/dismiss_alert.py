"""
An action to dismiss an alert. An actor must possess the ability to
BrowseTheWeb to perform this action. An actor performs this action like
so:

    the_actor.attempts_to(DismissAlert())
"""


from ..abilities import BrowseTheWeb
from ..actor import Actor
from ..pacing import aside, beat
from .base_action import BaseAction


class DismissAlert(BaseAction):
    """
    Dismisses an alert. An DismissAlert action is expected to be
    instantiated as it is, no static methods for this one. The only
    invocation looks like:

        DismissAlert()

    It can then be passed along to the |Actor| to perform the action.
    """

    @beat("{0} dismisses the alert.")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Asks the actor to perform the DismissAlert action.

        Args:
            the_actor: The |Actor| who will perform this action.

        Raises:
            |BrowsingError|: no alert was present.
            |UnableToPerform|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        alert = the_actor.uses_ability_to(BrowseTheWeb).to_switch_to_alert()
        aside(f'... the alert says "{alert.text}"')
        alert.dismiss()
