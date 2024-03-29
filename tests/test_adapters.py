import logging

import pytest

from screenpy import StdOutAdapter, StdOutManager
from screenpy.narration import gravitas
from screenpy.protocols import Adapter


def prop() -> None:
    """The revolver in the foyer!"""


class TestStdOutManager:
    def test_can_be_instantiated(self) -> None:
        m = StdOutManager()

        assert isinstance(m, StdOutManager)

    def test__outdent(self) -> None:
        manager = StdOutManager()
        manager.depth = []

        manager._outdent()
        manager._outdent()
        manager._outdent()

        assert len(manager.depth) == 0

    def test__indent(self) -> None:
        manager = StdOutManager()

        with manager._indent():
            assert len(manager.depth) == 1

        # context persists until manager._outdent is called
        assert len(manager.depth) == 1

    def test_step(self, caplog: pytest.LogCaptureFixture) -> None:
        manager = StdOutManager()
        test_message = "Wow. I'm Mr. Manager."

        with caplog.at_level(logging.INFO), manager.log_context(test_message):
            assert len(caplog.records) == 1
            assert caplog.records[0].message == test_message


class TestStdOutAdapter:
    def test_instantiate(self) -> None:
        a = StdOutAdapter()

        assert isinstance(a, StdOutAdapter)

    def test_implements_protocol(self) -> None:
        a = StdOutAdapter()

        assert isinstance(a, Adapter)

    def test_act(self, caplog: pytest.LogCaptureFixture) -> None:
        adapter = StdOutAdapter()
        act_name = "test act"
        test_func = adapter.act(prop, act_name)

        with caplog.at_level(logging.INFO):
            next(test_func)()

        assert len(caplog.records) == 1
        assert caplog.records[0].message == f"ACT {act_name.upper()}"

    def test_scene(self, caplog: pytest.LogCaptureFixture) -> None:
        adapter = StdOutAdapter()
        scene_name = "test scene"
        test_func = adapter.scene(prop, scene_name)

        with caplog.at_level(logging.INFO):
            next(test_func)()

        assert len(caplog.records) == 1
        assert caplog.records[0].message == f"Scene: {scene_name.title()}"

    def test_beat(self, caplog: pytest.LogCaptureFixture) -> None:
        adapter = StdOutAdapter()
        beat_line = "test beat"
        test_func = adapter.beat(prop, beat_line)

        with caplog.at_level(logging.INFO):
            next(test_func)()

        assert len(caplog.records) == 1
        assert caplog.records[0].message == beat_line

    def test_indentation(self, caplog: pytest.LogCaptureFixture) -> None:
        adapter = StdOutAdapter()

        with caplog.at_level(logging.INFO):
            for func1 in adapter.beat(prop, "1"):
                for func2 in adapter.beat(func1, "2"):
                    for func3 in adapter.beat(func2, "3"):
                        func3()

        assert len(caplog.records) == 3
        assert caplog.records[0].message == "1"
        assert caplog.records[1].message == "    2"
        assert caplog.records[2].message == "        3"

    def test_aside(self, caplog: pytest.LogCaptureFixture) -> None:
        adapter = StdOutAdapter()
        aside_line = "test aside"
        test_func = adapter.aside(prop, aside_line)

        with caplog.at_level(logging.INFO):
            next(test_func)()

        assert len(caplog.records) == 1
        assert caplog.records[0].message == aside_line

    def test_aside_in_a_beat(self, caplog: pytest.LogCaptureFixture) -> None:
        adapter = StdOutAdapter()

        with caplog.at_level(logging.INFO):
            for func1 in adapter.aside(prop, "beat"):
                for func2 in adapter.beat(func1, "aside"):
                    func2()

        assert len(caplog.records) == 2
        assert caplog.records[0].message == "beat"
        assert caplog.records[1].message == "    aside"

    def test_error(self, caplog: pytest.LogCaptureFixture) -> None:
        adapter = StdOutAdapter()
        expected_exception = ValueError("Snakes. Why is it always snakes?")

        with caplog.at_level(logging.INFO):
            adapter.error(expected_exception)

        assert len(caplog.records) == 1
        assert expected_exception.__class__.__name__ in caplog.records[0].message
        assert str(expected_exception) in caplog.records[0].message

    def test_attach(self, caplog: pytest.LogCaptureFixture) -> None:
        test_filepath = "freakazoid/documents/freak_in.png"
        adapter = StdOutAdapter()

        with caplog.at_level(logging.INFO):
            adapter.attach(test_filepath)

        assert len(caplog.records) == 1
        assert test_filepath in caplog.records[0].message

    @pytest.mark.parametrize(
        ("gravity", "level"),
        [
            (gravitas.AIRY, logging.DEBUG),
            (gravitas.LIGHT, logging.INFO),
            (gravitas.NORMAL, logging.WARNING),
            (gravitas.HEAVY, logging.CRITICAL),
            (gravitas.EXTREME, logging.ERROR),
        ],
    )
    def test_gravitas(
        self, gravity: str, level: int, caplog: pytest.LogCaptureFixture
    ) -> None:
        adapter = StdOutAdapter()
        line = "testing!"
        act = adapter.act(prop, line, gravity)
        scene = adapter.scene(prop, line, gravity)
        beat = adapter.beat(prop, line, gravity)
        aside = adapter.aside(prop, line, gravity)

        with caplog.at_level(level):
            for test_func in [act, scene, beat, aside]:
                next(test_func)()

        logs = [record.message for record in caplog.records]
        assert len(logs) == 4
        assert f"ACT {line.upper()}" in logs
        assert f"Scene: {line.capitalize()}" in logs
        assert line in logs
        assert f"    {line}" in logs
