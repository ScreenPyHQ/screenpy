"""
Locators and URL for the Drag and Drop page.
"""

from screenpy import Target

URL = "http://the-internet.herokuapp.com/drag_and_drop"

FIRST_DRAGGABLE_BOX = Target.the("first draggable box").located_by("#column-a")
SECOND_DRAGGABLE_BOX = Target.the("second draggable box").located_by("#column-b")
