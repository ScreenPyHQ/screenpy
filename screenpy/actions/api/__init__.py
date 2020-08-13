"""
All the actions an actor can perform specific to API testing.
"""

from .send_get_request import SendGETRequest
from .send_head_request import SendHEADRequest

__all__ = [
    "SendGETRequest",
    "SendHEADRequest",
]
