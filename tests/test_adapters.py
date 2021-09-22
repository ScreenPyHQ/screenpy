import logging
from screenpy.exceptions import UnableToNarrate
from unittest import mock

import pytest

from screenpy.narration.adapters.allure_adapter import AllureAdapter
from screenpy.narration.adapters.stdout_adapter import StdOutManager, StdOutAdapter


def prop():
    """The revolver in the foyer!"""
    pass


@mock.patch("screenpy.narration.adapters.allure_adapter.allure")
class TestAllureAdapter:
    @pytest.mark.parametrize(
        "narrator_level,allure_level", AllureAdapter.GRAVITAS.items()
    )
    def test_act(self, mocked_allure, narrator_level, allure_level):
        adapter = AllureAdapter()
        act_name = "test act"
        test_func = adapter.act(prop, act_name, narrator_level)

        next(test_func)()

        mocked_allure.epic.assert_called_once_with(act_name)
        mocked_allure.severity.assert_called_once_with(allure_level)

    @pytest.mark.parametrize(
        "narrator_level,allure_level", AllureAdapter.GRAVITAS.items()
    )
    def test_scene(self, mocked_allure, narrator_level, allure_level):
        adapter = AllureAdapter()
        scene_name = "test scene"
        test_func = adapter.scene(prop, scene_name, narrator_level)

        next(test_func)()

        mocked_allure.feature.assert_called_once_with(scene_name)
        mocked_allure.severity.assert_called_once_with(allure_level)

    def test_beat(self, mocked_allure):
        adapter = AllureAdapter()
        beat_message = "test beat"
        test_func = adapter.beat(prop, beat_message)

        next(test_func)()

        mocked_allure.step.assert_called_once_with(beat_message)

    def test_embedded_beat_allure_message(self, mocked_allure):
        """Context deepens with the embedded beats."""
        adapter = AllureAdapter()

        # yeah, this is weird. The beat method returns a generator, and we
        # need to keep it open. This is the most straightforward way!
        for func1 in adapter.beat(prop, "1"):
            for func2 in adapter.beat(func1, "2"):
                for func3 in adapter.beat(func2, "3"):
                    func3()

        calls = mocked_allure.step.mock_calls
        assert len(calls) == 9
        assert calls[0][1][0] == "1"
        assert calls[1][0] == "().__enter__"
        assert calls[2][1][0] == "2"
        assert calls[3][0] == "().__enter__"
        assert calls[4][1][0] == "3"
        assert calls[5][0] == "().__enter__"
        assert calls[6][0] == "().__exit__"
        assert calls[7][0] == "().__exit__"
        assert calls[8][0] == "().__exit__"

    def test_aside(self, mocked_allure):
        adapter = AllureAdapter()
        aside_message = "test aside"
        test_func = adapter.aside(prop, aside_message)

        next(test_func)()

        mocked_allure.step.assert_called_once_with(aside_message)

    def test_attach(self, mocked_allure):
        adapter = AllureAdapter()
        test_path = "ddouglas/documents/freak_out.png"
        test_name = "Dexter Douglas"
        test_attachment_type = ("nerd", "computer ace")
        test_extension = "cyberspace"

        adapter.attach(
            test_path,
            name=test_name,
            attachment_type=test_attachment_type,
            extension=test_extension,
        )

        mocked_allure.attach.assert_called_once_with(
            test_path, test_name, test_attachment_type, test_extension
        )

    def test_attach_raises_if_no_attachment_type(self, mocked_allure):
        adapter = AllureAdapter()

        with pytest.raises(UnableToNarrate):
            adapter.attach("foo")


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

    def test___str__(self):
        manager = StdOutManager()
        manager.enabled = True
        manager.depth = [1, 1, 1]
        manager.whitespace = "???"

        assert str(manager) == "?????????"


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

    def test_attach(self, caplog):
        test_filepath = "freakazoid/documents/freak_in.png"
        adapter = StdOutAdapter()

        with caplog.at_level(logging.INFO):
            adapter.attach(test_filepath)

        assert len(caplog.records) == 1
        assert test_filepath in caplog.records[0].message
