"""
An action to open a browser on a URL. An actor must possess the ability to
BrowseTheWeb to perform this action. An actor can perform this action like
so:

    the_actor.attempts_to(
        Open.their_browser_on(
            "https://screenpy-docs.readthedocs.io/en/latest/"
        )
    )
"""


import os
from typing import Union

from screenpy.abilities.browse_the_web import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import beat


class Open:
    """
    Open the browser to a specific URL! An Open action is expected to be
    instantiated via its static |Open.browser_on| method. A typical invocation
    might look like:

        Open.their_browser_on(the_homepage_url)

        Open.browser_on(HomepageObject)

    This action supports using the BASE_URL environment variable to
    set a base URL. If you set BASE_URL, the url passed in to this
    function will be appended to the end of it. For example, if you
    have `BASE_URL=http://localhost`, then to_get("/home") will send
    your browser to "http://localhost/home".

    If you pass in an object, make sure the object has a `url` property
    that can be referenced by this action.

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def their_browser_on(location: Union[str, object]) -> "Open":
        """
        Open the actor's browser on the specified URL.

        Args:
            location: The URL to open when this action is performed, or an
                object containing a `url` property that holds the URL to
                open when this action is performed.

        Returns:
            |Open|
        """
        return Open(location)

    browser_on = their_browser_on

    @beat("{0} opens their browser and visits {url}")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to visit the specified URL.

        Args:
            the_actor: The |Actor| who will perform the action.

        Raises:
            |UnableToPerform|: the actor does not have the ability to
                |BrowseTheWeb|.
        """
        browser = the_actor.ability_to(BrowseTheWeb).browser
        browser.get(self.url)

    def __init__(self, location: Union[str, object]) -> None:
        url = getattr(location, "url", location)
        url = f'{os.getenv("BASE_URL", "")}{url}'
        self.url = url
