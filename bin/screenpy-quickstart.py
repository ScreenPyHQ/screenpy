#!/usr/bin/env python3


import os
import sys
from pathlib import Path


def create_module(name, filename, contents):
    print(f"Creating {name} directory and files...")
    try:
        os.mkdir(name)
        Path(f"{name}/__init__.py").touch()
        with open(f"{name}/{filename}", "w") as modulefile:
            modulefile.write(contents)
    except FileExistsError:
        print(f"> Directory {name} already exists! Skipping.")


print(f"""
    This script will set up the scaffolding for your new ScreenPy project.
    It will create several folders and files in the current directory:
         {os.getcwd()}
    For more information, see https://screenpy-docs.readthedocs.io/en/latest/filehierarchy.html
""")
response = input("Would you like to continue? [Y/n]: ")
if response and response[0].lower() != 'y':
    print("OK! Goodbye!")
    sys.exit(0)

print("OK! This should take only a second.\n")


Path("__init__.py").touch()


create_module(
    "user_interface",
    "home_page.py",
    """from screenpy import Target


url = "https://screenpy-docs.readthedocs.io/en/latest/"

WELCOME_MESSAGE = Target.the("welcome message").located_by(
    "#welcome-to-screenpy-s-documentation>h1"
)
"""
)


create_module(
    "tasks",
    "start.py",
    """from screenpy.actions import Open

from ..user_interface import home_page


class Start:
    @staticmethod
    def on_the_homepage():
        return Start(home_page.url)

    def perform_as(self, actor):
        actor.attempts_to(Open.browser_on(self.location))

    def __init__(self, location):
        self.location = location

"""
)


create_module(
    "questions",
    "welcome_message.py",
    """from screenpy.questions import Text
from screenpy.pacing import beat

from ..user_interface import home_page


class WelcomeMessage:
    @staticmethod
    def text():
        return WelcomeMessage()

    @beat("{0} checks the welcome message...")
    def answered_by(self, the_actor):
        return Text.of(home_page.WELCOME_MESSAGE).answered_by(the_actor)
"""
)


create_module(
    "features",
    "test_example.py",
    """from unittest import TestCase

from selenium.webdriver import Firefox

from screenpy import AnActor, given, when, then
from screenpy.abilities import BrowseTheWeb
from screenpy.resolutions import ContainsTheText

from ..questions.welcome_message import WelcomeMessage
from ..tasks.start import Start
from ..user_interface import home_page


class TestExample(TestCase):
    def setUp(self):
        self.actor = AnActor.named("Name me!").who_can(BrowseTheWeb.using(Firefox()))

    def test_open_homepage(self):
        "Tests that the user can visit the homepage. Extend me!"
        Actor = self.actor

        given(Actor).was_able_to(Start.on_the_homepage())
        # ... fill in your test steps here!
        then(Actor).should_see_the(
            (WelcomeMessage.text(), ContainsTheText("Welcome to ScreenPy"))
        )

    def tearDown(self):
        self.actor.exit_stage_right()
"""
)


print("""
Done! 🎉
Next steps:
    - Try a test run with `python3 -m pytest features/`
    - Remove or modify any of the files created by this script, or add new ones!
    - Continue maintaining and extending your Screenplay Pattern test suite :)
""")
