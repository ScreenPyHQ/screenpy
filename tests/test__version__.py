from __future__ import annotations

from datetime import datetime
from pathlib import Path

from screenpy import __version__


def test_metadata() -> None:
    assert __version__.__title__ == "screenpy"
    assert __version__.__license__ == "MIT"
    assert __version__.__author__ == "Perry Goy"


def test_copyright_year() -> None:
    current = datetime.now().year

    assert f"{current}" in __version__.__copyright__


def test_copyright_year_in_license() -> None:
    current = datetime.now().year
    license_path = Path(__file__) / ".." / "LICENSE"
    with open(license_path) as fp:
        license_text = fp.read()

    assert f"{current}" in license_text
