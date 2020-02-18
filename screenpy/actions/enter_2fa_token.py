"""
An action to enter a 2-factor authentication code into a text field. An actor
must possess the abilities to BrowseTheWeb and AuthenticateWith2FA. An actor
can perform this action like so:

    the_actor.attempts_to(Enter2FAToken.into_the(2FA_INPUT_FIELD))
"""


from screenpy import Actor, Target
from screenpy.actions import Enter
from screenpy.pacing import beat

from ..abilities.authenticate_with_2fa import AuthenticateWith2FA
from .base_action import BaseAction


class Enter2FAToken(BaseAction):
    """
    Enters the current two-factor authentication token into an input field. An
    Enter2FAToken action is expected to be instantiated by its static
    |Enter2FAToken.into_the| method. A typical invocation might look like:

        Enter2FAToken.into_the(2FA_INPUT_FIELD)

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def into_the(target: Target) -> "Enter2FAToken":
        """
        Provide the input field into which to enter the 2FA token.

        Args:
            target: the |Target| describing the input field.

        Returns:
            |Enter2FAToken|
        """
        return Enter2FAToken(target)

    @staticmethod
    def into(target: Target) -> "Enter2FAToken":
        """Syntactic sugar for |Enter2FAToken.into_the|"""
        return Enter2FAToken.into_the(target)

    @beat("{0} enters their 2FA token into the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Asks the actor to perform the Enter2FAToken action, which will get the
        current token using the actor's AuthenticateWith2FA ability.

        Args:
            the_actor: the |Actor| who will perform this action.

        Raises:
            |UnableToPerformError|: if the actor does not have the
                abilities to |AuthenticateWith2FA| and |BrowseTheWeb|.
        """
        token = the_actor.uses_ability_to(AuthenticateWith2FA).to_get_token()
        the_actor.attempts_to(Enter.the_text(token).into_the(self.target))

    def __init__(self, target: Target) -> None:
        self.target = target
