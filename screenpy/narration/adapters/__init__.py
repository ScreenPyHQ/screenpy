"""
Default Adapters for the Narrator's microphone.
"""


from .settings import config
from .stdout_adapter import StdOutAdapter, StdOutManager

LoggingAdapter = StdOutAdapter

__all__ = [
    "config",
    "LoggingAdapter",
    "StdOutAdapter",
    "StdOutManager",
]
