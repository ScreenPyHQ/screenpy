"""
An action to click on an element.
"""

from screenpy.actor import Actor
from screenpy.exceptions import DeliveryError
from screenpy.pacing import beat
from screenpy.target import Target
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains


class Click:
    """Click on an element!

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(Click.on_the(PROFILE_LINK))
    """

    @staticmethod
    def on_the(target: Target) -> "Click":
        """Target the element to click on."""
        return Click(target)

    on = on_the

    @beat("{} clicks on the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to click on the targeted element."""
        element = self.target.found_by(the_actor)

        try:
            element.click()
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to click "
                f"{self.target}: {e.__class__.__name__}"
            )
            raise DeliveryError(msg).with_traceback(e.__traceback__)

    @beat("  Click on the {target}!")
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Add the Click action to an in-progress |Chain| of actions."""
        the_chain.click(self.target.found_by(the_actor))

    def __init__(self, target: Target) -> None:
        self.target = target
