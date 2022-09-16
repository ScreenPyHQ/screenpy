"""
Directors handle the meta information that it takes to run a screenplay. There
is only one of them, so you'll always have access to the same information.
"""
from typing import Type, TypeVar

SelfDirector = TypeVar("SelfDirector", bound="Director")
T = TypeVar("T")


class Director:
    """The single Director of the screenplay.

    The Director keeps track of information for the Actors. This information
    can be retrieved using one of the :ref:`directions`.
    """

    notebook: dict

    _instance = None

    def __new__(cls: Type[SelfDirector]) -> SelfDirector:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.notebook = {}
        return cls._instance

    def notes(self: SelfDirector, key: str, value: T) -> None:
        """Note down a value under the given key."""
        self.notebook[key] = value

    def looks_up(self: SelfDirector, key: str) -> T:
        """Look up a noted value by its key."""
        return self.notebook[key]
