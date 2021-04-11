"""
Matches a clickable WebElement.
"""

from .base_resolution import BaseResolution
from .custom_matchers import is_clickable_element


class IsClickable(BaseResolution):
    """Match on a clickable element.

    Examples::

        the_actor.should(See.the(Element(LOGIN_BUTTON), IsClickable()))
    """

    line = "clickable"
    matcher_function = is_clickable_element
