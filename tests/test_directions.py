import pytest

from screenpy import Director
from screenpy.directions import noted_under
from screenpy.exceptions import UnableToDirect


def test_noted_under() -> None:
    expected_note = "note"
    key = "key"
    director = Director()
    director.notes(key, expected_note)

    actual_note = noted_under(key)

    assert actual_note == expected_note


def test_noted_under_no_note() -> None:
    """Raises UnableToDirect with no note, exception points to docs."""
    with pytest.raises(UnableToDirect) as exc:
        noted_under("does not exist")

    assert "screenpy-docs.readthedocs.io" in str(exc.value)
