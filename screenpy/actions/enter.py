"""
Enter text into an input field, or press keys.
"""

from functools import partial
from typing import List, Optional

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

from screenpy.actor import Actor
from screenpy.exceptions import DeliveryError, UnableToAct
from screenpy.pacing import aside, beat
from screenpy.target import Target

from .hold_down import KEY_NAMES


class Enter:
    """Enter text into an input field, or press specific keys.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(
            Enter.the_text("Hello world!").into_the(COMMENT_FIELD)
        )
    """

    target: Optional[Target]
    following_keys: List[str]

    @staticmethod
    def the_text(text: str) -> "Enter":
        """Provide the text to enter in to the field."""
        return Enter(text)

    the_keys = the_text

    @staticmethod
    def the_secret(text: str) -> "Enter":
        """
        Provide the text to enter into the field, but mark that the text
        should be masked in the log. The text will appear as "[CENSORED]".
        """
        return Enter(text, mask=True)

    the_password = the_secret

    def into_the(self, target: Target) -> "Enter":
        """Target the element to enter text into."""
        self.target = target
        return self

    on = into = into_the

    def then_hit(self, *keys: str) -> "Enter":
        """Supply additional keys to hit after entering the text.

        Args:
            keys: the keys to hit afterwards. These are probably the
                constants from Selenium's |Keys|.
        """
        self.following_keys.extend(keys)
        return self

    then_press = then_hit

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f'Enter "{self.text_to_log}" into the {self.target}.'

    @beat('{} enters "{text_to_log}" into the {target}.')
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to enter the text into the element."""
        if self.target is None:
            raise UnableToAct(
                "Target was not supplied for Enter. Provide a Target by using either "
                "the .into(), .into_the(), or .on() method."
            )

        element = self.target.found_by(the_actor)

        try:
            element.send_keys(self.text)
            for key in self.following_keys:
                aside(f"then hits the {KEY_NAMES[key]} key")
                element.send_keys(key)
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to enter text into "
                f"{self.target}: {e.__class__.__name__}"
            )
            raise DeliveryError(msg) from e

    @beat('  Enter "{text_to_log}" into the {target}!')
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Add the Enter Action to an in-progress |Chain| of Actions."""
        if self.target is None:
            send_keys = the_chain.send_keys
        else:
            element = self.target.found_by(the_actor)
            send_keys = partial(the_chain.send_keys_to_element, element)

        send_keys(self.text)
        for key in self.following_keys:
            send_keys(key)

    def __init__(self, text: str, mask: bool = False) -> None:
        self.text = text
        self.target = None
        self.following_keys = []

        if mask:
            self.text_to_log = "[CENSORED]"
        else:
            altered_text = text
            for value, keyname in KEY_NAMES.items():
                altered_text = altered_text.replace(value, keyname)
            self.text_to_log = altered_text
