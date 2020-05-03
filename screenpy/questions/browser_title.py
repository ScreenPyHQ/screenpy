"""
A question to discover the title of the current window of an Actor's
browser. Questions must be asked with an expected resolution, like so:
    the_actor.should_see_the(
        (BrowserTitle(), ContainsTheText("ScreenPy's Documentation")),
    )
"""


from ..abilities import BrowseTheWeb
from ..actor import Actor
from ..pacing import beat
from .base_question import BaseQuestion


class BrowserTitle(BaseQuestion):
    """
    Ask what the title of the |Actor|'s browser's current window is. This
    question is meant to be instantiated all on its own:

        BrowserTitle()

    It can then be passed along to the |Actor| to ask the question.
    """

    @beat("{} reads the URL from the browser.")
    def answered_by(self, the_actor: Actor) -> str:
        """
        Direct the actor to investigate the browser's title.

        Args:
            the_actor: the |Actor| who will answer the question.

        Returns:
            str: the title of the browser's current window.
        """
        browser = the_actor.ability_to(BrowseTheWeb).browser
        return browser.title
