"""
An action to click on an element. An actor must possess the ability to
BrowseTheWeb to perform this action. An actor performs this action like
so:

    the_actor.attempts_to(Click.on_the(LOGIN_LINK))

    the_actor.attempts_to(
        Click.on(THE_MODAL_LAUNCHER).then_wait_for_the(MODAL)
    )
"""


from screenpy.actor import Actor
from screenpy.exceptions import DeliveryError
from screenpy.pacing import beat
from screenpy.target import Target
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains


class Click:
    """
    Click on an element! A Click action is expected to be instantiated via its
    static |Click.on| or |Click.on_the| methods. A typical invocation might
    look like:

        Click.on_the(PROFILE_LINK)

    It can then be passed along to the |Actor| or added to a |Chain| to
    perform the action.
    """

    @staticmethod
    def on_the(target: Target) -> "Click":
        """
        Specify the target to click.

        Args:
            target: The |Target| describing the element to click.

        Returns:
            |Click|
        """
        return Click(target)

    on = on_the

    @beat("{0} clicks on the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to click on the element described by the given target.

        Args:
            the_actor: the |Actor| who will perform the action.

        Raises:
            |DeliveryError|: an exception was raised by Selenium.
            |UnableToPerform|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
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
        """
        Add the Click action to an in-progress |Chain| of actions.

        Args:
            the_actor: the |Actor| who will be performing the action chain.
            the_chain: the |ActionChains| instance that is being built.
        """
        the_chain.click(self.target.found_by(the_actor))

    def __init__(self, target: Target) -> None:
        self.target = target
