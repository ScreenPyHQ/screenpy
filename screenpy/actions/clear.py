"""
An action to clear text from an input. An actor must possess the ability
to BrowseTheWeb to perform this action. An actor performs this action like
so:

    the_actor.attempts_to(Clear.the_text_from_the(NAME_INPUT))
"""


from ..actor import Actor
from ..pacing import MINOR, beat
from ..target import Target
from .base_action import BaseAction


class Clear(BaseAction):
    """
    Clears the text from an input field. A Clear action is expected to be
    instantiated by its static |Clear.the_text_from| method. A typical
    invocation might look like:

        Clear.the_text_from(COMMENT_FIELD)

    It can then be passed along to the |Actor| to perform the action.
    """

    target: Target

    @staticmethod
    def the_text_from_the(target: Target) -> "Clear":
        """
        Creates a new Clear action with the provided text.

        Args:
            target: the |Target| from which to clear the text.

        Returns:
            |Clear|
        """
        return Clear(target)

    @staticmethod
    def the_text_from(target: Target) -> "Clear":
        """Syntactic sugar for |Clear.the_text_from_the|."""
        return Clear.the_text_from_the(target)

    @beat("{0} clears text from the {target}.", gravitas=MINOR)
    def perform_as(self, the_actor: Actor) -> None:
        """
        Asks the actor to performs the Clear action, clearing the text
        from the targeted input field using their ability to browse the
        web.

        Args:
            the_actor: The |Actor| who will perform this action.

        Raises:
            |UnableToPerformException|: if the actor does not have the
                ability to |BrowseTheWeb|.
        """
        element = self.target.found_by(the_actor)
        element.clear()

    def __init__(self, target: Target) -> None:
        self.target = target
