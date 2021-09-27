"""
Hold down a specific key or the left mouse button, optionally on an element.
"""

import platform
from typing import Optional

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from screenpy.actor import Actor
from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat
from screenpy.target import Target

KEY_NAMES = {
    getattr(Keys, key_name): key_name
    for key_name in dir(Keys)
    if key_name.isupper() and not key_name.startswith("LEFT_")
}


class HoldDown:
    """Hold down the specified key or left mouse button.

    This Action can only be used with the |Chain| meta-Action, and it is
    expected that a corresponding |Release| Action will be called later to
    release the held key or button.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(Chain(HoldDown(Keys.SHIFT))

        the_actor.attempts_to(Chain(HoldDown.command_or_control_key()))

        the_actor.attempts_to(
            Chain(HoldDown.left_mouse_button().on_the(DRAGGABLE_BOX))
        )
    """

    target: Optional[Target]

    @staticmethod
    def command_or_control_key() -> "HoldDown":
        """
        A convenience method that figures out what operating system the Actor
        is using and directs the Actor which execution key to hold down.
        """
        if platform.system() == "Darwin":
            return HoldDown(Keys.COMMAND)
        return HoldDown(Keys.CONTROL)

    @staticmethod
    def left_mouse_button() -> "HoldDown":
        """Hold down the left mouse button."""
        return HoldDown(lmb=True)

    def on_the(self, target: Target) -> "HoldDown":
        """Target an element to hold down left click on."""
        self.target = target
        return self

    on = on_the

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Hold down {self.description}."

    @beat("  Hold down {description}!")
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Add the HoldDown Action to an in-progress |Chain| of Actions."""
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
