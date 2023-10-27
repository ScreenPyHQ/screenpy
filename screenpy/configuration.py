"""Settings that affect ScreenPy's behavior."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import BaseSettings

if TYPE_CHECKING:
    from typing import Any

    from pydantic.env_settings import SettingsSourceCallable

if sys.version_info >= (3, 11):
    try:
        import tomllib
    except ImportError:
        if not TYPE_CHECKING:
            # Help users on older alphas
            import tomli as tomllib
else:
    import tomli as tomllib


# The following pyproject.toml function was taken and adapted from Black:
# https://github.com/psf/black/blob/main/src/black/files.py


def _parse_pyproject_toml(tool_path: str) -> dict[str, Any]:
    """Parse a pyproject toml file, pulling out relevant parts for ScreenPy.

    If parsing fails, will raise a tomllib.TOMLDecodeError.

    Args:
        tool_path: dotted-path for the tool, like "screenpy.stdoutadapter"

    Returns:
        Dict[str, Any]: the pyproject.toml settings under the tool_path.
    """
    pyproject_path = Path.cwd() / "pyproject.toml"
    if not pyproject_path.is_file():
        return {}

    with pyproject_path.open("rb") as f:
        pyproject_toml = tomllib.load(f)
    toml_config: dict[str, Any] = pyproject_toml.get("tool", {})
    tool_steps = tool_path.split(".")
    for subtool in tool_steps:
        toml_config = toml_config.get(subtool, {})

    return toml_config


def pyproject_settings(settings_class: BaseSettings) -> dict[str, Any]:
    """Retrieve the ``pyproject.toml`` settings for a ScreenPy settings class.

    For more information, see Pydantic's documentation:
    https://docs.pydantic.dev/usage/settings/#adding-sources

    Args:
        settings_class: the ScreenPy settings class to populate. This class
            should have a ``_tool_path`` set, which will inform this function
            of where to find its settings in pyproject.toml.

    Returns:
        Dict[str, Any]: the pyproject.toml settings for the settings_class.
    """
    tool_path = getattr(settings_class, "_tool_path", "")
    toml_config = _parse_pyproject_toml(tool_path)

    allowed_keys = settings_class.schema()["properties"]
    return {
        k.replace("--", "").replace("-", "_"): v
        for k, v in toml_config.items()
        if k in allowed_keys
    }


class ScreenPySettings(BaseSettings):
    """Settings for ScreenPy.

    To change these settings using environment variables, use the prefix
    ``SCREENPY_``, like so::

        SCREENPY_TIMEOUT=60   # sets the default timeout length to 60 seconds
    """

    _tool_path = "screenpy"

    TIMEOUT: float = 20
    """
    Default timeout (in seconds) to use for things that wait
    (e.g. :class:`~screenpy.actions.Eventually`).
    """

    POLLING: float = 0.5
    """
    Default polling interval (in seconds) to use for things that poll
    (e.g. :class:`~screenpy.actions.Eventually`).
    """

    UNABRIDGED_NARRATION: bool = False
    """
    If True, :class:`~screenpy.actions.Silently` is turned off, allowing
    all Narration. False by default.
    """

    class Config:  # noqa: D106
        env_prefix = "SCREENPY_"
        allow_mutation = True

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            """Set the order of preference of settings sources."""
            return init_settings, env_settings, pyproject_settings, file_secret_settings


# initialized instance
settings = ScreenPySettings()
