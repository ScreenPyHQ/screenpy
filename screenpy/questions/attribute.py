"""
Investigate an attribute of a Target.
"""

from typing import Optional

from screenpy import Actor, Target
from screenpy.exceptions import UnableToAnswer
from screenpy.pacing import beat


class Attribute:
    """Ask about an attribute on an element.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.should(
            See.the(
                Attribute("value").of_the(NAME_INPUT), ReadsExactly("Jessica Walters")),
            ),
            See.the(
                Attribute("aria-label").of_the(BALLOONS), ContainsTheText("balloon")),
            ),
        )
    """

    target: Optional[Target]

    def of(self, target: Target) -> "Attribute":
        """Set the Target to examine."""
        self.target = target
        return self

    of_the = of

    @beat('{} examines the "{attribute}" attribute of the {target}...')
    def answered_by(self, the_actor: Actor) -> None:
        """Direct the actor to investigate the attribute on the element."""
        if self.target is None:
            raise UnableToAnswer(
                "No Target given to Attribute to investigate. Supply a Target"
                " with the `.of()` or `.of_the()` method."
            )

        element = self.target.found_by(the_actor)
        return element.get_attribute(self.attribute)

    def __init__(self, attribute: str) -> None:
        self.attribute = attribute
        self.target = None
