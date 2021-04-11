"""
Abilities allow Actors to perform Actions and ask Questions.
"""


from .authenticate_with_2fa import AuthenticateWith2FA
from .browse_the_web import BrowseTheWeb
from .make_api_requests import MakeAPIRequests

__all__ = [
    "AuthenticateWith2FA",
    "BrowseTheWeb",
    "MakeAPIRequests",
]
