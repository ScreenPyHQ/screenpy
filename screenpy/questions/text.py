"""
Investigate the text of an element or many elements.
"""

from typing import List, Union

from screenpy.actor import Actor
from screenpy.pacing import beat
from screenpy.target import Target


class Text:
    """Ask what text appears in an element or elements.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.should(
            See.the(Text.of(THE_WELCOME_HEADER), ReadsExactly("Welcome!"))
        )

        the_actor.should(
            See.the(Text.of_all(SEARCH_RESULTS), ContainsTheItem("Rear Window"))
        )
    """

    @staticmethod
    def of_the(target: Target) -> "Text":
        """Target the element to extract the text from."""
        return Text(target=target)

    of = of_the

    @staticmethod
    def of_all(multi_target: Target) -> "Text":
        """Target the elements, plural, to extract the text from."""
        return Text(target=multi_target, multi=True)

    def describe(self) -> str:
        """Describe the Question.."""
        return f"The text from the {self.target}."

    @beat("{} reads the text from the {target}.")
    def answered_by(self, the_actor: Actor) -> Union[str, List[str]]:
        """Direct the Actor to read off the text of the element(s)."""
        if self.multi:
            return [e.text for e in self.target.all_found_by(the_actor)]
        return self.target.found_by(the_actor).text

    def __init__(self, target: Target, multi: bool = False) -> None:
        self.target = target
        self.multi = multi
