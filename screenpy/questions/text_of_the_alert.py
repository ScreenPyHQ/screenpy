"""
A question to discover the text of an alert. Questions must be asked with
an expected resolution, like so:

    the_actor.should_see_the(
        (TextOfTheAlert(), ReadsExactly("Look out!!")),
    )
"""


from ..abilities import BrowseTheWeb
from ..actor import Actor
from ..pacing import beat
from .base_question import BaseQuestion


class TextOfTheAlert(BaseQuestion):
    """
    Ask what text appears in the alert, viewed by an |Actor|. This question is
    expected to be instantiated all on its own:

        TextOfTheAlert()

    It can then be passed along to the |Actor| to ask the question.
    """

    @beat("{} reads the text from the alert.")
    def answered_by(self, the_actor: Actor) -> str:
        """
        Direct the actor to read off the alert's text.

        Args:
            the_actor: the |Actor| who will answer the question.

        Returns:
            str: the text of the alert.
        """
        browser = the_actor.uses_ability_to(BrowseTheWeb).browser
        return browser.switch_to.alert.text
