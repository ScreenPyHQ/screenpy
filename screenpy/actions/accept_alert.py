"""
An action to accept an alert. An actor must possess the ability to
BrowseTheWeb to perform this action. An actor performs this action like
so:

    the_actor.attempts_to(AcceptAlert())
"""


from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import aside, beat


class AcceptAlert:
    """
    Accept an alert. An AcceptAlert action is expected to be instantiated as
    on its own. Its invocation looks like:

        AcceptAlert()

    It can then be passed along to the |Actor| to perform the action.
    """

    @beat("{0} accepts the alert.")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to accept the alert.

        Args:
            the_actor: The |Actor| who will perform this action.

        Raises:
            |UnableToPerform|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        browser = the_actor.ability_to(BrowseTheWeb).browser
        alert = browser.switch_to.alert
        aside(f'... the alert says "{alert.text}"')
        alert.accept()
