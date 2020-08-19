"""
An action to dismiss an alert. An actor must possess the ability to
BrowseTheWeb to perform this action. An actor performs this action like
so:

    the_actor.attempts_to(DismissAlert())
"""


from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import aside, beat


class DismissAlert:
    """
    Dismiss an alert. A DismissAlert action is expected to be instantiated on
    its own. Its invocation looks like:

        DismissAlert()

    It can then be passed along to the |Actor| to perform the action.
    """

    @beat("{0} dismisses the alert.")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Asks the actor to dismiss the alert.

        Args:
            the_actor: The |Actor| who will perform this action.

        Raises:
            |UnableToPerform|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        browser = the_actor.uses_ability_to(BrowseTheWeb).browser
        alert = browser.switch_to.alert
        aside(f'... the alert says "{alert.text}"')
        alert.dismiss()
