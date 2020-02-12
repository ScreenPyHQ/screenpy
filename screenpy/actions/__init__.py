"""
Actions are what the actors do, possibly requiring use of their abilities.
Ask your actors to perform actions by passing the actions into their
|Actor.attempts_to| method.
"""


from .base_action import BaseAction
from .clear import Clear
from .click import Click
from .enter import Enter
from .open import Open
from .pause import Pause
from .select import Select, SelectByIndex, SelectByText, SelectByValue
from .wait import Wait

# Natural-language-enabling syntactic sugar
Clears = Clear
Clicks = Click
Opens = Open
Press = Presses = Enters = Enter
Selects = Select
Waits = Wait
Sleep = Sleeps = Pauses = Pause


__all__ = [
    "BaseAction",
    "Clear",
    "Clears",
    "Click",
    "Clicks",
    "Enter",
    "Enters",
    "Open",
    "Opens",
    "Pause",
    "Pauses",
    "Press",
    "Presses",
    "Select",
    "SelectByIndex",
    "SelectByText",
    "SelectByValue",
    "Selects",
    "Sleep",
    "Sleeps",
    "Wait",
    "Waits",
]
