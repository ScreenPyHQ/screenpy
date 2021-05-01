"""
Directions are special functions that ask for something from the Director.
"""

from typing import Any

from .director import Director
from .exceptions import UnableToDirect


def noted_under(key: str) -> Any:
    """Gets a noted value from the director.

    Examples::

        the_actor.should(
            See.the(
                Text.of_the(WELCOME_MESSAGE), ContainsTheText(noted_under("first name"))
            ),
        )
    """
    try:
        return Director().looks_up(key)
    except KeyError as e:
        msg = (
            f'The Director has no "{key}" noted.'
            " See https://screenpy-docs.readthedocs.io/"
            "en/latest/cookbook.html#using-makenote"
            " for more information."
        )
        raise UnableToDirect(msg) from e


# Natural-language-enabling syntactic sugar

the_noted = noted = noted_under
