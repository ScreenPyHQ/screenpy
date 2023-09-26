from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Generator

import pytest

from screenpy import (
    NORMAL,
    Narrator,
    StdOutAdapter,
    act,
    aside,
    beat,
    scene,
    the_narrator,
)
from screenpy.narration.stdout_adapter import settings

if TYPE_CHECKING:
    from _pytest.logging import LogCaptureFixture

TEST_ACT = "Three"
TEST_SCENE = "The Scene Where He Uses It"
TEST_BEAT = "Don't make me use this!"
TEST_ASIDE = "You made me use it!!"
TEST_RETVAL = ">:("
INDENT = settings.INDENT_CHAR * settings.INDENT_SIZE


@act(TEST_ACT, gravitas=NORMAL)
@scene(TEST_SCENE)
def prop() -> None:
    pass


class Prop:
    @beat(TEST_BEAT)
    def use(self) -> str:
        aside(TEST_ASIDE)
        return TEST_RETVAL


def _assert_stdout_correct(caplog: LogCaptureFixture) -> None:
    """Assert the correctness of logged messages to stdout."""
    assert len(caplog.messages) == 5
    assert caplog.messages[0] == f"ACT {TEST_ACT.upper()}"
    assert caplog.messages[1] == f"Scene: {TEST_SCENE.title()}"
    assert caplog.messages[2] == TEST_BEAT
    assert caplog.messages[3] == f"{INDENT}{TEST_ASIDE}"
    assert caplog.messages[4] == f"{INDENT}=> {TEST_RETVAL}"


class TestNarrateToStdOut:
    @pytest.fixture(autouse=True)
    def narrator_has_stdout(self) -> Generator[Narrator, Any, None]:
        old_adapters = the_narrator.adapters
        the_narrator.adapters = [StdOutAdapter()]
        yield the_narrator
        the_narrator.adapters = old_adapters

    def test_narrations(self, caplog: LogCaptureFixture) -> None:
        with caplog.at_level(logging.INFO):
            prop()
            Prop().use()

        _assert_stdout_correct(caplog)

    def test_flushed_narrations(self, caplog: LogCaptureFixture) -> None:
        with caplog.at_level(logging.INFO), the_narrator.mic_cable_kinked():
            prop()
            Prop().use()

        _assert_stdout_correct(caplog)
