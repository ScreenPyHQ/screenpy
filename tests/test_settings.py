import os
from unittest import mock

from screenpy.settings import ScreenPySettings
from screenpy.narration.adapters.settings import StdOutAdapterSettings


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
