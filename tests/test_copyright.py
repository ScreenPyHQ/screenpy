from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from screenpy import __doc__, __version__


class TestCopyrightYear:
    @pytest.fixture(autouse=True)
    def _setup(self) -> None:
        self.current_year = datetime.now().year

    def test_version(self) -> None:
        assert f"{self.current_year}" in __version__.__copyright__

    def test_license(self) -> None:
        license_path = Path(__file__).parent / ".." / "LICENSE"
        with open(license_path) as fp:
            license_text = fp.read()

        assert f"{self.current_year}" in license_text

    def test_init(self) -> None:
        assert f"{self.current_year}" in __doc__
