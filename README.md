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
            It's a composition-based approach to writing
            maintainable test suites, counter to the more popular
            inheritance-based approach Page Object Model. It
            allows test-writers to use Gherkin-style syntax in
            Python to create descriptive UI test cases.

                              AUDIENCE
                              (reluctantly)
            Ignoring how you avoided answering my first questions,
            how do i get started?

                              NARRATOR (V.O.)
            I thought you'd never ask...

                                                                      FADE OUT
```

QuickStart
----------
```python
from selenium.webdriver import Firefox

from screenpy.actions.click import Click
from screenpy.actions.open import Open
from screenpy.actors.actor import Actor
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

AUTHOR_LINK = Target.the("Repository author link").located_by("a[rel=author]")
USER_NAME = Target.the("GitHub user's name").located_by("span.vcard-fullname")

# This would normally go in your questions/user_name.py
class UserName(object):
    """Questions about the user name"""
    def answered_by(self, the_actor):
        return Text.of(USER_NAME).viewed_by(the_actor)
    @staticmethod
    def text():
        return UserName()

perry = Actor.named("Perry").who_can(BrowseTheWeb.using(Firefox()))

given(perry).was_able_to(Start.on_the_screenpy_repo())
when(perry).attempts_to(Click.on(AUTHOR_LINK).then_wait_for(USER_NAME))
then(perry).should_see_that((UserName.text(), ReadsExactly("Perry Goy")),)
perry.exit()
```

You may think to yourself, man, that's a lot of setup for a simple quickstart. And you're definitely right! There are a lot of moving parts to a Screenplay Pattern test suite. If you want to know more, please read on!

Suite Hierarchy
---------------

```
- suite_root
  - features        # this is where the actual test files will live
      feature1.py
      ...
  - questions       # questions your actors will ask about the site
      question1.py
      ...
  - tasks           # groups of actions your actors can perform
      task1.py
      ...
  - user_interface  # files containing locators for each page
      page1.py
      ...
  requirements.txt  # where you list screenpy!
```

The examples in [Examples](/examples) all follow the naming and organization conventions outlined just above, but the specific names of the directories in your suite have no bearing on ScreenPy. If a directory makes more sense under a different name to you and your team, by all means use that name instead.

Let's talk more about what each of these file types are, though!

### Features

The features folder is where your tests will live. The folder can also be named `tests` or `stories`, whatever your group is most comfortable with. These files will be focused on testing exactly one feature of your application, hence the name.

These files will inherit from your TestCase object of choice and contain your actors' performances.

### Questions

Questions are things your actors will ask about the webpage with the intention of asserting something is true about the answer. The `RepositoryName` class in the [QuickStart][QuickStart] section of this README has a comment above it, mentioning that it usually belongs in this folder, in its own dedicated file. That is true.

What is the text currently in the welcome header of the page? How many of this target exist? These are good questions your actors can ask.

Questions will all need a `answered_by` method that takes in the parameters `(self, the_actor)`. In it, return the question(s) provided by ScreenPy or your own suite that make up the answer to the question you're asking.

### Tasks

These are groupings of actions that your actors will perform. The `Start` class in the [QuickStart][QuickStart] section of this README has a comment above it, mentioning that it usually belongs in this folder, in its own dedicated file. That is also true.

Tasks will all need a `perform_as` method that takes in the parameters `(self, the_actor)`. In it, call `the_actor.attempts_to(action1, action2, action3, ...)`

### User Interface

Automation needs locators, and this is where they live. Using the Target class, specify any number of locators in each file, grouped however you like. Some folks like grouping them by page, some by module, still others by some arcane metrick. Incidentally, that is why this directory isn't called something simple like "pages".

Allure Integration
------------------

ScreenPy utilizes Allure in its actions, tasks, and questions. If you would like to see an allure report of your Screenplay Suite, run the test using PyTest like so:

    python -m pytest features --allure_dir allure_report
    allure serve allure_report

Additional Context
------------------

As mentioned in the introduction, Screenplay Pattern uses composition instead of inheritance to form the test suite. The concept was first formed by Antony Marcano—frustrated with Page Object Model files growing unreasonably large—under the name the Journey Pattern. You can watch [Antony's talk about Screenplay Pattern at SeleniumConf2016](https://www.youtube.com/watch?v=8f8tdZBvAbI "The Screenplay Pattern - a SOLID alternative to Page Objects | Antony Marcano"), which is the same talk that got me interested in this pattern!
