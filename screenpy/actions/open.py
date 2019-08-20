from typing import Union

from ..abilities.browse_the_web import BrowseTheWeb
from ..actor import Actor
from ..pacing import beat, MINOR


class Open:
    """
    A very important action; opens the browser! An Open action is expected
    to be instantiated via its static |Open.browser_on| method. A typical
    invocation might look like:

        Open.browser_on(the_homepage_url)
        Open.browser_on(HomepageObject)

    If you pass in an object, make sure the object has a `url` property
    that can be referenced by this action.

    It can then be passed along to the |Actor| to perform the action.
    """

    @staticmethod
    def browser_on(location: Union[str, object]) -> "Open":
        """
        Creates a new Open action which holds its destined location.

        Args:
            location (str or object): The URL to open when this action is
                performed, or an object containing a `url` property that
                holds the URL to open when this action is performed.

        Returns:
            |Open|
        """
        return Open(location)

    @staticmethod
    def their_browser_on(location: Union[str, object]) -> "Open":
        """Syntactic sugar for |Open.browser_on|."""
        return Open.browser_on(location)

    @beat("{0} opens their browser and loads {url}", gravitas=MINOR)
    def perform_as(self, the_actor: Actor) -> None:
        """
        Asks the supplied actor to perform this Open action, using their
        ability to |BrowseTheWeb|.

        Args:
            the_actor (Actor): The |Actor| who will perform the
                action.

        Raises:
            |UnableToPerformException|: if the actor does
                not have the ability to |BrowseTheWeb|.
        """
        the_actor.uses_ability_to(BrowseTheWeb).to_get(self.url)

    def __init__(self, location: Union[str, object]) -> None:
        self.url = getattr(location, "url", location)
