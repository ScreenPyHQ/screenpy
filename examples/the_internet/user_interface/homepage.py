"""
Locators and URL for The Internet app's homepage.
"""


from screenpy import Target

URL = "http://the-internet.herokuapp.com/"

CHECKBOXES_LINK = Target.the("checkboxes link").located_by("a[href*=checkboxes]")
DROPDOWN_LINK = Target.the("dropdown link").located_by("a[href*=dropdown]")
ADD_REMOVE_ELEMENTS_LINK = Target.the("add and remove elements link").located_by(
    "a[href*=add_remove_elements]"
)
