"""Settings that affect ScreenPy's behavior."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

if TYPE_CHECKING:
    from typing import Any

    from pydantic.fields import FieldInfo

if sys.version_info >= (3, 11):
    try:
        import tomllib
    except ImportError:
        if not TYPE_CHECKING:
            # Help users on older alphas
            import tomli as tomllib
else:
    import tomli as tomllib


# The logic in PyprojectTomlConfig was taken and adapted from Black:
# https://github.com/psf/black/blob/main/src/black/files.py


class PyprojectTomlConfig(PydanticBaseSettingsSource):
    """Load setting configuration from pyproject.toml."""

    toml_config: dict[str, Any] | None

    def __init__(self, settings_cls: type[BaseSettings]) -> None:
        super().__init__(settings_cls)
        self.toml_config = None

    def _parse_pyproject_toml(self) -> dict[str, Any]:
        """Parse the pyproject.toml file and extract the relevant information."""
        pyproject_path = Path.cwd() / "pyproject.toml"
        if not pyproject_path.is_file():
            self.toml_config = {}
        else:
            with pyproject_path.open("rb") as f:
                pyproject_toml = tomllib.load(f)
            toml_config: dict[str, Any] = pyproject_toml.get("tool", {})
            if hasattr(self.settings_cls, "_tool_path"):
                tool_path = self.settings_cls._tool_path.get_default()
            else:
                tool_path = ""
            tool_steps = tool_path.split(".")
            for subtool in tool_steps:
                toml_config = toml_config.get(subtool, {})

            self.toml_config = toml_config

        return self.toml_config

    def get_field_value(self, _: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        """Retrieve the field's value from the toml config.

        This method overrides an abstract method in the abstract base class.

        Args:
            field: the field to look up.
            field_name: the name of the field to look up.

        Returns:
            (The value, the field_name, whether the value is a JSON object)
        """
        if self.toml_config is None:
            toml_config = self._parse_pyproject_toml()
        else:
            toml_config = self.toml_config

        return toml_config.get(field_name), field_name, False

    def prepare_field_value(
        self,
        field_name: str,  # noqa: ARG002
        field: FieldInfo,  # noqa: ARG002
        value: Any,  # noqa: ANN401
        value_is_complex: bool,  # noqa: ARG002, FBT001
    ) -> Any:  # noqa: ANN401
        """Return the value as-is, we do not need to prepare it.

        This method overrides an abstract method in the abstract base class.
        """
        return value

    def __call__(self) -> dict[str, Any]:
        """Generate the config information."""
        toml_config: dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex=value_is_complex
            )
            if field_value is not None:
                toml_config[field_key] = field_value

        return toml_config


class ScreenPySettings(BaseSettings):
    """Settings for ScreenPy.

    To change these settings using environment variables, use the prefix
    ``SCREENPY_``, like so::

        SCREENPY_TIMEOUT=60   # sets the default timeout length to 60 seconds
    """

    _tool_path = "screenpy"
    model_config = SettingsConfigDict(env_prefix="SCREENPY_", frozen=False)

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

    @classmethod
    def settings_customise_sources(  # noqa: PLR0913
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,  # noqa: ARG003
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Set the order of preference of settings sources."""
        return (
            init_settings,
            env_settings,
            PyprojectTomlConfig(settings_cls),
            file_secret_settings,
        )


# initialized instance
settings = ScreenPySettings()
