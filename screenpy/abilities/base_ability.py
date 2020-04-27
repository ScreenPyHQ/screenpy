"""
The base class for an Ability. This class only serves to enforce that the
forget method is defined on an Ability. If you intend to create a custom
Ability, inheriting from this class will ensure you've defined all the
required methods.
"""


class BaseAbility:
    """
    This base class is only used to enforce proper Ability implementation.
    """

    def forget(self) -> None:
        """
        Cause the actor to forget this ability -- exit and clean up any
        resources needed.
        """
        raise NotImplementedError(
            "Abilities must implement forget(self). Please implement this method for "
            f"the '{self.__class__.__name__}' Ability."
        )
