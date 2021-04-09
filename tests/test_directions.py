from screenpy import Director
from screenpy.directions import noted_under


def test_noted_under():
    expected_note = "note"
    key = "key"
    director = Director()
    director.notes(key, expected_note)

    actual_note = noted_under(key)

    assert actual_note == expected_note
