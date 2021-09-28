"""
Attach a file.
"""

from typing import Any

from screenpy import Actor
from screenpy.pacing import the_narrator


class AttachTheFile:
    """Attach a file to the Narrator's reports.

    Supports passing arbitrary keyword arguments along to the adapters hooked
    up to the Narrator's microphone.

    Examples::

        the_actor.attempts_to(AttachTheFile(filepath))

        the_actor.attempts_to(
            AttachTheFile(filepath, attachment_type=AttachmentTypes.PNG)
        )
    """

    # no beat, to make reading reports easier.
    def perform_as(self, _: Actor) -> None:
        """Direct the Narrator to attach a file."""
        the_narrator.attaches_a_file(self.path, **self.attach_kwargs)

    def __init__(self, path: str, **kwargs: Any) -> None:
        self.path = path
        self.attach_kwargs = kwargs
