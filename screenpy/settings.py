"""
Settings that affect ScreenPy's behavior.
"""

from pydantic import BaseSettings


class ScreenPySettings(BaseSettings):
    """Settings for ScreenPy.

    These settings can be set in several ways:

     * The defaults defined in here.
     * As environment variables, or in a dotenv file.
     * In ``pyproject.toml`` under ``[tool.screenpy]``.
     * Directly in your test setup::

        from screenpy.settings import settings

        settings.timeout = 60
    """

    tool_path = "screenpy"

    debug = False  # True increases logging
    timeout = 20  # default timeout for things that wait
    polling = 0.5  # default polling interval for things that poll

    class Config:  # pylint: disable=missing-class-docstring
        env_prefix = "SCREENPY_"


class StdOutAdapterSettings(BaseSettings):
    """Settings for the StdOutAdapter"""

    tool_path = "screenpy.stdoutadapter"

    indent_logs = True  # whether or not to use indentation in logging
    indent_char = " "  # which character to use for indentation
    indent_size = 4  # how many indent_chars for each level of indentation

    class Config(ScreenPySettings.Config):  # pylint: disable=missing-class-docstring
        env_prefix = "SCREENPY_STDOUTADAPTER_"


# initialized instance
settings = ScreenPySettings()
