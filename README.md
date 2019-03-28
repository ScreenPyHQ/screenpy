ScreenPy
========
```
TITLE CARD:
                                  "ScreenPy"
TITLE DISAPPEARS.
                                                                      FADE IN:
INT. DOCUMENTATION - NIGHT

Illuminated by the computer's glow, AUDIENCE sits reading the documentation
for a Python library they haven't seen before. AUDIENCE is visibly startled
as a dulcet voice begins to speak.

                              NARRATOR (V.O.)
            ScreenPy is a library that provides the base for an
            automated test suite using Screenplay Pattern.

                              AUDIENCE
            Wha- who are you? Where are you? And... what is
            Screenplay Pattern?!

                              NARRATOR (V.O.)
            It's a composition-based architecture pattern,
            encouraging automated test writers to write more
            maintainable test suites. It allows test writers to
            use Gherkin-style language in Python to create
            descriptive UI tests.

                              AUDIENCE
                              (reluctantly)
            Ignoring how you avoided answering my first questions,
            how do I get started?

                              NARRATOR (V.O.)
            I thought you'd never ask...

                                                                      FADE OUT
```

Installation
------------
    pip install screenpy

QuickStart
----------
```python
from selenium.webdriver import Firefox

from screenpy.actions.click import Click
from screenpy.actions.open import Open
from screenpy.actors.actor import AnActor
from screenpy.abilities.browse_the_web import BrowseTheWeb
from screenpy.given_when_then import given, when, then
from screenpy.questions.text import Text
from screenpy.resolutions import ReadsExactly
from screenpy.target import Target

# This would normally go in your tasks/start.py
class Start(object):
    """Test case start points"""
    def perform_as(self, actor):
        actor.attempts_to(Open.browser_on(self.location))
    @staticmethod
    def on_the_screenpy_repo():
        return Start("https://github.com/perrygoy/screenpy")
    def __init__(self, location):
        self.location = location

# These two would normally go in your user_interface/some_page.py
THE_AUTHOR_LINK = Target.the("repository author link").located_by("a[rel=author]")
THE_DISPLAYED_USER_NAME = Target.the("GitHub user's name").located_by("span.vcard-fullname")

# This would normally go in your questions/user_name.py
class UserName(object):
    """Questions about the user name"""
    def answered_by(self, the_actor):
        return Text.of(THE_DISPLAYED_USER_NAME).viewed_by(the_actor)
    @staticmethod
    def text():
        return UserName()

perry = AnActor.named("Perry").who_can(BrowseTheWeb.using(Firefox()))

given(perry).was_able_to(Start.on_the_screenpy_repo())
when(perry).attempts_to(Click.on(THE_AUTHOR_LINK).then_wait_for(THE_DISPLAYED_USER_NAME))
then(perry).should_see_the((UserName.text(), ReadsExactly("Perry Goy")),)
perry.exit_stage_right()
```

You may think to yourself, man, that's a lot of setup for a simple quickstart. And you're definitely right! There are a lot of moving parts to a Screenplay Pattern test suite. If you want to know more, please check out the [Read The Docs documentation!](https://screenpy-docs.readthedocs.io/en/latest/)


Allure Integration
------------------

ScreenPy utilizes [Allure](https://github.com/allure-framework) to document the action. If you would like to see an allure report of your Screenplay Suite, run the test using PyTest like so:

    python -m pytest features --allure_dir allure_report
    allure serve allure_report
