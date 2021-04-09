"""
Abilities provide an API for actors to use other libraries to perform
actions.
"""


from .authenticate_with_2fa import AuthenticateWith2FA
from .browse_the_web import BrowseTheWeb
from .make_api_requests import MakeAPIRequests

__all__ = [
    "AuthenticateWith2FA",
    "BrowseTheWeb",
    "MakeAPIRequests",
]
