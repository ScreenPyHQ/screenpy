"""
An action to right-click on an element, or wherever the cursor currently is.
An actor must possess the ability to BrowseTheWeb to perform this action. An
actor performs this action like so:

    the_actor.attempts_to(RightClick.on_the(HERO_IMAGE))

    the_actor.attempts_to(RightClick())

    the_actor.attempts_to(Chain(RightClick()))
"""


from typing import Optional

from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import beat
from screenpy.target import Target
from selenium.webdriver.common.action_chains import ActionChains


class RightClick:
    """
    Right-click! A RightClick action is expected to be instantiated via its
    static |RightClick.on| or |RightClick.on_the| methods, or on its own. If
    called without an element, RightClick will click wherever the cursor
    currently is. A typical invocation might look like:

        RightClick.on_the(HERO_IMAGE)

        RightClick()

    It can then be passed along to the |Actor| or added to a |Chain| to
    perform the action.

    *Note*: Most of the time, the context menu that appears after a user
    right-clicks is not interactable through Selenium, because it is an
    application-level menu. A website will need to have implemented a custom
    context menu made of web elements to be able to interact with it.
    """

    target: Optional[Target]

    @staticmethod
    def on_the(target: Target) -> "RightClick":
        """
        Specify which element to right-click on.

        Args:
            target: The |Target| describing the element to right-click.

        Returns:
            |RightClick|
        """
        return RightClick(target=target)

    on = on_the

    def _add_action_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Private method to add the action to the chain."""
        if self.target is not None:
            the_element = self.target.found_by(the_actor)
        else:
            the_element = None

        the_chain.context_click(on_element=the_element)

    @beat("{} right-clicks{description}.")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to right-click on the specified element (or wherever
        the cursor currently is, if no element was specified).

        Args:
            the_actor: the |Actor| who will perform this action.

        Raises:
            |UnableToPerform|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        browser = the_actor.ability_to(BrowseTheWeb).browser
        the_chain = ActionChains(browser)
        self._add_action_to_chain(the_actor, the_chain)
        the_chain.perform()

    @beat("  Right-click{description}!")
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """
        Add the RightClick action to an in-progress |Chain| of actions.

        Args:
            the_actor: the |Actor| who will be performing the action chain.
            the_chain: the |ActionChains| instance that is being built.
        """
        self._add_action_to_chain(the_actor, the_chain)

    def __init__(self, target: Optional[Target] = None) -> None:
        self.target = target
        self.description = f" on the {target}" if target is not None else ""
