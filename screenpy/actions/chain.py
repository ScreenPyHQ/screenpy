"""
A meta-action to perform lower level actions. An actor will probably need the
ability to BrowseTheWeb to perform this action. An actor performs this action
like so:

    the_actor.attempts_to(
        Chain(Hover.on_the(MENU_ELEMENT), Click.on_the(SUBMENU_ELEMENT))
    )
"""

from selenium.webdriver.common.action_chains import ActionChains

from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat
from screenpy.protocols import Chainable


class Chain:
    """
    A meta-action to group a series of lower-level actions together, like
    hovering and dragging. A Chain action is expected to be instantiated with
    a list of actions to perform in a series.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(
            Chain(Hover.on_the(MENU_ICON), Click.on_the(SUBMENU_LINK))
        )

    *Note*: Several actions cannot be Chained, and will raise an exception.
    """

    @beat("{} performs a thrilling chain of actions!")
    def perform_as(self, the_actor: Actor) -> None:
        """Choreograph the actions and direct the actor to perform the chain."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        the_chain = ActionChains(browser)

        for action in self.actions:
            if "add_to_chain" not in dir(action):
                raise UnableToAct(
                    f"The {action.__class__.__name__} action cannot be chained."
                )
            action.add_to_chain(the_actor, the_chain)
        the_chain.perform()

    def __init__(self, *actions: Chainable):
        self.actions = actions
