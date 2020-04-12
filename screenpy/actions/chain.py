"""
A meta-action to perform lower level actions. An actor will probably need the
ability to BrowseTheWeb to perform this action. An actor performs this action
like so:

    the_actor.attempts_to(
        Chain(Hover.on_the(MENU_ELEMENT), Click.on_the(SUBMENU_ELEMENT))
    )
"""


from typing import Any

from selenium.webdriver.common.action_chains import ActionChains

from ..abilities import BrowseTheWeb
from ..actor import Actor
from ..exceptions import UnableToChainError
from ..pacing import beat
from .base_action import BaseAction

# For type-hinting
Action = Any


class Chain(BaseAction):
    """
    A meta-action to group a series of lower-level actions together, like
    hovering and dragging. A Chain action is expected to be instantiated with
    a list of actions to perform in a series. A typical invocation might look
    like:

        Chain(Hover.on_the(MENU_ELEMENT), Click.on_the(SUBMENU_ELEMENT))

    It can then be passed along to the |Actor| to perform the actions.

    *Note*: Several actions cannot be Chained, and will raise an exception if
        you try.
    """

    @beat("{} performs a complicated series of actions!")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Groups the actions together and asks the actor to perform the chain.

        Args:
            the_actor: the |Actor| who will perform the action.

        Raises:
            |UnableToChainError|: an action in the Chain was not chainable.
            |UnableToPerformError|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        browser = the_actor.ability_to(BrowseTheWeb).browser
        the_chain = ActionChains(browser)

        for action in self.actions:
            try:
                action.add_to_chain(the_chain)
            except AttributeError:
                raise UnableToChainError(
                    f"The {action.__class__.__name__} action is not able to "
                    "be chained; it has no add_to_chain(self, the_chain) "
                    "method defined."
                )

        the_chain.perform()

    def __init__(self, *actions: Action):
        self.actions = actions
