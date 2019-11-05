from typing import Callable, Tuple

from selenium.webdriver.support import expected_conditions as EC

from ..abilities.browse_the_web import BrowseTheWeb
from ..actor import Actor
from ..pacing import beat, MINOR
from ..target import Target


class Wait:
    """
    Waits for an element to fulfill a certain condition. A Wait action is
    expected to be instantiated by its |Wait.for| method, followed by one
    of its strategies. By default, the |Wait.to_appear| strategy is used.
    Some examples of invocations:

        Wait.for_the(LOGIN_FORM)
        Wait.for_the(WELCOME_BANNER).to_contain_text("Welcome!")
        Wait.for(CONFETTI).to_disappear()

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def for_(target: Target) -> "Wait":
        """
        Creates a new Wait action holding the provided target. It is
        expected that the next call will be to one of the instantiated
        Wait object's strategy methods, such as

        Args:
            target (Target): The |Target| to enter text into.

        Returns:
            |Wait|
        """
        return Wait(target)

    @staticmethod
    def for_the(target: Target) -> "Wait":
        """Syntactic sugar for |Wait.for_|"""
        return Wait.for_(target)

    def using(self, strategy: Callable[[Tuple], None]) -> "Wait":
        """
        Uses the given strategy to wait for the target.

        Args:
            strategy (ExpectedCondition): the strategy from Selenium's
                expected_conditions module to use.

        Returns:
            |Wait|
        """
        self.condition = strategy
        return self

    def to_appear(self) -> "Wait":
        """
        Uses Selenium's "visibility of element" strategy.
        This is the default strategy, so calling this is not strictly
        necessary.

        Returns:
            |Wait|
        """
        self.log_detail = " to be visible"
        return self.using(EC.visibility_of_element_located)

    def to_disappear(self) -> "Wait":
        """
        Uses Selenium's "invisibility of element" strategy.

        Returns:
            |Wait|
        """
        self.log_detail = " to disappear"
        return self.using(EC.invisibility_of_element_located)

    def to_contain_text(self, text: str) -> "Wait":
        """
        Uses Selenium's "text to be present in element" strategy.

        Args:
            text (str): the text to expect to be present.

        Returns:
            |Wait|
        """
        self.log_detail = f" to contain the text '{text}'"
        return self.using(
            lambda locator: EC.text_to_be_present_in_element(locator, text)
        )

    @beat("{0} waits for the '{target}'{log_detail}.", gravitas=MINOR)
    def perform_as(self, the_actor: Actor) -> None:
        """
        Asks the |Actor| to performs the Wait action, using the contained
        strategy and any extra arguments provided.

        Args:
            the_actor: The |Actor| who will perform this action.

        Raises:
            |UnableToPerformException|: if the actor does not have the
                ability to |BrowseTheWeb|.
        """
        the_actor.uses_ability_to(BrowseTheWeb).to_wait_for(
            self.target.get_locator(), cond=self.condition
        )

    def __init__(self, target: Target) -> None:
        self.target = target
        self.condition = EC.visibility_of_element_located
        self.log_detail = ""
