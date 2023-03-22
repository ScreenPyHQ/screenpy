import logging
from typing import Any, Generator

import pytest

from screenpy import (
    NORMAL,
    Narrator,
    StdOutAdapter,
    act,
    aside,
    beat,
    scene,
)

TEST_ACT = "Three"
TEST_SCENE = "The Scene Where He Uses It"
TEST_BEAT = "Don't make me use this!"
TEST_ASIDE = "You made me use it!!"
TEST_RETVAL = ">:("
INDENT = StdOutAdapter().manager.whitespace


@act(TEST_ACT, gravitas=NORMAL)
@scene(TEST_SCENE)
def prop():
    pass


class Prop:
    @beat(TEST_BEAT)
    def use(self) -> str:
        aside(TEST_ASIDE)
        return TEST_RETVAL


def _assert_stdout_correct(caplog) -> None:
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
        old_adapters = Narrator().adapters
        Narrator().adapters = [StdOutAdapter()]
        yield Narrator()
        Narrator().adapters = old_adapters

    def test_narrations(self, caplog) -> None:
        with caplog.at_level(logging.INFO):
            prop()
            Prop().use()

        _assert_stdout_correct(caplog)

    def test_flushed_narrations(self, caplog) -> None:
        with caplog.at_level(logging.INFO):
            with Narrator().mic_cable_kinked():
                prop()
                Prop().use()

        _assert_stdout_correct(caplog)
