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
    Asks what the current url of the Actor's browser is.
    """

    @beat("{} reads the URL from the browser.")
    def answered_by(self, the_actor: Actor) -> str:
        """
        Asks the supplied actor to investigate the page and give their answer.

        Args:
            the_actor: the Actor who will answer the question.

        Returns:
            str: the current URL of the browser.
        """
        browser = the_actor.ability_to(BrowseTheWeb).browser
        return browser.current_url
