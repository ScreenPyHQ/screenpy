"""
Release the left mouse button or a held modifier key.
"""

import platform
from typing import Optional

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from screenpy.actor import Actor
from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat

from .hold_down import KEY_NAMES


class Release:
    """Release the specified key or left mouse button.

    This Action can only be used with the |Chain| meta-Action, and it expects
    that a corresponding |HoldDown| Action was called earlier in the Chain.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(Release.left_mouse_button())

        the_actor.attempts_to(Release(Keys.SHIFT))

        the_actor.attempts_to(Release.command_or_control_key())
    """

    @staticmethod
    def command_or_control_key() -> "Release":
        """
        A convenience method that figures out what operating system the Actor
        is using and tells the Actor which execution key to release.
        """
        if platform.system() == "Darwin":
            return Release(Keys.COMMAND)
        return Release(Keys.CONTROL)

    @staticmethod
    def left_mouse_button() -> "Release":
        """Release the left mouse button."""
        return Release(lmb=True)

    def describe(self) -> str:
        """Describe the Action in present tense."""
        # darn, it doesn't work quite as well here. :P
        return f"Release {self.the_kraken}."

    @beat("  Release {the_kraken}!")
    def add_to_chain(self, _: Actor, the_chain: ActionChains) -> None:
        """Add the Release Action to an in-progress |Chain| of Actions."""
        if self.lmb:
            the_chain.release()
        elif self.key is not None:
            the_chain.key_up(self.key)
        else:
            raise UnableToAct("Release must be told what to release.")

    def __init__(self, key: Optional[str] = None, lmb: bool = False) -> None:
        self.key = key
        self.lmb = lmb
        self.description = "LEFT MOUSE BUTTON" if lmb else KEY_NAMES[key]
        self.the_kraken = self.description  # i can't help myself
