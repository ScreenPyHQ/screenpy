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
 - docs_page.py
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
    if not os.path.exists(name):
        print(f"Creating {name} module...")
        os.mkdir(name)

    Path(f"{name}/__init__.py").touch()
    filepath = f"{name}/{filename}"
    if os.path.exists(filepath):
        print(f">     File {filepath} already exists! Skipping.")
    else:
        print(f"      Creating {filepath} file...")
        with open(filepath, "w") as modulefile:
            modulefile.write(contents)


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
    "docs_page.py",
    '''"""
Locators and the URL for ScreenPy's ReadTheDocs homepage.
"""

from screenpy import Target

URL = "https://screenpy-docs.readthedocs.io/en/latest/"

WELCOME_MESSAGE = Target.the("welcome message").located_by(
    "#welcome-to-screenpy-s-documentation>h1"
)
GUIDED_TOUR_LINK = Target.the('homepage "Guided Tour" link').located_by(
    '#guided-tour a[href*="actors.html"]'
)

''',
)

create_module(
    "ui",
    "actors_page.py",
    '''"""
Locators and the URL for ScreenPy's Actors docs page.
"""

from screenpy import Target

URL = "https://screenpy-docs.readthedocs.io/en/latest/topics/actors.html"

UP_NEXT_LINK = Target.the('Actors "Up Next" link').located_by(
    "#up-next a.reference"
)

''',
)

create_module(
    "ui",
    "abilities_page.py",
    '''"""
Locators and the URL for ScreenPy's Abilities docs page.
"""

from screenpy import Target

URL = "https://screenpy-docs.readthedocs.io/en/latest/topics/abilities.html"

UP_NEXT_LINK = Target.the('Abilities "Up Next" link').located_by(
    "#up-next a.reference"
)

''',
)

create_module(
    "ui",
    "targets_page.py",
    '''"""
Locators and the URL for ScreenPy's Targets docs page.
"""

from screenpy import Target

URL = "https://screenpy-docs.readthedocs.io/en/latest/topics/targets.html"

UP_NEXT_LINK = Target.the('Targets "Up Next" link').located_by(
    "#up-next a.reference"
)

''',
)

create_module(
    "ui",
    "actions_page.py",
    '''"""
Locators and the URL for ScreenPy's Actions docs page.
"""

from screenpy import Target

URL = "https://screenpy-docs.readthedocs.io/en/latest/topics/actions.html"

UP_NEXT_LINK = Target.the('Actions "Up Next" link').located_by(
    "#up-next a.reference"
)

''',
)

create_module(
    "ui",
    "questions_page.py",
    '''"""
Locators and the URL for ScreenPy's Questions docs page.
"""

from screenpy import Target

URL = "https://screenpy-docs.readthedocs.io/en/latest/topics/questions.html"

UP_NEXT_LINK = Target.the('Questions "Up Next" link').located_by(
    "#up-next a.reference"
)

''',
)

create_module(
    "ui",
    "resolutions_page.py",
    '''"""
Locators and the URL for ScreenPy's Resolutions docs page.
"""

from screenpy import Target

URL = "https://screenpy-docs.readthedocs.io/en/latest/topics/resolutions.html"

UP_NEXT_SECTION = Target.the('"Up Next" section').located_by(
    "#up-next"
)

''',
)

create_module(
    "tasks",
    "start.py",
    '''"""
A very simple Task to give you an idea of what a task might be or do. An Actor
must possess the Ability to BrowseTheWeb to perform this task. An Actor
performs this task like so:

    the_actor.attempts_to(Start.on_the_docs_page())
"""

from screenpy import AnActor
from screenpy.actions import Open

from ..ui import docs_page


class Start:
    """
    A very simple task that starts on the ScreenPy docs homepage.
    """

    @staticmethod
    def on_the_docs_page() -> "Start":
        """Sets the URL to be the homepage."""
        return Start(docs_page.URL)

    def perform_as(self, the_actor: AnActor) -> None:
        """
        Asks the Actor to visit the specified URL in their browser.

        Args:
            the_actor: the Actor who will perform this task.

        Raises:
            UnableToPerformException: if the Actor does not possess the
                Ability to BrowseTheWeb.
        """
        the_actor.attempts_to(Open.their_browser_on(self.location))

    def __init__(self, location: str) -> None:
        self.location = location

''',
)


