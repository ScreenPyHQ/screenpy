"""
Default Adapters for the Narrator's microphone.
"""


from .stdout_adapter import StdOutAdapter, StdOutManager

LoggingAdapter = StdOutAdapter

__all__ = [
    "LoggingAdapter",
    "StdOutAdapter",
    "StdOutManager",
]
