ScreenPy
========
[![Build Status](../../actions/workflows/tests.yml/badge.svg)](../../actions/workflows/tests.yml)
[![Build Status](../../actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)

[![Supported Versions](https://img.shields.io/pypi/pyversions/screenpy.svg)](https://pypi.org/project/screenpy)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

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


Contributing
------------
You want to contribute? Great! Here are the things you should do before submitting your PR:

1. Fork the repo and git clone your fork.
1. `dev` install the project package:
   1. `pip install -e .[dev]` 
   1. Optional (poetry users):
      1. `poetry install --extras dev`
1. Run `pre-commit install` once.
1. Run `tox` to perform tests frequently.
1. Create pull-request from your branch.

That's it! :)
