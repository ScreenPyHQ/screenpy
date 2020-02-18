"""
Locators and URL for the Alerts page.
"""


from screenpy import Target

URL = "http://the-internet.herokuapp.com/javascript_alerts"

JS_ALERT_BUTTON = Target.the("launch javascript dialog button").located_by(
    'button[onclick="jsAlert()"]'
)
JS_CONFIRM_BUTTON = Target.the("launch javascript dialog button").located_by(
    'button[onclick="jsConfirm()"]'
)
JS_PROMPT_BUTTON = Target.the("launch javascript prompt button").located_by(
    'button[onclick="jsPrompt()"]'
)
RESULT_MESSAGE = Target.the("result message").located_by("#result")
