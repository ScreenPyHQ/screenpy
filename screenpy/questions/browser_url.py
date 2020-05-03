"""
A question to discover the current url of an Actor's browser. Questions
must be asked with an expected resolution, like so:
    the_actor.should_see_the(
        (BrowserURL(), ReadsExactly("https://example.com/")),
    )
"""


from ..abilities import BrowseTheWeb
from ..actor import Actor
from ..pacing import beat
from .base_question import BaseQuestion


class BrowserURL(BaseQuestion):
    """
    Ask what the current url of the |Actor|'s browser is. This question
    is meant to be instantiated all on its own:

        BrowserURL()

    It can then be passed along to the |Actor| to ask the question.
    """

    @beat("{} reads the URL from the browser.")
    def answered_by(self, the_actor: Actor) -> str:
        """
        Direct the actor to investigate the browser's current URL.

        Args:
            the_actor: the |Actor| who will answer the question.

        Returns:
            str: the current URL of the browser.
        """
        browser = the_actor.ability_to(BrowseTheWeb).browser
        return browser.current_url
