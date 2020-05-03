"""
Actions are what the actors do, possibly requiring use of their abilities.
Ask your actors to perform actions by passing the actions into their
|Actor.was_able_to| or |Actor.attempts_to| method.
"""


from .accept_alert import AcceptAlert
from .base_action import BaseAction
from .chain import Chain
from .clear import Clear
from .click import Click
from .debug import Debug
from .dismiss_alert import DismissAlert
from .double_click import DoubleClick
from .enter import Enter
from .enter_2fa_token import Enter2FAToken
from .go_back import GoBack
from .go_forward import GoForward
from .hold_down import HoldDown
from .move_mouse import MoveMouse
from .open import Open
from .pause import Pause
from .refresh_page import RefreshPage
from .release import Release
from .respond_to_the_prompt import RespondToThePrompt
from .right_click import RightClick
from .select import Select, SelectByIndex, SelectByText, SelectByValue
from .switch_to import SwitchTo
from .switch_to_tab import SwitchToTab
from .wait import Wait

# Natural-language-enabling syntactic sugar
ContextClick = RightClick
Hover = MoveMouse
Press = Enter
Refresh = Reload = ReloadPage = RefreshPage
RespondToPrompt = RespondToThePrompt
Sleep = Pause
SwitchToWindow = SwitchToTab
Visit = Open


__all__ = [
    "AcceptAlert",
    "BaseAction",
    "Chain",
    "Clear",
    "Click",
    "ContextClick",
    "Debug",
    "DismissAlert",
    "DoubleClick",
    "Enter",
    "Enter2FAToken",
    "GoBack",
    "GoForward",
    "HoldDown",
    "Hover",
    "MoveMouse",
    "Open",
    "Pause",
    "Press",
    "Refresh",
    "RefreshPage",
    "Release",
    "Reload",
    "ReloadPage",
    "RespondToPrompt",
    "RespondToThePrompt",
    "RightClick",
    "Select",
    "SelectByIndex",
    "SelectByText",
    "SelectByValue",
    "Sleep",
    "SwitchTo",
    "SwitchToTab",
    "SwitchToWindow",
    "Wait",
]
