"""
Locators and URL for the Add & Remove Elements page.
"""


from screenpy import Target

URL = "http://the-internet.herokuapp.com/add_remove_elements/"

ADD_BUTTON = Target.the("add element button").located_by("button[onclick^=addElement]")
ADDED_ELEMENTS = Target.the("added elements").located_by("button.added-manually")
