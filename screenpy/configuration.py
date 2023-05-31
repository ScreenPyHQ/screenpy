"""
Settings that affect ScreenPy's behavior.
"""

import sys
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple

from pydantic import BaseSettings
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


# The following pyproject.toml functions were taken and adapted from Black:
# https://github.com/psf/black/blob/main/src/black/files.py


@lru_cache()
def _find_project_root() -> Tuple[Path, str]:
    """Return a directory containing .git, .hg, or pyproject.toml.

    That directory will be a common parent of all files and directories
    passed in `srcs`.

    If no directory in the tree contains a marker that would specify it's the
    project root, the root of the file system is returned.

    Returns a two-tuple with the first element as the project root path and
    the second element as a string describing the method by which the
    project root was discovered.
    """
    path_srcs = [Path.cwd()]

    # A list of lists of parents for each 'src'. 'src' is included as a
    # "parent" of itself if it is a directory
    src_parents = [
        list(path.parents) + ([path] if path.is_dir() else []) for path in path_srcs
    ]

    common_base = max(
        set.intersection(*(set(parents) for parents in src_parents)),
        key=lambda path: path.parts,
    )

    for directory in (common_base, *common_base.parents):
        if (directory / ".git").exists():
            return directory, ".git directory"

        if (directory / ".hg").is_dir():
            return directory, ".hg directory"

        if (directory / "pyproject.toml").is_file():
            return directory, "pyproject.toml"

    return common_base, "file system root"


def _find_pyproject_toml() -> Optional[Path]:
    """Find the absolute filepath to a pyproject.toml if it exists"""
    path_project_root, _ = _find_project_root()
    path_pyproject_toml = path_project_root / "pyproject.toml"
    if path_pyproject_toml.is_file():
        return path_pyproject_toml
    return None


def _parse_pyproject_toml(
    filepath: Optional[Path], settings_class: BaseSettings
) -> Dict[str, Any]:
    """Parse a pyproject toml file, pulling out relevant parts for ScreenPy.

    If parsing fails, will raise a tomllib.TOMLDecodeError.
    """
    if filepath is None:
        return {}

    with filepath.open("rb") as f:
        pyproject_toml = tomllib.load(f)
    allowed_keys = settings_class.schema()["properties"]
    toml_config: Dict[str, Any] = pyproject_toml.get("tool", {})
    tool_paths = getattr(settings_class, "_tool_path", "").split(".")
    for subtool in tool_paths:
        toml_config = toml_config.get(subtool, {})
    toml_config = {
        k.replace("--", "").replace("-", "_"): v
        for k, v in toml_config.items()
        if k in allowed_keys
    }

    return toml_config


def pyproject_settings(settings_class: BaseSettings) -> Dict[str, Any]:
    """Retrieve the ``pyproject.toml`` settings for ScreenPy.

    For more information, see Pydantic's documentation:
    https://docs.pydantic.dev/usage/settings/#adding-sources
    """
    pyproject_path = _find_pyproject_toml()
    project_settings = _parse_pyproject_toml(pyproject_path, settings_class)
    return project_settings


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

    class Config:  # pylint: disable=missing-class-docstring
        env_prefix = "SCREENPY_"
        allow_mutation = True

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            """Set the order of preference of settings sources."""
            return init_settings, env_settings, pyproject_settings, file_secret_settings


# initialized instance
settings = ScreenPySettings()
