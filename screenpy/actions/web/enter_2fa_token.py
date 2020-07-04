"""
An action to enter a 2-factor authentication code into a text field. An actor
must possess the abilities to BrowseTheWeb and AuthenticateWith2FA. An actor
can perform this action like so:

    the_actor.attempts_to(Enter2FAToken.into_the(2FA_INPUT_FIELD))
"""

from screenpy.abilities.authenticate_with_2fa import AuthenticateWith2FA
from screenpy.actor import Actor
from screenpy.pacing import beat
from screenpy.target import Target
from selenium.webdriver.common.action_chains import ActionChains

from .enter import Enter


class Enter2FAToken:
    """
    Enter the current two-factor authentication token into an input field. An
    Enter2FAToken action is expected to be instantiated by its static
    |Enter2FAToken.into_the| method. A typical invocation might look like:

        Enter2FAToken.into_the(2FA_INPUT_FIELD)

    It can then be passed along to the |Actor| or added to a |Chain| to
    perform the action.
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

    into = into_the

    @beat("{0} enters their 2FA token into the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to get the two-factor authentication instrument's
        current token and enter it into the targeted input field.

        Args:
            the_actor: the |Actor| who will perform this action.

        Raises:
            |UnableToPerform|: the actor does not have the
                abilities to |AuthenticateWith2FA| and |BrowseTheWeb|.
        """
        token = the_actor.uses_ability_to(AuthenticateWith2FA).to_get_token()
        the_actor.attempts_to(Enter.the_text(token).into_the(self.target))

    @beat("  Enter their 2FA token into the {target}!")
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """
        Add the Enter2FAToken action to an in-progress |Chain| of actions.

        Args:
            the_actor: the |Actor| who will be performing the action chain.
            the_chain: the |ActionChains| instance that is being built.
        """
        token = the_actor.uses_ability_to(AuthenticateWith2FA).to_get_token()
        the_chain.send_keys_to_element(self.target.found_by(the_actor), token)

    def __init__(self, target: Target) -> None:
        self.target = target
