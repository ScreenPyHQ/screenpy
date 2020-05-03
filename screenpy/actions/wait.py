"""
An action to wait for a specified element to fulfill a given condition.
An actor must have the ability to BrowseTheWeb to perform this action. An
actor can perform this action like so:

    the_actor.attempts_to(Wait.for_the(LOGIN_MODAL))

    the_actor.attempts_to(
        Wait(30).seconds_for_the(WELCOME_BANNER).to_disappear()
    )

    the_actor.attempts_to(
        Wait.for_the(BONUS_ICON).using(EC.presence_of_element_located)
    )
"""


from typing import Optional

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC

from ..abilities.browse_the_web import BrowseTheWeb
from ..actor import Actor
from ..exceptions import DeliveryError, UnableToAct
from ..pacing import beat
from ..target import Target
from .base_action import BaseAction


class Wait(BaseAction):
    """
    Wait for an element to fulfill a certain condition. A Wait action is
    expected to be instantiated by its |Wait.for_| method, followed by one
    of its strategies. By default, the |Wait.to_appear| strategy is used.
    Wait can also be instantiated with an integer, like Wait(30), which
    will set the timeout to be used. Some examples of invocations:

        Wait.for_the(LOGIN_FORM)

        Wait.for_the(WELCOME_BANNER).to_contain_text("Welcome!")

        Wait.for(CONFETTI).to_disappear()

        Wait(10).seconds_for_the(PARADE_FLOATS).to_appear()

    It can then be passed along to the |Actor| to perform the action.
    """

    target: Optional[Target]
    timeout: float
    condition: object
    log_detail: str

    @staticmethod
    def for_the(target: Target) -> "Wait":
        """
        Specify the target to wait for.

        Args:
            target: The |Target| to wait for.

        Returns:
            |Wait|
        """
        return Wait(target=target)

    for_ = for_the

    def seconds_for_the(self, target: Target) -> "Wait":
        """
        Specify the target to wait for. This method is only expected to be
        called if the default wait time of 20 seconds was not sufficient for
        your needs. Supply a different timeout like this:

            Wait(60).seconds_for(CONFETTI).to_disappear()

        This will direct the actor to wait up to 60 seconds for CONFETTI to
        disappear before throwing an exception.

        Args:
            target: The |Target| to wait for.

        Returns:
            |Wait|
        """
        self.target = target
        return self

    seconds_for = seconds_for_the

    def using(self, strategy: object) -> "Wait":
        """
        Use the given strategy to wait for the target.

        Args:
            strategy: the condition to use to wait. This can be one of
                Selenium's Expected Conditions, or it can be a custom
                Callable that accepts a Tuple[|By|, str] locator.

        Returns:
            |Wait|
        """
        self.condition = strategy
        return self

    def to_appear(self) -> "Wait":
        """
        Use Selenium's "visibility of element located" strategy. This is the
        default strategy, so calling this is not strictly necessary.

        Returns:
            |Wait|
        """
        self.log_detail = " to be visible..."
        return self.using(EC.visibility_of_element_located)

    def to_be_clickable(self) -> "Wait":
        """
        Use Selenium's "to be clickable" strategy.

        Returns:
            |Wait|
        """
        self.log_detail = " to be clickable..."
        return self.using(EC.element_to_be_clickable)

    def to_disappear(self) -> "Wait":
        """
        Use Selenium's "invisibility of element located" strategy.

        Returns:
            |Wait|
        """
        self.log_detail = " to disappear..."
        return self.using(EC.invisibility_of_element_located)

    def to_contain_text(self, text: str) -> "Wait":
        """
        Use Selenium's "text to be present in element" strategy.

        Args:
            text: the text to expect to be present.

        Returns:
            |Wait|
        """
        self.log_detail = f' to contain the text "{text}"...'
        return self.using(
            lambda locator: EC.text_to_be_present_in_element(locator, text)
        )

    @beat("{0} waits for the {target}{log_detail}")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to wait for the specified condition to be satisfied.

        Args:
            the_actor: The |Actor| who will perform this action.

        Raises:
            |UnableToAct|: no target was supplied.
            |UnableToPerform|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        if self.target is None:
            raise UnableToAct(
                "Target was not supplied for Wait. Provide a target by using either "
                ".for_(), .for_the(), .seconds_for(), or .seconds_for_the() method."
            )

        try:
            the_actor.uses_ability_to(BrowseTheWeb).to_wait_for(
                self.target, timeout=self.timeout, cond=self.condition
            )
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to wait for the "
                f"{self.target}: {e.__class__.__name__}"
            )
            raise DeliveryError(msg).with_traceback(e.__traceback__)

    def __init__(self, seconds: int = 20, target: Optional[Target] = None) -> None:
        self.target = target
        self.timeout = seconds
        self.condition = EC.visibility_of_element_located
        self.log_detail = " to be visible..."
