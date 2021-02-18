"""
An action to click on an element.
"""

from typing import Optional

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

from screenpy.actor import Actor
from screenpy.exceptions import DeliveryError, UnableToAct
from screenpy.pacing import beat
from screenpy.target import Target


class Click:
    """Click on an element!

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(Click.on_the(PROFILE_LINK))

        the_actor.attempts_to(Click.on(THE_LOGIN_LINK))

        the_actor.attempts_to(Chain(Click(THE_LOGIN_LINK)))
    """

    @staticmethod
    def on_the(target: Target) -> "Click":
        """Target the element to click on."""
        return Click(target)

    on = on_the

    @beat("{} clicks on the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to click on the targeted element."""
        if self.target is None:
            raise UnableToAct(
                "Target was not supplied for Click. Provide a target by using the "
                ".on() or .on_the() method."
            )

        element = self.target.found_by(the_actor)

        try:
            element.click()
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to click "
                f"{self.target}: {e.__class__.__name__}"
            )
            raise DeliveryError(msg) from e

    @beat("  Click{description}!")
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Add the Click action to an in-progress |Chain| of actions."""
        if self.target is not None:
            the_element = self.target.found_by(the_actor)
        else:
            the_element = None

        the_chain.click(on_element=the_element)

    def __init__(self, target: Optional[Target] = None) -> None:
        self.target = target
        self.description = f" on the {target}" if target is not None else ""
