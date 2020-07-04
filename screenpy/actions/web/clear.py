"""
An action to clear text from an input. An actor must possess the ability
to BrowseTheWeb to perform this action. An actor performs this action like
so:

    the_actor.attempts_to(Clear.the_text_from_the(NAME_INPUT))
"""


from screenpy.actor import Actor
from screenpy.exceptions import DeliveryError
from screenpy.pacing import beat
from screenpy.target import Target
from selenium.common.exceptions import WebDriverException


class Clear:
    """
    Clear the text from an input field. A Clear action is expected to be
    instantiated by its static |Clear.the_text_from| method. A typical
    invocation might look like:

        Clear.the_text_from(COMMENT_FIELD)

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def the_text_from_the(target: Target) -> "Clear":
        """
        Specify which target from which to clear the text.

        Args:
            target: the |Target| from which to clear the text.

        Returns:
            |Clear|
        """
        return Clear(target)

    the_text_from = the_text_from_the

    @beat("{0} clears text from the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to clear the text from the targeted input field.

        Args:
            the_actor: The |Actor| who will perform this action.

        Raises:
            |UnableToPerform|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        element = self.target.found_by(the_actor)

        try:
            element.clear()
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to clear "
                f"{self.target}: {e.__class__.__name__}"
            )
            raise DeliveryError(msg).with_traceback(e.__traceback__)

    def __init__(self, target: Target) -> None:
        self.target = target
