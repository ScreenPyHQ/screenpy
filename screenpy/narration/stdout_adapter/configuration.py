"""Define settings for the StdOutAdapter."""

from pydantic import BaseSettings

from screenpy.configuration import ScreenPySettings


class StdOutAdapterSettings(BaseSettings):
    """Settings for the StdOutAdapter.

    To change these settings using environment variables, use the prefix
    ``SCREENPY_STDOUTADAPTER_``, like so::

        SCREENPY_STDOUTADAPTER_INDENT_CHAR=">"  # sets the indent char to >
    """

    _tool_path = "screenpy.stdoutadapter"

    INDENT_LOGS: bool = True
    """Whether or not to use indentation in logging."""

    INDENT_CHAR: str = " "
    """Which character to use for indentation."""

    INDENT_SIZE: int = 4
    """How many indent_chars to use for each level of indentation."""

    class Config(ScreenPySettings.Config):
        """Inherit from the base Config but change the env_prefix."""

        env_prefix = "SCREENPY_STDOUTADAPTER_"


# initialized instance
settings = StdOutAdapterSettings()
