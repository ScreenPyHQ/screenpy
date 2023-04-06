========
Settings
========

To configure ScreenPy,
we provide some settings
through `Pydantic's settings management <https://docs.pydantic.dev/usage/settings/>`__.

Settings can be configured through three ways:

  * Directly modifying the ``config`` object in your test configuration.
  * Using environment variables.
  * In the ``[tool.screenpy]`` section in your ``pyproject.toml``.

The above three options are in order of precedence;
that is,
modifying ``config`` directly will override everything,
any environment variables will override any ``pyproject.toml`` settings,
and any ``pyproject.toml`` settings will override the defaults.

To demonstrate,
here is how we can change the default timeout value
used by things like :class:`screenpy.actions.Eventually`::

    # in your suite setup file, like conftest.py
    from screenpy import config

    config.TIMEOUT = 60

.. code-block:: toml

    # in your pyproject.toml file
    [tool.screenpy]
    TIMEOUT = 60

.. code-block:: bash

    $ # in your shell
    $ SCREENPY_TIMEOUT=60 pytest

The environment variable approach
works particularly well with `python-dotenv <https://pypi.org/project/python-dotenv/>`__!


ScreenPy Default Settings
-------------------------

.. autopydantic_settings:: screenpy.settings.ScreenPySettings
    :exclude-members: Config.customise_sources

ScreenPy StdOutAdapter Default Settings
---------------------------------------

.. autopydantic_settings:: screenpy.settings.StdOutAdapterSettings
    :exclude-members: Config.customise_sources
