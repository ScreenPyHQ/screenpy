"""
An action to move the mouse to a specific element, or by an offset. An actor
must possess the ability to BrowseTheWeb to perform this action. An actor
performs this action like so:

    the_actor.attempts_to(MoveMouse.to_the(HAMBURGER_MENU))

    the_actor.attempts_to(MoveMouse.by_offset(500, -200))

    the_actor.attempts_to(
        MoveMouse.to_the(HAMBURGER_MENU).with_offset(500, -200)
    )

    the_actor.attempts_to(
        Chain(MoveMouse.to_the(HAMBURGER_MENU))
    )
"""


from typing import Optional, Tuple

from screenpy.abilities.browse_the_web import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat
from screenpy.target import Target
from selenium.webdriver.common.action_chains import ActionChains


class MoveMouse:
    """
    Move the mouse to a specific element or by a pixel offset. A MoveMouse
    action is expected to be instantiated by one of its many static methods.
    A typical invocation might look like:

        MoveMouse.to_the(HAMBURGER_MENU)

        MoveMouse.by_offset(500, -200)

        MoveMouse.to_the(HAMBURGER_MENU).with_offset(500, -200)

    It can then be passed along to the |Actor| or added to a |Chain| to
    perform the action.
    """

    offset: Optional[Tuple[int, int]]

    @staticmethod
    def to_the(target: Target) -> "MoveMouse":
        """
        Specify an element to move the mouse to.

        Args:
            target: The |Target| describing the element to move to.

        Returns:
            |MoveMouse|
        """
        return MoveMouse(target=target, description=f"to the {target}")

    on_the = over_the = to_the

    @staticmethod
    def by_offset(x_offset: int, y_offset: int) -> "MoveMouse":
        """
        Specify the offset by which to move the mouse. The x and y offsets are
        measured in pixels, with the "origin" at the top left of the screen.

        * To move left, give a negative x_offset.
        * To move right, give a positive x_offset.
        * To move up, give a negative y_offset.
        * To move down, give a positive y_offset.

        Args:
            x_offset: the number of pixels to move left or right.
            y_offset: the number of pixels to move up or down.

        Returns:
            |MoveMouse|
        """
        return MoveMouse(
            offset=(x_offset, y_offset),
            description=f"by an offset of ({x_offset}, {y_offset})",
        )

    def with_offset(self, x_offset: int, y_offset: int) -> "MoveMouse":
        """
        Specify that the mouse should be moved to a specific position relative
        to the element, with the "origin" at the top left of the element.

        Args:
            x_offset: the number of pixels to move left or right.
            y_offset: the number of pixels to move up or down.

        Returns:
            |MoveMouse|
        """
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
        """
        Direct the actor to move the mouse in the specified way.

        Args:
            the_actor: the |Actor| who will perform this action.

        Raises:
            |UnableToAct|: neither target nor offset were supplied.
            |UnableToPerform|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        browser = the_actor.ability_to(BrowseTheWeb).browser
        the_chain = ActionChains(browser)
        self._add_action_to_chain(the_actor, the_chain)
        the_chain.perform()

    @beat("  Move the mouse {description}!")
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """
        Add the MoveMouse action to an in-progress |Chain| of actions.

        Args:
            the_actor: the |Actor| who will be performing the action chain.
            the_chain: the |ActionChains| instance that is being built.
        """
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
