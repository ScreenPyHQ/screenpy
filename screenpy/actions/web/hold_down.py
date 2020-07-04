"""
An action to hold down the left mouse button, optionally on an element, or a
specific modifier key. It is expected that a |Release| action will be called
later in the |Chain| to release the button or key. An actor must possess the
ability to BrowseTheWeb to perform this action. An actor performs this action
like so:

    the_actor.attempts_to(Chain(HoldDown(Keys.ALT)))

    the_actor.attempts_to(
        Chain(HoldDown.left_mouse_button().on_the(DRAGGABLE_BOX))
    )
"""


import platform
from typing import Optional

from screenpy.actor import Actor
from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat
from screenpy.target import Target
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

KEY_NAMES = {
    getattr(Keys, key_name): key_name
    for key_name in dir(Keys)
    if key_name.isupper() and not key_name.startswith("LEFT_")
}


class HoldDown:
    """
    Hold down the specified key or left mouse button. This action can only be
    used with the |Chain| meta-action, and it is expected that a corresponding
    |Release| action will be called later to release the held key or button.

    A HoldDown action is expected to be instantiated via one of its static
    methods, or on its own with a specific key. A typical invocation might
    look like:

        HoldDown.left_mouse_button().on_the(DRAGGABLE_BOX)

        HoldDown(Keys.SHIFT)

        HoldDown.command_or_control_key()

    It can then be passed along to the |Actor| in a Chain to perform the
    action.
    """

    target: Optional[Target]

    @staticmethod
    def command_or_control_key() -> "HoldDown":
        """
        A convenience method that figures out what operating system the actor
        is using and directs the actor which execution key to hold down.

        Returns:
            |HoldDown|
        """
        if platform.system() == "Darwin":
            return HoldDown(Keys.COMMAND)
        return HoldDown(Keys.CONTROL)

    @staticmethod
    def left_mouse_button() -> "HoldDown":
        """
        Hold down the left mouse button. To provide a target to hold down the
        mouse button on, follow up this method call with |HoldDown.on_the|.

        Returns:
            |HoldDown|
        """
        return HoldDown(lmb=True)

    def on_the(self, target: Target) -> "HoldDown":
        """
        Supply a target to hold down the left mouse button on. If this is
        not called, the currently focused element will receive the click.

        Args:
            target: The |Target| describing the element to click.

        Returns:
            |HoldDown|
        """
        self.target = target
        return self

    on = on_the

    def perform_as(self, the_actor: Actor) -> None:
        """
        Raise an exception. A HoldDown action cannot be directly performed,
        it must be used with |Chain|. It just doesn't make sense otherwise.

        Raises:
            |UnableToAct|: always.
        """
        raise UnableToAct(
            "The HoldDown action cannot be performed directly, "
            "it can only be used with the Chain action."
        )

    @beat("  Hold down the {description}!")
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """
        Add the configured HoldDown action to an in-progress |Chain| of
        actions.

        Args:
            the_actor: the |Actor| who will be performing the action chain.
            the_chain: the |ActionChains| instance that is being built.

        Raises:
            |UnableToAct|: the action was not told what to hold down.
        """
        if self.lmb:
            element = self.target.found_by(the_actor) if self.target else None
            the_chain.click_and_hold(on_element=element)
        elif self.key is not None:
            the_chain.key_down(self.key)
        else:
            raise UnableToAct("HoldDown must be told what to hold down.")

    def __init__(self, key: Optional[str] = None, lmb: bool = False) -> None:
        self.key = key
        self.lmb = lmb
        self.target = None
        self.description = "LEFT MOUSE BUTTON" if lmb else KEY_NAMES[key]
