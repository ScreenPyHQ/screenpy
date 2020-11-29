"""
An action to move the mouse to a specific element, or by an offset.
"""

from typing import Optional, Tuple

from selenium.webdriver.common.action_chains import ActionChains

from screenpy.abilities.browse_the_web import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat
from screenpy.target import Target


class MoveMouse:
    """Move the mouse to a specific element or by a pixel offset.

    The x and y offsets are measured in pixels, with the "origin" at the top
    left of the screen.

    * To move left, give a negative x_offset.
    * To move right, give a positive x_offset.
    * To move up, give a negative y_offset.
    * To move down, give a positive y_offset.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(MoveMouse.to_the(HAMBURGER_MENU))

        the_actor.attempts_to(MoveMouse.by_offset(500, -200))

        the_actor.attempts_to(
            Chain(MoveMouse.to_the(HAMBURGER_MENU).with_offset(500, -200))
        )
    """

    offset: Optional[Tuple[int, int]]

    @staticmethod
    def to_the(target: Target) -> "MoveMouse":
        """Target an element to move the mouse to."""
        return MoveMouse(target=target, description=f"to the {target}")

    on_the = over_the = to_the

    @staticmethod
    def by_offset(x_offset: int, y_offset: int) -> "MoveMouse":
        """Specify the offset by which to move the mouse."""
        return MoveMouse(
            offset=(x_offset, y_offset),
            description=f"by an offset of ({x_offset}, {y_offset})",
        )

    def with_offset(self, x_offset: int, y_offset: int) -> "MoveMouse":
        """Specify the mouse should be moved to the element with an offset."""
        self.offset = (x_offset, y_offset)
        self.description += f" offset by ({x_offset}, {y_offset})"
        return self

    def _add_action_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Private method to add the action to the chain."""
        if self.target is not None and self.offset is not None:
            the_chain.move_to_element_with_offset(
                self.target.found_by(the_actor), *self.offset
            )
        elif self.target is not None:
            the_chain.move_to_element(self.target.found_by(the_actor))
        elif self.offset is not None:
            the_chain.move_by_offset(*self.offset)
        else:
            raise UnableToAct(
                "MoveMouse was given neither coordinates nor a target. Supply "
                "one of these using MoveMouse.by_offset or MoveMouse.to_the."
            )

    @beat("{} moves the mouse {description}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to move the mouse."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        the_chain = ActionChains(browser)
        self._add_action_to_chain(the_actor, the_chain)
        the_chain.perform()

    @beat("  Move the mouse {description}!")
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Add the MoveMouse action to an in-progress |Chain| of actions."""
        self._add_action_to_chain(the_actor, the_chain)

    def __init__(
        self,
        offset: Optional[Tuple[int, int]] = None,
        target: Optional[Target] = None,
        description: str = "",
    ) -> None:
        self.offset = offset
        self.target = target
        self.description = description
