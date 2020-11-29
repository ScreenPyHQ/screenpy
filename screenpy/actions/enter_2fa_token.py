"""
An action to enter a 2-factor authentication code into a text field.
"""

from selenium.webdriver.common.action_chains import ActionChains

from screenpy.abilities.authenticate_with_2fa import AuthenticateWith2FA
from screenpy.actor import Actor
from screenpy.pacing import beat
from screenpy.target import Target

from .enter import Enter


class Enter2FAToken:
    """Enter the current two-factor authentication token into an input field.

    Abilities Required:
        |BrowseTheWeb|
        |AuthenticateWith2FA|

    Examples::

        the_actor.attempts_to(Enter2FAToken.into_the(2FA_INPUT_FIELD))
    """

    @staticmethod
    def into_the(target: Target) -> "Enter2FAToken":
        """Target the element into which to enter the 2FA token."""
        return Enter2FAToken(target)

    into = into_the

    @beat("{} enters their 2FA token into the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to enter their 2FA token into the targeted element."""
        token = the_actor.uses_ability_to(AuthenticateWith2FA).to_get_token()
        the_actor.attempts_to(Enter.the_text(token).into_the(self.target))

    @beat("  Enter their 2FA token into the {target}!")
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Add the Enter2FAToken action to an in-progress |Chain| of actions."""
        token = the_actor.uses_ability_to(AuthenticateWith2FA).to_get_token()
        the_chain.send_keys_to_element(self.target.found_by(the_actor), token)

    def __init__(self, target: Target) -> None:
        self.target = target
