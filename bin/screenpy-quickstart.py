#!/usr/bin/env python3
"""
A helpful script to setup a Screenplay Pattern scaffold. You can run it
in the directory where you want your suite to be created like so:

    $ ./screenpy-quickstart.py

This script will create the following structure in the current working
directory:

__init__.py
features/
 - __init__.py
 - test_example.py
tasks/
 - __init__.py
 - start.py
ui/
 - __init__.py
 - home_page.py
"""

import os
import sys
from pathlib import Path


def create_module(name: str, filename: str, contents: str) -> None:
    """
    Create one of the many modules for ScreenPy.

    Args:
        name: the name of the module, e.g. "tasks".
        filename: the name of the file to create in the module.
        contents: what to write in the file.
    """
    print(f"Creating {name} directory and files...")
    try:
        os.mkdir(name)
        Path(f"{name}/__init__.py").touch()
        with open(f"{name}/{filename}", "w") as modulefile:
            modulefile.write(contents)
    except FileExistsError:
        print(f"> Directory {name} already exists! Skipping.")


print(
    f"""
    This script will set up the scaffolding for your new ScreenPy project.
    It will create several folders and files in the current directory:
         {os.getcwd()}
    For more information, see
    https://screenpy-docs.readthedocs.io/en/latest/filehierarchy.html
"""
)
response = input("Would you like to continue? [Y/n]: ")
if response and response[0].lower() != "y":
    print("OK! Goodbye!")
    sys.exit(0)

print("OK! This should only take a second.\n")


Path("__init__.py").touch()


create_module(
    "ui",
    "home_page.py",
    '''"""
Locators and the URL for ScreenPy's ReadTheDocs homepage.
"""

from screenpy import Target

URL = "https://screenpy-docs.readthedocs.io/en/latest/"

WELCOME_MESSAGE = Target.the("welcome message").located_by(
    "#welcome-to-screenpy-s-documentation>h1"
)

''',
)


create_module(
    "tasks",
    "start.py",
    '''"""
A very simple Task to give you an idea of what a Task might be or do. An actor
must possess the ability to BrowseTheWeb to perform this task. An actor
performs this task like so:

    the_actor.attempts_to(Start.on_the_homepage())
"""

from screenpy import AnActor
from screenpy.actions import Open

from ..ui import home_page


class Start:
    """
    A very simple task that starts on the ScreenPy docs homepage.
    """

    @staticmethod
    def on_the_homepage() -> "Start":
        """Sets the URL to be the homepage."""
        return Start(home_page.URL)

    def perform_as(self, the_actor: AnActor) -> None:
        """
        Asks the actor to visit the specified URL in their browser.

        Args:
            the_actor: the actor who will perform this task.

        Raises:
            UnableToPerformException: if the actor does not possess the
                ability to BrowseTheWeb.
        """
        the_actor.attempts_to(Open.their_browser_on(self.location))

    def __init__(self, location: str) -> None:
        self.location = location

''',
)


create_module(
    "features",
    "test_example.py",
    '''"""
Two very simple example tests that assert the welcome message on ScreenPy's
ReadTheDocs homepage contains "ScreenPy". This test module includes an example
following the unittest.TestCase style and an example using pytest fixtures.
You will probably want to only follow one style.
"""

from selenium.webdriver import Firefox
from screenpy import AnActor, given, when, then
from screenpy.abilities import BrowseTheWeb
from screenpy.questions import Text
from screenpy.resolutions import ContainsTheText

from ..tasks.start import Start
from ..ui.home_page import WELCOME_MESSAGE


# Example using unittest.TestCase
from unittest import TestCase


class TestExample(TestCase):
    """
    A simple example to show a test using unittest.TestCase.
    """

    def setUp(self):
        self.actor = AnActor.named("Tester").who_can(
            BrowseTheWeb.using(Firefox())
        )

    def test_open_homepage(self):
        """Tests that the user can visit the homepage. Extend me!"""
        Actor = self.actor

        given(Actor).was_able_to(Start.on_the_homepage())
        # ... fill in your test steps here!
        then(Actor).should_see_the(
            (Text.of_the(WELCOME_MESSAGE), ContainsTheText("ScreenPy"))
        )

    def tearDown(self):
        self.actor.exit_stage_right()


# Example using pytest
import pytest


@pytest.fixture(scope="function")
def TheActor():
    """A simple Actor fixture for the pytest example"""
    the_actor = AnActor.named("Tester").who_can(BrowseTheWeb.using(Firefox()))
    yield the_actor
    the_actor.exit_stage_left()


def test_open_homepage_pytest(TheActor):
    """A simple example to show a test using pytest fixtures"""
    given(TheActor).was_able_to(Start.on_the_homepage())
    # ... fill in your test steps here!
    then(TheActor).should_see_the(
        (Text.of_the(WELCOME_MESSAGE), ContainsTheText("ScreenPy"))
    )

''',
)


print(
    """
Done! 🎉
Next steps:
    - Try a test run with `python3 -m pytest features/`
    - Remove or modify any of the files created by this script, or add new ones!
    - Continue maintaining and extending your Screenplay Pattern test suite :)
"""
)
