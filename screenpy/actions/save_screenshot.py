"""
Save a screenshot.
"""

import os
from typing import Any, Optional

from screenpy.abilities import BrowseTheWeb
from screenpy.actor import Actor
from screenpy.pacing import beat

from .attach_the_file import AttachTheFile


class SaveScreenshot:
    """Save a screenshot from the actor's browser.

    Use the ``and_attach_it`` method to indicate that this screenshot should
    be attached to all reports through the Narrator's adapters. This method
    also accepts any keyword arguments those adapters might require.

    Examples::

        the_actor.attempts_to(SaveScreenshot("screenshot.png"))

        the_actor.attempts_to(SaveScreenshot.as_(filepath))

        the_actor.attempts_to(SaveScreenshot.as_(filepath).and_attach_it())

        the_actor.attempts_to(
            SaveScreenshot.as_(filepath).and_attach_it_with(
                attachment_type=AttachmentTypes.PNG,
            ),
        )
    """

    attach_kwargs: Optional[dict]

    @staticmethod
    def as_(path: str) -> "SaveScreenshot":
        """Supply the name and/or filepath for the screenshot.

        If only a name is supplied, the screenshot will appear in the current
        working directory.
        """
        return SaveScreenshot(path)

    def and_attach_it(self, **kwargs: Any) -> "SaveScreenshot":
        """Indicate the screenshot should be attached to any reports.

        This method accepts any additional keywords needed by any adapters
        attached to the Narrator's microphone.
        """
        self.attach_kwargs = kwargs
        return self

    and_attach_it_with = and_attach_it

    @beat("{} saves a screenshot as {filename}")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the actor to save a screenshot."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        screenshot = browser.get_screenshot_as_png()

        with open(self.path, "wb+") as screenshot_file:
            screenshot_file.write(screenshot)

        if self.attach_kwargs is not None:
            the_actor.attempts_to(AttachTheFile(self.path, **self.attach_kwargs))

    def __init__(self, path: str) -> None:
        self.path = path
        self.filename = path.split(os.path.sep)[-1]
        self.attach_kwargs = None
