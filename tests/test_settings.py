import os
from pathlib import Path
from unittest import mock

from screenpy import settings as screenpy_settings
from screenpy.configuration import PyprojectTomlConfig, ScreenPySettings
from screenpy.narration.stdout_adapter import settings as stdout_adapter_settings
from screenpy.narration.stdout_adapter.configuration import StdOutAdapterSettings


class TestPyprojectTomlConfig:
    def test__parse_pyproject_toml_file_does_not_exist(self) -> None:
        MockedPath = mock.MagicMock(spec=Path)
        MockedPath.cwd.return_value.__truediv__.return_value = MockedPath
        MockedPath.is_file.return_value = False

        pyproject_config = PyprojectTomlConfig(ScreenPySettings)
        pyproject_config._parse_pyproject_toml()

        assert pyproject_config.toml_config == {}

    def test__parse_pyproject_toml_file_exists(self) -> None:
        MockedPath = mock.MagicMock(spec=Path)
        MockedPath.cwd.return_value.__truediv__.return_value = MockedPath
        MockedPath.is_file.return_value = True
        test_data = (
            b"[tool.screenpy]\nTIMEOUT = 500"
            b"\n\n[tool.screenpy.stdoutadapter]\nINDENT_SIZE = 500"
        )
        mock_open = mock.mock_open(read_data=test_data)

        with mock.patch("pathlib.Path.open", mock_open):
            pyproject_config = PyprojectTomlConfig(ScreenPySettings)
            pyproject_config._parse_pyproject_toml()

        assert pyproject_config.toml_config == {
            "TIMEOUT": 500,
            "stdoutadapter": {"INDENT_SIZE": 500},
        }


class TestSettings:
    def test_pyproject_overwrites_initial(self) -> None:
        mock_open = mock.mock_open(read_data=b"[tool.screenpy]\nTIMEOUT = 500")

        with mock.patch("pathlib.Path.open", mock_open):
            settings = ScreenPySettings()

        assert settings.TIMEOUT == 500

    def test_env_overwrites_pyproject(self) -> None:
        mock_open = mock.mock_open(read_data=b"[tool.screenpy]\nTIMEOUT = 500")
        mock_env = {"SCREENPY_TIMEOUT": "1337"}

        with mock.patch("pathlib.Path.open", mock_open):  # noqa: SIM117
            with mock.patch.dict(os.environ, mock_env):
                settings = ScreenPySettings()

        assert settings.TIMEOUT == 1337

    def test_init_overwrites_env(self) -> None:
        mock_env = {"SCREENPY_TIMEOUT": "1337"}

        with mock.patch.dict(os.environ, mock_env):
            settings = ScreenPySettings(TIMEOUT=9001)

        assert settings.TIMEOUT == 9001

    def test_can_be_changed_at_runtime(self) -> None:
        try:
            screenpy_settings.TIMEOUT = 4
        except TypeError as exc:
            msg = "ScreenPySettings could not be changed at runtime."
            raise AssertionError(msg) from exc


class TestStdOutAdapterSettings:
    def test_pyproject_overwrites_initial(self) -> None:
        mock_open = mock.mock_open(
            read_data=b"[tool.screenpy.stdoutadapter]\nINDENT_SIZE = 500"
        )

        with mock.patch("pathlib.Path.open", mock_open):
            settings = StdOutAdapterSettings()

        assert settings.INDENT_SIZE == 500

    def test_env_overwrites_pyproject(self) -> None:
        mock_open = mock.mock_open(
            read_data=b"[tool.screenpy.stdoutadapter]\nINDENT_SIZE = 500"
        )
        mock_env = {"SCREENPY_STDOUTADAPTER_INDENT_SIZE": "1337"}

        with mock.patch("pathlib.Path.open", mock_open):  # noqa: SIM117
            with mock.patch.dict(os.environ, mock_env):
                settings = StdOutAdapterSettings()

        assert settings.INDENT_SIZE == 1337

    def test_init_overwrites_env(self) -> None:
        mock_env = {"SCREENPY_STDOUTADAPTER_INDENT_SIZE": "1337"}

        with mock.patch.dict(os.environ, mock_env):
            settings = StdOutAdapterSettings(INDENT_SIZE=9001)

        assert settings.INDENT_SIZE == 9001

    def test_can_be_changed_at_runtime(self) -> None:
        try:
            stdout_adapter_settings.INDENT_CHAR = "?"
        except TypeError as exc:
            msg = "StdOutAdapterSettings could not be changed at runtime."
            raise AssertionError(msg) from exc


class TestCombo:
    def test_can_set_multiple_tools(self) -> None:
        test_data = (
            b"[tool.screenpy]\nTIMEOUT = 500"
            b"\n\n[tool.screenpy.stdoutadapter]\nINDENT_SIZE = 500"
        )
        mock_open = mock.mock_open(read_data=test_data)

        with mock.patch("pathlib.Path.open", mock_open):
            base_settings = ScreenPySettings()
            adapter_settings = StdOutAdapterSettings()

        assert base_settings.TIMEOUT == 500
        assert adapter_settings.INDENT_SIZE == 500
