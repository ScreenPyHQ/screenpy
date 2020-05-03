"""
The base class for an Action. This class only serves to enforce that the
perform_as method is defined on an Action. If you intend to create a
custom Action, inheriting from this class will ensure you've defined all
the required methods.
"""


from ..actor import Actor


class BaseAction:
    """
    This base class is only used to enforce proper Action implementation.
    """

    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to perform this action.

        Args:
            the_actor: the actor who will perform this action.
        """
        raise NotImplementedError(
            "Actions must implement perform_as(self, the actor). Please implement this "
            f"method for the '{self.__class__.__name__}' Action."
        )
