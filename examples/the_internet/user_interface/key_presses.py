"""
Locators and URL for the Key Presses page.
"""

from screenpy import Target

URL = "http://the-internet.herokuapp.com/key_presses"

ENTRY_INPUT = Target.the("entry input field").located_by("#target")
RESULT_TEXT = Target.the("result text").located_by("#result")
