"""
A few questions to ask about the cookies on the actor's session.
"""

from screenpy import Actor
from screenpy.abilities import BrowseTheWeb, MakeAPIRequests
from screenpy.exceptions import UnableToAnswer
from screenpy.pacing import beat


class Cookies:
    """Ask about the cookies on the actor's session.

    This can be either an API session or their browsing session, whichever one
    they have. If they have both, use one of the more specific questions,
    |CookiesOnTheAPISession| or |CookiesOnTheWebSession|, directly.

    Abilities Required:
        |BrowseTheWeb| or |MakeAPIRequests|

    Examples::

        the_actor.should_see_the(
            (Cookies(), ContainTheEntry(type="chocolate chip"))
        )
    """

    def answered_by(self, the_actor: Actor) -> dict:
        """Direct the actor to investigate their cookies."""
        if the_actor.has_ability_to(BrowseTheWeb):
            return CookiesOnTheWebSession().answered_by(the_actor)
        if the_actor.has_ability_to(MakeAPIRequests):
            return CookiesOnTheAPISession().answered_by(the_actor)

        raise UnableToAnswer(f"{the_actor} has no cookies!")


class CookiesOnTheWebSession:
    """Ask about the cookies on the actor's web browsing session.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.should_see_the(
            (CookiesOnTheWebSession(), ContainTheEntry(type="oatmeal raisin"))
        )
    """

    @beat("{} inspects their web browser's cookies...")
    def answered_by(self, the_actor: Actor) -> dict:
        """Direct the actor to investigate their web browser's cookies."""
        cookies = the_actor.uses_ability_to(BrowseTheWeb).browser.get_cookies()
        return {c["name"]: c["value"] for c in cookies}


class CookiesOnTheAPISession:
    """Ask about the cookies on the actor's API session.

    Abilities Required:
        |MakeAPIRequests|

    Examples::

        the_actor.should_see_the(
            (CookiesOnTheAPISession(), ContainTheEntry(type="snickerdoodle"))
        )
    """

    @beat("{} inspects their API session's cookies.")
    def answered_by(self, the_actor: Actor) -> dict:
        """Direct the actor to investigate their API session's cookies."""
        cookies = the_actor.uses_ability_to(MakeAPIRequests).session.cookies
        return cookies.get_dict()
