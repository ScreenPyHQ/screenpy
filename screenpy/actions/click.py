from ..abilities.browse_the_web import BrowseTheWeb
from ..pacing import beat, aside, MINOR


class Click(object):
    """
    Clicks on an element! A Click action is expected to be instantiated
    via its static |Click.on| or |Click.on_the| methods. A typical
    invocation might look like:

        Click.on_the(PROFILE_LINK).then_wait_for(ACCOUNT_WELCOME_MESSAGE)

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def on(target: "Target") -> "Click":
        """
        Creates a new Click action with its crosshairs aimed at the
        provided target.

        Args:
            target (Target): The |Target| describing the element to click.

        Returns:
            |Click|
        """
        return Click(target)

    @staticmethod
    def on_the(target: "Target") -> "Click":
        """Syntactic sugar for |Click.on|."""
        return Click.on(target)

    def then_wait_for(self, target: "Target") -> "Click":
        """
        Supplies a |Target| to wait for after performing the click.

        Args:
            target (Target): The |Target| describing the element to wait
                for after performing the click.

        Returns:
            |Click|
        """
        self.action_complete_target = target
        return self

    @beat("{0} clicks on the {target}.", gravitas=MINOR)
    def perform_as(self, the_actor: "Actor") -> None:
        """
        Asks the actor to find the element described by the stored target,
        and then clicks it. May wait for another target to appear, if
        |Click.then_wait_for| had been called.

        Args:
            the_actor (Actor): The |Actor| who will perform the action.

        Raises:
            |UnableToPerformException|: if the actor does not have the
                ability to |BrowseTheWeb|.
        """
        element = self.target.found_by(the_actor)
        element.click()
        if self.action_complete_target is not None:
            aside("then waits to see the {}".format(self.action_complete_target))
            the_actor.uses_ability_to(BrowseTheWeb).to_wait_for(
                self.action_complete_target
            )

    def __init__(self, target: "Target") -> None:
        self.target = target
        self.action_complete_target = None
        self.following_keys = []
