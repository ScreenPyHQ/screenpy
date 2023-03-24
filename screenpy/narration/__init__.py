"""
Tools for narrating the screenplay.
"""

from .adapters import LoggingAdapter, StdOutAdapter, StdOutManager
from .gravitas import AIRY, EXTREME, HEAVY, LIGHT, NORMAL
from .narrator import Narrator

__all__ = [
    "AIRY",
    "EXTREME",
    "HEAVY",
    "LIGHT",
    "LoggingAdapter",
    "Narrator",
    "NORMAL",
    "StdOutAdapter",
    "StdOutManager",
]
