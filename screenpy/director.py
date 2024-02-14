"""Directors handle the meta information that it takes to run a screenplay.

Director is a singleton, just like in real life. The Director can take notes
to be passed between functions
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing_extensions import Self


class Director:
    """The single Director of the screenplay.

    The Director keeps track of information for the Actors. This information
    can be retrieved using one of the :ref:`directions`.
    """

    notebook: dict

    _instance = None

    def __new__(cls) -> Self:
        """Ensure there is only one Director."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.notebook = {}
        return cls._instance

    # ANN401 ignored here because the Director can note anything!
    def notes(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Note down a value under the given key."""
        self.notebook[key] = value

    # ANN401 ignored here because the Director can note anything!
    def looks_up(self, key: str) -> Any:  # noqa: ANN401
        """Look up a noted value by its key."""
        return self.notebook[key]
