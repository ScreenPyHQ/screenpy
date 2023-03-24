import os
from unittest import mock

from screenpy.settings import ScreenPySettings, StdOutAdapterSettings


class TestSettings:
    def test_pyproject_overwrites_init(self):
        mock_open = mock.mock_open(read_data=b"[tool.screenpy]\ntimeout = 500")

        with mock.patch("pathlib.Path.open", mock_open):
            settings = ScreenPySettings()

        assert settings.timeout == 500

    def test_env_overwrites_pyproject(self):
        mock_open = mock.mock_open(read_data=b"[tool.screenpy]\ntimeout = 500")
        mock_env = {"SCREENPY_TIMEOUT": "1337"}

        with mock.patch("pathlib.Path.open", mock_open):
            with mock.patch.dict(os.environ, mock_env):
                settings = ScreenPySettings()

        assert settings.timeout == 1337


class TestStdOutAdapterSettings:
    def test_pyproject_overwrites_init(self):
        mock_open = mock.mock_open(
            read_data=b"[tool.screenpy.stdoutadapter]\nindent_size = 500"
        )

        with mock.patch("pathlib.Path.open", mock_open):
            settings = StdOutAdapterSettings()

        assert settings.indent_size == 500

    def test_env_overwrites_pyproject(self):
        mock_open = mock.mock_open(
            read_data=b"[tool.screenpy.stdoutadapter]\nindent_size = 500"
        )
        mock_env = {"SCREENPY_STDOUTADAPTER_INDENT_SIZE": "1337"}

        with mock.patch("pathlib.Path.open", mock_open):
            with mock.patch.dict(os.environ, mock_env):
                settings = StdOutAdapterSettings()

        assert settings.indent_size == 1337
