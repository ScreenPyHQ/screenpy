"""
Actions are what the actors do, possibly requiring use of their abilities.
Ask your actors to perform actions by passing the actions into their
|Actor.was_able_to| or |Actor.attempts_to| method.
"""


from .accept_alert import AcceptAlert
from .base_action import BaseAction
from .clear import Clear
from .click import Click
from .debug import Debug
from .dismiss_alert import DismissAlert
from .enter import Enter
from .enter_2fa_token import Enter2FAToken
from .open import Open
from .pause import Pause
from .respond_to_the_prompt import RespondToThePrompt
from .select import Select, SelectByIndex, SelectByText, SelectByValue
from .switch_to import SwitchTo
from .wait import Wait

# Natural-language-enabling syntactic sugar
AcceptsAlert = AcceptAlert
Clears = Clear
Clicks = Click
Debugs = Debug
DismissesAlert = DismissAlert
Enters2FAToken = Enter2FAToken
Opens = Open
Press = Presses = Enters = Enter
RespondsToPrompt = RespondToPrompt = RespondsToThePrompt = RespondToThePrompt
Selects = Select
Sleep = Sleeps = Pauses = Pause
SwitchesTo = SwitchTo
Waits = Wait


__all__ = [
    "AcceptAlert",
    "AcceptsAlert",
    "BaseAction",
    "Clear",
    "Clears",
    "Click",
    "Clicks",
    "Debug",
    "Debugs",
    "DismissAlert",
    "DismissesAlert",
    "Enter",
    "Enter2FAToken",
    "Enters",
    "Enters2FAToken",
    "Open",
    "Opens",
    "Pause",
    "Pauses",
    "Press",
    "Presses",
    "RespondsToPrompt",
    "RespondsToThePrompt",
    "RespondToPrompt",
    "RespondToThePrompt",
    "Select",
    "SelectByIndex",
    "SelectByText",
    "SelectByValue",
    "Selects",
    "Sleep",
    "Sleeps",
    "SwitchesTo",
    "SwitchTo",
    "Wait",
    "Waits",
]
