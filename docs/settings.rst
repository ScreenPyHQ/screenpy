========
Settings
========

To configure ScreenPy,
we provide some settings
through `Pydantic's settings management <https://docs.pydantic.dev/usage/settings/>`__.

Settings can be configured through three ways:

  * Directly modifying the ``settings`` object in your test configuration.
  * Using environment variables.
  * In the ``[tool.screenpy]`` section in your ``pyproject.toml``.

The above three options are in order of precedence;
that is,
modifying ``settings`` directly will override any environment variables,
any environment variables will override any ``pyproject.toml`` settings,
and any ``pyproject.toml`` settings will override the defaults.

To demonstrate,
here is how we can change the default timeout value
used by things like :class:`screenpy.actions.Eventually`::

    # in your suite setup file, like conftest.py
    from screenpy.settings import settings

    settings.TIMEOUT = 60

.. code-block:: toml

    # in your pyproject.toml file
    [tool.screenpy]
    TIMEOUT = 60

.. code-block:: bash

    $ # in your shell
    $ SCREENPY_TIMEOUT=60 pytest


ScreenPy Default Settings
-------------------------

.. autopydantic_settings:: screenpy.settings.ScreenPySettings
    :exclude-members: Config.customise_sources

ScreenPy StdOutAdapter Default Settings
---------------------------------------

.. autopydantic_settings:: screenpy.settings.StdOutAdapterSettings
    :exclude-members: Config.customise_sources
