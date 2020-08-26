"""
Protocols to define the expected functions each of the types of Screenplay
Pattern will need to implement.

ScreenPy uses structural subtyping to define its "subclasses" -- for example,
any class that implements ``perform_as`` can be an Action, any class that
implements ``answered_by`` is a Question, etc. For more information, see
https://mypy.readthedocs.io/en/stable/protocols.html
"""

from typing import TYPE_CHECKING, Any

from selenium.webdriver.common.action_chains import ActionChains
from typing_extensions import Protocol

if TYPE_CHECKING:
    from .actor import Actor


class Answerable(Protocol):
    """Questions are Answerable"""

    def answered_by(self, the_actor: "Actor") -> Any:
        """
        Pose the question to the actor, who will investigate and provide the
        answer to their best knowledge.

        Args:
            the_actor: the |Actor| who will answer the question.

        Returns:
            The answer, based on the sleuthing the actor has done.
        """
        ...


class Chainable(Protocol):
    """Actions that can be added to a chain are Chainable"""

    def add_to_chain(self, the_actor: "Actor", the_chain: ActionChains) -> None:
        """
        Add this chainable action to an in-progress chain.

        Args:
            the_actor: the |Actor| who will be performing the action chain.
            the_chain: the |ActionChains| instance that is being built.
        """
        ...


class Forgettable(Protocol):
    """Abilities are Forgettable"""

    def forget(self) -> None:
        """
        Forget this ability by doing any necessary cleanup (quitting browsers,
        closing connections, etc.)
        """
        ...


class Performable(Protocol):
    """Actions that can be performed are Performable"""

    def perform_as(self, the_actor: "Actor") -> None:
        """
        Direct the actor to perform this action.

        Args:
            the_actor: the |Actor| who will perform this action.
        """
        ...
