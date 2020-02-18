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


import warnings
from typing import List, Union

from selenium.common.exceptions import WebDriverException

from ..actor import Actor
from ..exceptions import DeliveryError, UnableToActError
from ..pacing import aside, beat
from ..target import Target
from .base_action import BaseAction
from .wait import Wait


class Enter(BaseAction):
    """
    Enters text into an input field. An Enter action is expected to be
    instantiated by its static |Enter.the_text| method. A typical
    invocation might look like:

        Enter.the_text("Hello world!").into(COMMENT_FIELD)

    It can then be passed along to the |Actor| to perform the action.
    """

    text: str
    target: Union[None, Target]
    action_complete_target: Union[None, Target]
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
        Supplies the target to enter the text into. This is most likely
        an input field.

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
        Supplies additional keys to hit after entering the text, for
        example if the keyboard ENTER key should be pressed.

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
        self.following_keys.extend(keys)
        return self

    def then_wait_for(self, target: Target) -> "Enter":
        """
        Supplies the target to wait for after entering text (and hitting
        any additional keys, if this object's |Enter.then_hit| method was
        called).

        This method has been deprecated as of version 1.0.0. Please use
        the included |Wait| action instead. This method will be removed in
        version 2.0.0.

        Args:
            target: the |Target| to wait for after entering text.

        Returns:
            |Enter|
        """
        warnings.warn(
            "Enter.then_wait_for is deprecated. Please use the new Wait action "
            "instead.",
            DeprecationWarning,
        )

        self.action_complete_target = target
        return self

    @beat("{0} enters '{text_to_log}' into the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Asks the actor to perform the Enter action, entering the text into
        the targeted input field using their ability to browse the web.

        If this Enter object's |Enter.then_hit| method was called, it will
        also hit the supplied keys. Finally, if the |Enter.then_wait_for|
        method was called, it will wait for the supplied target to appear.

        Args:
            the_actor: the |Actor| who will perform this action.

        Raises:
            |DeliveryError|: an exception was raised by Selenium.
            |UnableToActError|: no target was supplied.
            |UnableToPerformError|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        if self.target is None:
            raise UnableToActError(
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

        if self.action_complete_target is not None:
            the_actor.attempts_to(Wait.for_the(self.action_complete_target).to_appear())

    def __init__(self, text: str, mask: bool = False) -> None:
        self.text = text
        self.text_to_log = "[CENSORED]" if mask else text
        self.target = None
        self.action_complete_target = None
        self.following_keys = []
