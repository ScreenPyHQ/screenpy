"""
Matches against a visible WebElement.
"""

from .base_resolution import BaseResolution
from .custom_matchers import is_visible_element


class IsVisible(BaseResolution):
    """Match on a visible element.

    Examples::

        the_actor.should(See.the(Element(WELCOME_BANNER), IsVisible()))
    """

    line = "visible"
    matcher_function = is_visible_element