create_module(
    "features",
    "test_docs_page.py",
    '''"""
Two very simple example tests that assert the welcome message on ScreenPy's
ReadTheDocs homepage contains "ScreenPy". This test module includes an example
following the unittest.TestCase style and an example using pytest fixtures.
You will probably want to only follow one style.
"""

from selenium.webdriver import Firefox
from screenpy import AnActor, given, when, then
from screenpy.abilities import BrowseTheWeb
from screenpy.actions import Click, See, Wait
from screenpy.questions import Text
from screenpy.resolutions import ContainsTheText

from ..tasks.start import Start
from ..ui import  (
    abilities_page,
    actions_page,
    actors_page,
    docs_page,
    questions_page,
    resolutions_page,
    targets_page,
)


# Example using unittest.TestCase
from unittest import TestCase


class TestDocsPage(TestCase):
    """
    A simple example to show a test using unittest.TestCase.
    """

    def setUp(self):
        self.actor = AnActor.named("Tester").who_can(
            BrowseTheWeb.using(Firefox())
        )

    def test_open_docspage_unittest(self):
        """The user can visit the docs homepage. Quick and easy!"""
        Actor = self.actor

        given(Actor).was_able_to(Start.on_the_docs_page())

        then(Actor).should(
            See.the(
                Text.of_the(docs_page.WELCOME_MESSAGE), ContainsTheText("ScreenPy")
            )
        )

    def test_guided_tour_unittest(self):
        """The user can take the guided tour. A little more steps involved."""
        Actor = self.actor

        given(Actor).was_able_to(Start.on_the_docs_page())

        when(Actor).attempts_to(
            Click.on_the(docs_page.GUIDED_TOUR_LINK),
            Wait.for_the(actors_page.UP_NEXT_LINK).to_appear(),
            Click.on_the(actors_page.UP_NEXT_LINK),
            Wait.for_the(abilities_page.UP_NEXT_LINK).to_appear(),
            Click.on_the(abilities_page.UP_NEXT_LINK),
            Wait.for_the(targets_page.UP_NEXT_LINK).to_appear(),
            Click.on_the(targets_page.UP_NEXT_LINK),
            Wait.for_the(actions_page.UP_NEXT_LINK).to_appear(),
            Click.on_the(actions_page.UP_NEXT_LINK),
            Wait.for_the(questions_page.UP_NEXT_LINK).to_appear(),
            Click.on_the(questions_page.UP_NEXT_LINK),
            Wait.for_the(resolutions_page.UP_NEXT_SECTION).to_appear(),
        )

        then(Actor).should(
            See.the(
                Text.of_the(resolutions_page.UP_NEXT_SECTION),
                ContainsTheText("concludes here!"),
            ),
            See.the(
                Text.of_the(resolutions_page.UP_NEXT_SECTION),
                ContainsTheText("Thanks for using ScreenPy!"),
            ),
        )

    def tearDown(self):
        self.actor.exit_stage_right()


# Example using pytest
import pytest


@pytest.fixture(scope="function")
def TheActor():
    """A simple Actor fixture for the pytest example"""
    the_actor = AnActor.named("Tester").who_can(BrowseTheWeb.using_firefox())
    yield the_actor
    the_actor.exit_stage_left()


def test_open_docspage_pytest(TheActor):
    """A simple example to show a test using pytest fixtures"""
    given(TheActor).was_able_to(Start.on_the_docs_page())

    then(TheActor).should(
        See.the(Text.of_the(docs_page.WELCOME_MESSAGE), ContainsTheText("ScreenPy"))
    )

def test_take_guided_tour_pytest(TheActor):
    """A more involved example using pytest fixtures."""
    given(TheActor).was_able_to(Start.on_the_docs_page())

    when(TheActor).attempts_to(
        Click.on_the(docs_page.GUIDED_TOUR_LINK),
        Wait.for_the(actors_page.UP_NEXT_LINK).to_appear(),
        Click.on_the(actors_page.UP_NEXT_LINK),
        Wait.for_the(abilities_page.UP_NEXT_LINK).to_appear(),
        Click.on_the(abilities_page.UP_NEXT_LINK),
        Wait.for_the(targets_page.UP_NEXT_LINK).to_appear(),
        Click.on_the(targets_page.UP_NEXT_LINK),
        Wait.for_the(actions_page.UP_NEXT_LINK).to_appear(),
        Click.on_the(actions_page.UP_NEXT_LINK),
        Wait.for_the(questions_page.UP_NEXT_LINK).to_appear(),
        Click.on_the(questions_page.UP_NEXT_LINK),
        Wait.for_the(resolutions_page.UP_NEXT_SECTION).to_appear(),
    )

    then(TheActor).should(
        See.the(
            Text.of_the(resolutions_page.UP_NEXT_SECTION),
            ContainsTheText("concludes here!"),
        ),
        See.the(
            Text.of_the(resolutions_page.UP_NEXT_SECTION),
            ContainsTheText("Thanks for using ScreenPy!"),
        ),
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
