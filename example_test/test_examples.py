"""Example tests demonstrating core ScreenPy functionality."""

from screenpy import AnActor, then, when
from screenpy.actions import Log, MakeNote, See, SeeAllOf
from screenpy.directions import noted_under
from screenpy.resolutions import (
    ContainsTheItem,
    ContainsTheText,
    IsEqualTo,
    IsLessThan,
    Matches,
)


class TestLogging:
    """Tests for the Log action and a simple assertion."""

    def test_log_a_message(self, Perry: AnActor) -> None:
        """An Actor can log a value and assert True is True."""
        when(Perry).attempts_to(Log("This is a test!"))

        then(Perry).should(See(True, IsEqualTo(True)))


class TestMakeNote:
    """Tests for the MakeNote action and noted_under direction."""

    def test_make_note_and_recall(self, Perry: AnActor) -> None:
        """An Actor can note a value and assert against it later."""
        when(Perry).attempts_to(
            MakeNote.of("this is only a test").as_("memo"),
        )

        then(Perry).should(
            See(noted_under("memo"), ContainsTheText("test")),
        )


class TestSeeAllOf:
    """Tests for the SeeAllOf action with multiple assertions."""

    def test_see_all_of_multiple_checks(self, Perry: AnActor) -> None:
        """An Actor can verify several conditions at once."""
        then(Perry).should(
            SeeAllOf.the(
                (1, IsLessThan(2)),
                ([1, 2, 3], ContainsTheItem(3)),
                ("blahdy blah", Matches(r".*?y b.*?")),
            ),
        )
