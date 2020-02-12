"""
Locators and URL for the Dropdown page.
"""


from screenpy import Target

URL = "http://the-internet.herokuapp.com/dropdown"

THE_DROPDOWN = Target.the("dropdown menu").located_by("#dropdown")
