.. _settings:

Settings
========

To configure ScreenPy,
there are some settings available.

Currently the only way to change these settings
is to import the module
and edit the values.
If anyone knows how to tie in to things like
pyproject.toml,
tox.ini,
etc.—please,
feel free to contribute!

Here is an example
which will turn Action logging off::

    # in your suite setup file, like conftest.py
    from screenpy import settings

    settings.LOG_ACTIONS = False

