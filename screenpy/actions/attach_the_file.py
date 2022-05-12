"""
Attach a file.
"""

import os
from typing import Any

from screenpy import Actor
from screenpy.pacing import the_narrator


class AttachTheFile:
    """Attach a file for :ref:`Narration`.

    Supports passing arbitrary keyword arguments along to the adapters hooked
    up to the Narrator's microphone.

    Examples::

        the_actor.attempts_to(AttachTheFile(filepath))

        the_actor.attempts_to(
            AttachTheFile(filepath, attachment_type=AttachmentTypes.PNG)
        )
    """

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Attach a file named {self.filename}."

    # no beat, to make reading reports easier.
    def perform_as(self, _: Actor) -> None:
        """Direct the Narrator to attach a file."""
        the_narrator.attaches_a_file(self.filepath, **self.attach_kwargs)

    def __init__(self, filepath: str, **kwargs: Any) -> None:
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.attach_kwargs = kwargs
