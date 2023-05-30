import os
from unittest import mock

import pytest

from screenpy import settings as screenpy_settings
from screenpy.narration.stdout_adapter import settings as stdout_adapter_settings
from screenpy.configuration import ScreenPySettings
from screenpy.narration.stdout_adapter.configuration import StdOutAdapterSettings


class TestSettings:
    def test_pyproject_overwrites_initial(self):
        mock_open = mock.mock_open(read_data=b"[tool.screenpy]\nTIMEOUT = 500")

        with mock.patch("pathlib.Path.open", mock_open):
            settings = ScreenPySettings()

        assert settings.TIMEOUT == 500

    def test_env_overwrites_pyproject(self):
        mock_open = mock.mock_open(read_data=b"[tool.screenpy]\nTIMEOUT = 500")
        mock_env = {"SCREENPY_TIMEOUT": "1337"}

        with mock.patch("pathlib.Path.open", mock_open):
            with mock.patch.dict(os.environ, mock_env):
                settings = ScreenPySettings()

        assert settings.TIMEOUT == 1337

    def test_init_overwrites_env(self):
        mock_env = {"SCREENPY_TIMEOUT": "1337"}

        with mock.patch.dict(os.environ, mock_env):
            settings = ScreenPySettings(TIMEOUT=9001)

        assert settings.TIMEOUT == 9001

    def test_cannot_be_changed_at_runtime(self):
        with pytest.raises(TypeError):
            screenpy_settings.TIMEOUT = 4


class TestStdOutAdapterSettings:
    def test_pyproject_overwrites_initial(self):
        mock_open = mock.mock_open(
            read_data=b"[tool.screenpy.stdoutadapter]\nINDENT_SIZE = 500"
        )

        with mock.patch("pathlib.Path.open", mock_open):
            settings = StdOutAdapterSettings()

        assert settings.INDENT_SIZE == 500

    def test_env_overwrites_pyproject(self):
        mock_open = mock.mock_open(
            read_data=b"[tool.screenpy.stdoutadapter]\nINDENT_SIZE = 500"
        )
        mock_env = {"SCREENPY_STDOUTADAPTER_INDENT_SIZE": "1337"}

        with mock.patch("pathlib.Path.open", mock_open):
            with mock.patch.dict(os.environ, mock_env):
                settings = StdOutAdapterSettings()

        assert settings.INDENT_SIZE == 1337

    def test_init_overwrites_env(self):
        mock_env = {"SCREENPY_STDOUTADAPTER_INDENT_SIZE": "1337"}

        with mock.patch.dict(os.environ, mock_env):
            settings = StdOutAdapterSettings(INDENT_SIZE=9001)

        assert settings.INDENT_SIZE == 9001

    def test_cannot_be_changed_at_runtime(self):
        with pytest.raises(TypeError):
            stdout_adapter_settings.INDENT_CHAR = "?"


class TestCombo:
    def test_can_set_multiple_tools(self):
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
