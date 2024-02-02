"""Default Adapters for the Narrator's microphone."""

from .configuration import settings
from .stdout_adapter import StdOutAdapter, StdOutManager

LoggingAdapter = StdOutAdapter

__all__ = [
    "LoggingAdapter",
    "settings",
    "StdOutAdapter",
    "StdOutManager",
]
