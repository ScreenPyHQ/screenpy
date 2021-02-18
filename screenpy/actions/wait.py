"""
An action to wait for a specified element to fulfill a given condition.
"""

from typing import Any, Callable, Iterable, Optional

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from screenpy.abilities.browse_the_web import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.exceptions import DeliveryError
from screenpy.pacing import beat
from screenpy.target import Target


class Wait:
    """Wait for the application to fulfill a certain condition.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(Wait.for_the(LOGIN_FORM))

        the_actor.attempts_to(
            Wait.for_the(WELCOME_BANNER).to_contain_text("Welcome!")
        )

        the_actor.attempts_to(Wait.for(CONFETTI).to_disappear())

        the_actor.attempts_to(
            Wait(10).seconds_for_the(PARADE_FLOATS).to(float_on_by)
        )

        the_actor.attempts_to(
            Wait().using(cookies_to_contain).with_("delicious=true")
        )
    """

    args: Iterable[Any]

    @staticmethod
    def for_the(target: Target) -> "Wait":
        """Set the target to wait for."""
        return Wait(20, [target])

    for_ = for_the

    def seconds_for_the(self, target: Target) -> "Wait":
        """Set the target to wait for, after changing the default timeout."""
        self.args = [target]
        return self

    second_for = second_for_the = seconds_for = seconds_for_the

    def using(self, strategy: Callable[..., Any]) -> "Wait":
        """Use the given strategy to wait for the target.

        Args:
            strategy: the condition to use to wait. This can be one of
                Selenium's Expected Conditions, or any custom Callable
                that returns a boolean.
        """
        self.condition = strategy
        self.strategy_name = strategy.__name__
        return self

    to = seconds_using = using

    def to_appear(self) -> "Wait":
        """Use Selenium's "visibility of element located" strategy."""
        return self.using(EC.visibility_of_element_located)

    def to_be_clickable(self) -> "Wait":
        """Use Selenium's "to be clickable" strategy."""
        return self.using(EC.element_to_be_clickable)

    def to_disappear(self) -> "Wait":
        """Use Selenium's "invisibility of element located" strategy."""
        return self.using(EC.invisibility_of_element_located)

    def to_contain_text(self, text: str) -> "Wait":
        """Use Selenium's "text to be present in element" strategy."""
        return self.using(EC.text_to_be_present_in_element).with_(*self.args, text)

    def with_(self, *args: Any) -> "Wait":
        """Set the arguments to pass in to the wait condition."""
        self.args = args
        return self

    @beat("{} waits using {strategy_name} with {args}...")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to wait for the condition to be satisfied."""
        browser = the_actor.ability_to(BrowseTheWeb).browser

        # we need to get the locators for any targets passed in, but also keep
        # them as targets for logging.
        args = map(
            lambda arg: arg.get_locator() if isinstance(arg, Target) else arg, self.args
        )

        try:
            WebDriverWait(browser, self.timeout).until(self.condition(*args))
        except WebDriverException as e:
            msg = (
                f"Encountered an exception using {self.strategy_name} with "
                f"[{', '.join(self.args)}]: {e.__class__.__name__}"
            )
            raise DeliveryError(msg) from e

    def __init__(self, seconds: int = 20, args: Optional[Iterable[Any]] = None) -> None:
        self.args = args if args is not None else []
        self.timeout = seconds
        self.condition = EC.visibility_of_element_located
        self.strategy_name = self.condition.__name__
