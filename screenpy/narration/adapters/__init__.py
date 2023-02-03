"""
Default Adapters for the Narrator's microphone.
"""


from .stdout_adapter import StdOutAdapter

LoggingAdapter = StdOutAdapter

__all__ = [
    "LoggingAdapter",
    "StdOutAdapter",
]
