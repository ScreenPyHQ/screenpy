import logging

from screenpy.narration.adapters.stdout_adapter import StdOutAdapter, StdOutManager


def prop():
    """The revolver in the foyer!"""
    pass


class TestStdOutManager:
    def test__outdent(self):
        manager = StdOutManager()
        manager.depth = []

        manager._outdent()
        manager._outdent()
        manager._outdent()

        assert len(manager.depth) == 0

    def test__indent(self):
        manager = StdOutManager()

        with manager._indent():
            assert len(manager.depth) == 1
        # context persists until manager._outdent is called
        assert len(manager.depth) == 1

    def test_step(self, caplog):
        manager = StdOutManager()
        test_message = "Wow. I’m Mr. Manager."

        with caplog.at_level(logging.INFO):
            with manager.log_context(test_message):
                assert len(caplog.records) == 1
                assert caplog.records[0].message == test_message


class TestStdOutAdapter:
    def test_act(self, caplog):
        adapter = StdOutAdapter()
        act_name = "test act"
        test_func = adapter.act(prop, act_name, None)

        with caplog.at_level(logging.INFO):
            next(test_func)()

        assert len(caplog.records) == 1
        assert caplog.records[0].message == f"ACT {act_name.upper()}"

    def test_scene(self, caplog):
        adapter = StdOutAdapter()
        scene_name = "test scene"
        test_func = adapter.scene(prop, scene_name, None)

        with caplog.at_level(logging.INFO):
            next(test_func)()

        assert len(caplog.records) == 1
        assert caplog.records[0].message == f"Scene: {scene_name.title()}"

    def test_beat(self, caplog):
        adapter = StdOutAdapter()
        beat_line = "test beat"
        test_func = adapter.beat(prop, beat_line)

        with caplog.at_level(logging.INFO):
            next(test_func)()

        assert len(caplog.records) == 1
        assert caplog.records[0].message == beat_line

    def test_indentation(self, caplog):
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

    def test_aside(self, caplog):
        adapter = StdOutAdapter()
        aside_line = "test aside"
        test_func = adapter.aside(prop, aside_line)

        with caplog.at_level(logging.INFO):
            next(test_func)()

        assert len(caplog.records) == 1
        assert caplog.records[0].message == aside_line

    def test_aside_in_a_beat(self, caplog):
        adapter = StdOutAdapter()

        with caplog.at_level(logging.INFO):
            for func1 in adapter.aside(prop, "beat"):
                for func2 in adapter.beat(func1, "aside"):
                    func2()

        assert len(caplog.records) == 2
        assert caplog.records[0].message == "beat"
        assert caplog.records[1].message == "    aside"

    def test_error(self, caplog):
        adapter = StdOutAdapter()
        expected_exception = ValueError("Snakes. Why is it always snakes?")

        with caplog.at_level(logging.INFO):
            adapter.error(expected_exception)

        assert len(caplog.records) == 1
        assert expected_exception.__class__.__name__ in caplog.records[0].message
        assert str(expected_exception) in caplog.records[0].message

    def test_attach(self, caplog):
        test_filepath = "freakazoid/documents/freak_in.png"
        adapter = StdOutAdapter()

        with caplog.at_level(logging.INFO):
            adapter.attach(test_filepath)

        assert len(caplog.records) == 1
        assert test_filepath in caplog.records[0].message
