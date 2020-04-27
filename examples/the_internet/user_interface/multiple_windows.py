"""
Locators and URLs for the Multiple Windows page.
"""


from screenpy import Target

URL = "http://the-internet.herokuapp.com/windows"

CLICK_HERE_LINK = Target.the("'Click Here' link").located_by("#content a")
HEADER_MESSAGE = Target.the("header message").located_by("h3")
