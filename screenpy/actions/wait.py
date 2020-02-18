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
from ..exceptions import DeliveryError, UnableToActError
from ..pacing import beat
from ..target import Target
from .base_action import BaseAction


class Wait(BaseAction):
    """
    Waits for an element to fulfill a certain condition. A Wait action is
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
    def for_(target: Target) -> "Wait":
        """
        Creates a new Wait action holding the provided target.

        Args:
            target: The |Target| to wait for.

        Returns:
            |Wait|
        """
        return Wait(target=target)

    @staticmethod
    def for_the(target: Target) -> "Wait":
        """Syntactic sugar for |Wait.for_|"""
        return Wait.for_(target)

    def seconds_for(self, target: Target) -> "Wait":
        """
        Sets the target after invoking |Wait| with the number of seconds
        you want wait to allow the target to fulfill the expected
        condition. For example:

            Wait(60).seconds_for(CONFETTI).to_disappear()

        This will ask the actor to wait up to 60 seconds for CONFETTI to
        disappear before throwing an exception.

        Args:
            target: The |Target| to wait for.

        Returns:
            |Wait|
        """
        self.target = target
        return self

    def seconds_for_the(self, target: Target) -> "Wait":
        """Syntactic sugar for |Wait.seconds_for|"""
        return self.seconds_for(target)

    def using(self, strategy: object) -> "Wait":
        """
        Uses the given strategy to wait for the target.

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
        Uses Selenium's "visibility of element located" strategy.
        This is the default strategy, so calling this is not strictly
        necessary.

        Returns:
            |Wait|
        """
        self.log_detail = " to be visible..."
        return self.using(EC.visibility_of_element_located)

    def to_be_clickable(self) -> "Wait":
        """
        Uses Selenium's "to be clickable" strategy.

        Returns:
            |Wait|
        """
        self.log_detail = " to be clickable..."
        return self.using(EC.element_to_be_clickable)

    def to_disappear(self) -> "Wait":
        """
        Uses Selenium's "invisibility of element located" strategy.

        Returns:
            |Wait|
        """
        self.log_detail = " to disappear..."
        return self.using(EC.invisibility_of_element_located)

    def to_contain_text(self, text: str) -> "Wait":
        """
        Uses Selenium's "text to be present in element" strategy.

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
        Asks the actor to perform the Wait action, using the contained
        strategy and any extra arguments provided.

        Args:
            the_actor: The |Actor| who will perform this action.

        Raises:
            |UnableToActError|: no target was supplied.
            |UnableToPerformError|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        if self.target is None:
            raise UnableToActError(
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
