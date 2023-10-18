"""This is a duplicate of test_pacing but uses future annotations"""
from __future__ import annotations

import logging
from typing import Optional

from screenpy import Actor, IsEqualTo, See, beat


class CornerCase:
    @beat("{} examines CornerCase")
    def answered_by(self, _: Actor) -> object:
        self.do_not_log_me_man()
        self.does_return_something()
        self.no_annotations_rt_none(False)
        self.no_annotations_rt_int(True)
        return None

    @beat("Blah!")
    def do_not_log_me_man(self) -> None:
        return None

    @beat("Foobar...")
    def does_return_something(self, toggle: bool = False) -> Optional[int]:
        if toggle:
            return 1
        return None

    # purposfully not annotated
    @beat("Baz?")
    def no_annotations_rt_none(self, toggle=False):
        if toggle:
            return 1
        return None

    # purposfully not annotated
    @beat("Bazinga!!")
    def no_annotations_rt_int(self, toggle=False):
        if toggle:
            return 1
        return None

    def describe(self) -> str:
        return "CornerCase"


class TestBeat:
    def test_beat_logging_none_corner(self, Tester, caplog):
        caplog.set_level(logging.INFO)
        See(CornerCase(), IsEqualTo(None)).perform_as(Tester)

        assert [r.msg for r in caplog.records] == [
            "Tester sees if cornerCase is equal to <None>.",
            "    Tester examines CornerCase",
            "        Blah!",
            "        Foobar...",
            "            => <None>",
            "        Baz?",
            "        Bazinga!!",
            "            => <1>",
            "        => <None>",
            "    ... hoping it's equal to <None>.",
            "        => <None>",
        ]
