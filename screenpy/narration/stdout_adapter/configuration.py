"""Define settings for the StdOutAdapter."""

from pydantic_settings import SettingsConfigDict

from screenpy.configuration import ScreenPySettings


class StdOutAdapterSettings(ScreenPySettings):
    """Settings for the StdOutAdapter.

    To change these settings using environment variables, use the prefix
    ``SCREENPY_STDOUTADAPTER_``, like so::

        SCREENPY_STDOUTADAPTER_INDENT_CHAR=">"  # sets the indent char to >
    """

    _tool_path = "screenpy.stdoutadapter"
    model_config = SettingsConfigDict(env_prefix="SCREENPY_STDOUTADAPTER_")

    INDENT_LOGS: bool = True
    """Whether or not to use indentation in logging."""

    INDENT_CHAR: str = " "
    """Which character to use for indentation."""

    INDENT_SIZE: int = 4
    """How many indent_chars to use for each level of indentation."""


# initialized instance
settings = StdOutAdapterSettings()
