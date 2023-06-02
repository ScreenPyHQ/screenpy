========
Settings
========

To configure ScreenPy,
we provide some settings
through `Pydantic's settings management <https://docs.pydantic.dev/usage/settings/>`__.

Settings can be configured through these ways:

  * In your test configuration file (like conftest.py).
  * Using environment variables.
  * In the ``[tool.screenpy]`` section in your ``pyproject.toml``.

The above options are in order of precedence;
that is,
setting the values directly in your configuration file will override environment variables,
any environment variables will override any ``pyproject.toml`` settings,
and any ``pyproject.toml`` settings will override the defaults.

To demonstrate,
here is how we can change the default timeout value
used by things like :class:`screenpy.actions.Eventually`::

    # in your conftest.py
    from screenpy import settings

    settings.TIMEOUT = 60

.. code-block:: bash

    $ # environment variables in your shell
    $ SCREENPY_TIMEOUT=60 pytest

.. code-block:: toml

    # in your pyproject.toml file
    [tool.screenpy]
    TIMEOUT = 60

The environment variable approach
works particularly well with `python-dotenv <https://pypi.org/project/python-dotenv/>`__!


Adding Settings for Extensions
------------------------------

Extensions to ScreenPy
should follow the conventions set up in :class:`screenpy.configuration.ScreenPySettings`:

 * Add a ``_tool_path`` that looks like "screenpy.extensionname".
 * Add a ``Config`` subclass which inherits from ``ScreenPySettings.Config`` and override ``env_prefix``.

For example,
here is a bare-bones fictional extension settings class::

    from pydantic import BaseSettings

    from screenpy.configuration import ScreenPySettings


    class ScreenPyExampleSettings(BaseSettings):
        _tool_path = "screenpy.example"

        class Config(ScreenPySettings.Config):
            env_prefix = "SCREENPY_EXAMPLE_"

You can also look at the
`StdOutAdapterSettings class <https://github.com/ScreenPyHQ/screenpy/tree/trunk/screenpy/narration/stdout_adapter/configuration.py>`__
to see a concrete example.


Default Settings
----------------

These are the default settings included in ScreenPy.

ScreenPy Default Settings
+++++++++++++++++++++++++

.. autopydantic_settings:: screenpy.configuration.ScreenPySettings

StdOutAdapter Default Settings
++++++++++++++++++++++++++++++

.. autopydantic_settings:: screenpy.narration.stdout_adapter.configuration.StdOutAdapterSettings
