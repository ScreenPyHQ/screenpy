"""
Directions are special functions that ask for something from the Director.
"""

from .director import Director


def noted_under(key: str) -> object:
    """Gets a noted value from the director.

    Examples::

        the_actor.should(
            See.the(
                Text.of_the(WELCOME_MESSAGE), ContainsTheText(noted_under("first name"))
            ),
        )
    """
    return Director().looks_up(key)


# Natural-language-enabling syntactic sugar

the_noted = noted = noted_under
