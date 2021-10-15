"""
Wait for the application to fulfill a given condition.
"""

from typing import Any, Callable, Iterable, Optional

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from screenpy import settings
from screenpy.abilities.browse_the_web import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.exceptions import DeliveryError
from screenpy.pacing import beat
from screenpy.target import Target


class Wait:
    """Wait for the application to fulfill a given condition.

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

        the_actor.attempts_to(
            Wait().using(
                cookies_to_contain, "for a cookie that has {0}"
            ).with_("delicious=true")
        )
    """

    args: Iterable[Any]

    @staticmethod
    def for_the(target: Target) -> "Wait":
        """Set the Target to wait for."""
        return Wait(settings.TIMEOUT, [target])

    for_ = for_the

    def seconds_for_the(self, target: Target) -> "Wait":
        """Set the Target to wait for, after changing the default timeout."""
        self.args = [target]
        return self

    second_for = second_for_the = seconds_for = seconds_for_the

    def using(
        self, strategy: Callable[..., Any], log_detail: Optional[str] = None
    ) -> "Wait":
        """Use the given strategy to wait for the Target.

        Args:
            strategy: the condition to use to wait. This can be one of
                Selenium's Expected Conditions, or any custom Callable
                that returns a boolean.
            log_detail: a nicer-looking message to log than the default.
                You can use {0}, {1}, etc. to reference specific arguments
                passed into .with_() or .for_the().
        """
        self.condition = strategy
        self.log_detail = log_detail
        return self

    to = seconds_using = using

    def with_(self, *args: Any) -> "Wait":
        """Set the arguments to pass in to the wait condition."""
        self.args = args
        return self

    def to_appear(self) -> "Wait":
        """Use Selenium's "visibility of element located" strategy."""
        return self.using(EC.visibility_of_element_located, "for the {0} to appear...")

    def to_be_clickable(self) -> "Wait":
        """Use Selenium's "to be clickable" strategy."""
        return self.using(EC.element_to_be_clickable, "for the {0} to be clickable...")

    def to_disappear(self) -> "Wait":
        """Use Selenium's "invisibility of element located" strategy."""
        return self.using(
            EC.invisibility_of_element_located, "for the {0} to disappear..."
        )

    def to_contain_text(self, text: str) -> "Wait":
        """Use Selenium's "text to be present in element" strategy."""
        return self.using(
            EC.text_to_be_present_in_element, 'for "{1}" to appear in the {0}...'
        ).with_(*self.args, text)

    @property
    def log_message(self) -> str:
        """Format the nice log message, or give back the default."""
        if self.log_detail is None:
            return f"using {self.condition.__name__} with {self.args}"

        return self.log_detail.format(*self.args)

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Wait {self.timeout} seconds {self.log_message}."

    @beat("{} waits up to {timeout} seconds {log_message}")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to wait for the condition to be satisfied."""
        browser = the_actor.ability_to(BrowseTheWeb).browser

        try:
            WebDriverWait(browser, self.timeout).until(self.condition(*self.args))
        except WebDriverException as e:
            msg = (
                f"Encountered an exception using {self.condition.__name__} with "
                f"[{', '.join(map(str, self.args))}]: {e.__class__.__name__}"
            )
            raise DeliveryError(msg) from e

    def __init__(
        self, seconds: Optional[int] = None, args: Optional[Iterable[Any]] = None
    ) -> None:
        self.args = args if args is not None else []
        self.timeout = seconds if seconds is not None else settings.TIMEOUT
        self.condition = EC.visibility_of_element_located
        self.log_detail = None
