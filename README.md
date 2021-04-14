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


Documentation
----------
Please check out the [Read The Docs documentation](https://screenpy-docs.readthedocs.io/en/latest/) for the latest information about this module!


Quickstart
----------
Once installed, to set up a Screenplay Pattern scaffolding in your project, `cd` to the folder you will use for your suite and run this command:

    screenpy-quickstart

Note that the Python script directory will need to be on your path to find `screenpy-quickstart`.

This will set up `user_interface`, `tasks`, and `features` directories and fill them with a simple test. For explanations on what these directories are for, see the [File Hierarchy documentation](https://screenpy-docs.readthedocs.io/en/latest/filehierarchy.html)


Allure Integration
------------------

ScreenPy utilizes [Allure](https://github.com/allure-framework) to document the action. If you would like to see an allure report of your Screenplay Suite, run the test using PyTest like so:

    python -m pytest features --alluredir allure_report
    allure serve allure_report


Contributing
------------

You want to contribute? Great! Here are the things you should do before submitting your PR:

1. Install [`pre-commit`](https://pre-commit.com/)
1. run `pre-commit install` once.
1. run `tox` to perform tests frequently.

That's it! :)
