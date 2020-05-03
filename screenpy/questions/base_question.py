"""
The base class for a Question. This class only serves to enforce that the
answered_by method is defined on a Question. If you intend to create a
custom Question, inheriting from this class will ensure you've defined all
the required methods.
"""


from typing import Any

from ..actor import Actor


class BaseQuestion:
    """
    This base class is only used and enforce proper Question implementation.
    """

    def answered_by(self, the_actor: Actor) -> Any:
        """
        Direct the actor to answer this question.

        Args:
            the_actor: the actor who will answer this question.

        Returns:
            Any: whatever the answer to the question is!
        """
        raise NotImplementedError(
            "Questions must implement answered_by(self, the_actor). Please implement "
            f"this method for the custom '{self.__class__.__name__}' Question."
        )
