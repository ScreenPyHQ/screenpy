"""
An action to enter text into an input field. An actor must possess the
ability to BrowseTheWeb to perform this action. An actor performs this
action like so:

    the_actor.attempts_to(
        Enter.the_text("Hello!").into_the(GREETINGS_INPUT)
    )

    the_actor.attempts_to(
        Enter.the_text("Bye!").into_the(CHAT_INPUT).then_hit(Keys.ENTER)
    )
"""


from functools import partial
from typing import List, Union

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

from ..actor import Actor
from ..exceptions import DeliveryError, UnableToAct
from ..pacing import aside, beat
from ..target import Target
from .base_action import BaseAction
from .hold_down import KEY_NAMES


class Enter(BaseAction):
    """
    Enters text into an input field. An Enter action is expected to be
    instantiated by its static |Enter.the_text| method. A typical
    invocation might look like:

        Enter.the_text("Hello world!").into_the(COMMENT_FIELD)

    It can then be passed along to the |Actor| or added to a |Chain| to
    perform the action.
    """

    text: str
    target: Union[None, Target]
    following_keys: List[str]

    @staticmethod
    def the_text(text: str) -> "Enter":
        """
        Creates a new Enter action with the provided text. It is expected
        that the next call will be to the instantiated Enter object's
        |Enter.into| method.

        Args:
            text: the text to enter into the target.

        Returns:
            |Enter|
        """
        return Enter(text)

    @staticmethod
    def the_keys(text: str) -> "Enter":
        """Syntactic sugar for |Enter.the_text|."""
        return Enter.the_text(text)

    @staticmethod
    def the_secret(text: str) -> "Enter":
        """
        Creates a new Enter action with the provided text, but will mask
        the text for logging. The text will appear as "[CENSORED]" in the
        report. It is expected that the next call will be to the
        instantiated Enter object's |Enter.into| method.

        Args:
            text: the text to enter into the target, but it's a secret.

        Returns:
            |Enter|
        """
        return Enter(text, mask=True)

    @staticmethod
    def the_password(text: str) -> "Enter":
        """Syntactic sugar for |Enter.the_secret|."""
        return Enter.the_secret(text)

    def into(self, target: Target) -> "Enter":
        """
        Supplies the target to enter the text into. This is most likely an
        input field.

        Args:
            target: The |Target| describing the input field.

        Returns:
            |Enter|
        """
        self.target = target
        return self

    def into_the(self, target: Target) -> "Enter":
        """Syntactic sugar for |Enter.into|"""
        return self.into(target)

    def on(self, target: Target) -> "Enter":
        """Syntactic sugar for |Enter.into|"""
        return self.into(target)

    def then_hit(self, *keys: str) -> "Enter":
        """
        Supplies additional keys to hit after entering the text, for example
        if the keyboard ENTER key should be pressed.

        Args:
            keys: the keys to hit afterwards. These are probably the
                constants from Selenium's |Keys|, but they can be strings
                if you know the codes.

        Returns:
            |Enter|
        """
        self.following_keys.extend(keys)
        return self

    def then_press(self, *keys: str) -> "Enter":
        """Syntactic sugar for |Enter.then_hit|."""
        return self.then_hit(*keys)

    @beat("{0} enters '{text_to_log}' into the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Asks the actor to enter the text into the targeted input field. If
        this Enter object's |Enter.then_hit| method was called, it will also
        hit the supplied keys.

        Args:
            the_actor: the |Actor| who will perform this action.

        Raises:
            |DeliveryError|: an exception was raised by Selenium.
            |UnableToAct|: no target was supplied.
            |UnableToPerform|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        if self.target is None:
            raise UnableToAct(
                "Target was not supplied for Enter. Provide a target by using either "
                "the .into(), .into_the(), or .on() method."
            )

        element = self.target.found_by(the_actor)

        try:
            element.send_keys(self.text)
            for key in self.following_keys:
                aside(f"then hits the {key} key")
                element.send_keys(key)
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to enter text into "
                f"{self.target}: {e.__class__.__name__}"
            )
            raise DeliveryError(msg).with_traceback(e.__traceback__)

    @beat("  Enters the text {text_to_log} into the {target}!")
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """
        Adds the Enter action to an in-progress |Chain| of actions.

        Args:
            the_actor: the |Actor| who will be performing the action chain.
            the_chain: the |ActionChains| instance that is being built.
        """
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
