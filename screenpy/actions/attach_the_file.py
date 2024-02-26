"""Attach a file."""

import os
from typing import Any

from screenpy.actor import Actor
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

    @property
    def filename(self) -> str:
        """Get the filename from the filepath."""
        return os.path.basename(self.filepath)

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Attach a file named {self.filename}."

    # no beat, to make reading reports easier.
    def perform_as(self, _: Actor) -> None:
        """Direct the Narrator to attach a file."""
        the_narrator.attaches_a_file(self.filepath, **self.attach_kwargs)

    # ANN401 ignored here to allow for new adapters to use any kwargs.
    def __init__(self, filepath: str, **kwargs: Any) -> None:  # noqa: ANN401
        self.filepath = filepath
        self.attach_kwargs = kwargs
