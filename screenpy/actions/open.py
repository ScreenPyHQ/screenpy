"""
Open a browser on a URL.
"""

import os
from typing import Union

from screenpy.abilities.browse_the_web import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import beat


class Open:
    """Go to a specific URL!

    This Action supports using the BASE_URL environment variable to
    set a base URL. If you set BASE_URL, the url passed in to this
    Action will be appended to the end of it. For example, if you
    have ``BASE_URL=http://localhost``, then ``Open("/home")`` will send
    your browser to "http://localhost/home".

    If you pass in an object, make sure the object has a ``url`` property
    that can be referenced by this Action.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(Open.their_browser_on(HOMEPAGE_URL))

        # using environment variable BASE_URL
        the_actor.attempts_to(Open.their_browser_on("/login"))

        # using a page object with HomepageObject.url
        the_actor.attempts_to(Open.browser_on(HomepageObject))
    """

    @staticmethod
    def their_browser_on(location: Union[str, object]) -> "Open":
        """Provide a URL to visit."""
        return Open(location)

    browser_on = their_browser_on

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Visit {self.url}."

    @beat("{} visits {url}")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to visit the specified URL."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        browser.get(self.url)

    def __init__(self, location: Union[str, object]) -> None:
        url = getattr(location, "url", location)
        url = f'{os.getenv("BASE_URL", "")}{url}'
        self.url = url
