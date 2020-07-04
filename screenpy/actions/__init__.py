"""
Actions are what the actors do, possibly requiring use of their abilities.
Ask your actors to perform actions by passing the actions into their
|Actor.was_able_to| or |Actor.attempts_to| method.
"""


from .web.accept_alert import AcceptAlert
from .web.chain import Chain
from .web.clear import Clear
from .web.click import Click
from .web.debug import Debug
from .web.dismiss_alert import DismissAlert
from .web.double_click import DoubleClick
from .web.enter import Enter
from .web.enter_2fa_token import Enter2FAToken
from .web.go_back import GoBack
from .web.go_forward import GoForward
from .web.hold_down import HoldDown
from .web.move_mouse import MoveMouse
from .web.open import Open
from .web.pause import Pause
from .web.refresh_page import RefreshPage
from .web.release import Release
from .web.respond_to_the_prompt import RespondToThePrompt
from .web.right_click import RightClick
from .web.select import Select, SelectByIndex, SelectByText, SelectByValue
from .web.switch_to import SwitchTo
from .web.switch_to_tab import SwitchToTab
from .web.wait import Wait

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
    "Visit",
    "Wait",
]
