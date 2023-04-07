"""Define settings for the StdOutAdapter."""

from pydantic import BaseSettings

from screenpy.settings import ScreenPySettings


class StdOutAdapterSettings(BaseSettings):
    """Settings for the StdOutAdapter

    To change these settings using environment variables, use the prefix
    ``SCREENPY_STDOUTADAPTER_``, like so::

        SCREENPY_STDOUTADAPTER_INDENT_CHAR=">"  # sets the indent char to >
    """

    tool_path = "screenpy.stdoutadapter"

    INDENT_LOGS: bool = True
    """Whether or not to use indentation in logging."""

    INDENT_CHAR: str = " "
    """Which character to use for indentation."""

    INDENT_SIZE: int = 4
    """How many indent_chars to use for each level of indentation."""

    class Config(ScreenPySettings.Config):  # pylint: disable=missing-class-docstring
        env_prefix = "SCREENPY_STDOUTADAPTER_"


# initialized instance
config = StdOutAdapterSettings()
