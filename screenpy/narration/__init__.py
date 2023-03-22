"""
Tools for narrating the screenplay.
"""

from . import adapters
from .adapters import *  # noqa
from .gravitas import AIRY, EXTREME, HEAVY, LIGHT, NORMAL
from .narrator import Narrator

__all__ = [
    "AIRY",
    "EXTREME",
    "HEAVY",
    "LIGHT",
    "Narrator",
    "NORMAL",
]
__all__ += adapters.__all__
