"""
A meta-Action to group a series of chainable Actions together.
"""

from selenium.webdriver.common.action_chains import ActionChains

from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat
from screenpy.protocols import Chainable


class Chain:
    """A meta-Action to group a series of chainable Actions together

    A Chain Action is expected to be instantiated with a list of Actions to
    perform in a series.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(
            Chain(Hover.on_the(MENU_ICON), Click.on_the(SUBMENU_LINK))
        )

    *Note*: Several Actions cannot be Chained, and will raise an exception.
    """

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return "Perform a thrilling chain of actions."

    @beat("{} performs a thrilling chain of Actions!")
    def perform_as(self, the_actor: Actor) -> None:
        """Choreograph the Actions and direct the Actor to perform the chain."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        the_chain = ActionChains(browser)

        for action in self.actions:
            if "add_to_chain" not in dir(action):
                raise UnableToAct(
                    f"The {action.__class__.__name__} Action cannot be chained."
                )
            action.add_to_chain(the_actor, the_chain)
        the_chain.perform()

    def __init__(self, *actions: Chainable):
        self.actions = actions
