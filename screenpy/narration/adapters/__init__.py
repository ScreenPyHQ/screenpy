"""
Default Adapters for the Narrator's microphone.
"""


from .stdout_adapter import StdOutAdapter, StdOutManager, settings

LoggingAdapter = StdOutAdapter

__all__ = [
    "LoggingAdapter",
    "settings",
    "StdOutAdapter",
    "StdOutManager",
]
