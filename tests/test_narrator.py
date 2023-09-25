from typing import Callable, Dict, List, Tuple, Union
from unittest import mock

import pytest

from screenpy import NORMAL, Adapter, Narrator
from screenpy.narration.narrator import _chainify


def _() -> None:
    """Dummy function for simple chaining tests."""
    pass


T_KW = Dict[str, Union[Callable, str]]
T_Chain = List[Tuple[str, T_KW, List]]

KW: T_KW = {"func": _, "line": ""}
KW_G: T_KW = {**KW, "gravitas": NORMAL}


def get_mock_adapter():
    return mock.create_autospec(Adapter, instance=True)


class TestChainify:
    @pytest.mark.parametrize(
        "test_narrations,expected",
        [
            (
                [("ch", KW, 1), ("ch", KW, 1), ("ch", KW, 1)],
                [("ch", KW, []), ("ch", KW, []), ("ch", KW, [])],
            ),
            (
                [("ch", KW, 1), ("ch", KW, 2), ("ch", KW, 3)],
                [("ch", KW, [("ch", KW, [("ch", KW, [])])])],
            ),
            (
                [("ch", KW, 1), ("ch", KW, 2), ("ch", KW, 3), ("ch", KW, 1)],
                [("ch", KW, [("ch", KW, [("ch", KW, [])])]), ("ch", KW, [])],
            ),
        ],
    )
    def test_flat_narration(self, test_narrations, expected) -> None:
        actual = _chainify(test_narrations)

        assert actual == expected


class TestNarrator:
    def test_add_new_adapter(self) -> None:
        narrator = Narrator()
        test_adapter = get_mock_adapter()

        narrator.attach_adapter(test_adapter)

        assert test_adapter in narrator.adapters

    def test_off_air(self) -> None:
        mock_adapter = get_mock_adapter()
        narrator = Narrator(adapters=[mock_adapter])

        with narrator.off_the_air():
            narrator.announcing_the_act(_, "")
            narrator.setting_the_scene(_, "")
            narrator.stating_a_beat(_, "")
            narrator.whispering_an_aside("")

        assert narrator.backed_up_narrations == []
        mock_adapter.act.assert_not_called()
        mock_adapter.scene.assert_not_called()
        mock_adapter.beat.assert_not_called()
        mock_adapter.act.assert_not_called()

    def test_mic_cable_kinked(self) -> None:
        mock_adapter = get_mock_adapter()
        narrator = Narrator(adapters=[mock_adapter])

        with narrator.mic_cable_kinked():
            narrator.announcing_the_act(_, "")
            narrator.setting_the_scene(_, "")
            narrator.stating_a_beat(_, "")
            narrator.whispering_an_aside("")

            # assert these before leaving the context
            assert len(narrator.backed_up_narrations) == 1
            assert len(narrator.backed_up_narrations[0]) == 4
            assert narrator.backed_up_narrations[0][0][0] == "act"
            assert narrator.backed_up_narrations[0][1][0] == "scene"
            assert narrator.backed_up_narrations[0][2][0] == "beat"
            assert narrator.backed_up_narrations[0][3][0] == "aside"
            assert all(
                level == 1
                for level in map(lambda n: n[-1], narrator.backed_up_narrations[0])
            )
            mock_adapter.act.assert_not_called()
            mock_adapter.scene.assert_not_called()
            mock_adapter.beat.assert_not_called()
            mock_adapter.act.assert_not_called()

        # exiting the context flushes the backed-up narrations
        assert narrator.backed_up_narrations == []
        mock_adapter.act.assert_called_once()
        mock_adapter.scene.assert_called_once()
        mock_adapter.beat.assert_called_once()
        mock_adapter.act.assert_called_once()

    def test_deep_kink(self) -> None:
        mock_adapter = get_mock_adapter()
        narrator = Narrator(adapters=[mock_adapter])

        with narrator.mic_cable_kinked():
            with narrator.announcing_the_act(_, ""):
                with narrator.mic_cable_kinked():
                    with narrator.stating_a_beat(_, ""):
                        assert len(narrator.backed_up_narrations) == 2
                        assert narrator.backed_up_narrations[-1][0][0] == "beat"

    def test_clear_backup(self) -> None:
        mock_adapter = get_mock_adapter()
        narrator = Narrator(adapters=[mock_adapter])
        with narrator.mic_cable_kinked():
            narrator.announcing_the_act(_, "")
            narrator.setting_the_scene(_, "")
            narrator.stating_a_beat(_, "")
            narrator.whispering_an_aside("")

            narrator.clear_backup()

            assert narrator.backed_up_narrations == [[]]

        assert narrator.backed_up_narrations == []
        mock_adapter.act.assert_not_called()
        mock_adapter.scene.assert_not_called()
        mock_adapter.beat.assert_not_called()
        mock_adapter.act.assert_not_called()

    def test_clear_backup_deep_kink(self) -> None:
        mock_adapter = get_mock_adapter()
        narrator = Narrator(adapters=[mock_adapter])
        with narrator.mic_cable_kinked():
            with narrator.announcing_the_act(_, ""):
                with narrator.mic_cable_kinked():
                    with narrator.stating_a_beat(_, ""):
                        narrator.clear_backup()
                    assert len(narrator.backed_up_narrations) == 2
                    assert narrator.backed_up_narrations[0][0][0] == "act"
                    assert narrator.backed_up_narrations[1] == []

        mock_adapter.act.assert_called_once()

    def test__increase_exit_level(self) -> None:
        mock_adapter = get_mock_adapter()
        narrator = Narrator(adapters=[mock_adapter])

        with narrator.mic_cable_kinked():
            with narrator.announcing_the_act(_, "act"):
                with narrator.setting_the_scene(_, "scene"):
                    with narrator.stating_a_beat(_, "beat"):
                        with narrator.whispering_an_aside("aside"):
                            pass
                with narrator.whispering_an_aside("aside, too"):
                    pass

            assert narrator.backed_up_narrations[0][0][0] == "act"
            assert narrator.backed_up_narrations[0][0][-1] == 1
            assert narrator.backed_up_narrations[0][1][0] == "scene"
            assert narrator.backed_up_narrations[0][1][-1] == 2
            assert narrator.backed_up_narrations[0][2][0] == "beat"
            assert narrator.backed_up_narrations[0][2][-1] == 3
            assert narrator.backed_up_narrations[0][3][0] == "aside"
            assert narrator.backed_up_narrations[0][3][-1] == 4
            assert narrator.backed_up_narrations[0][4][0] == "aside"
            assert narrator.backed_up_narrations[0][4][-1] == 2

    def test_multi_kink(self) -> None:
        mock_adapter = get_mock_adapter()
        narrator = Narrator(adapters=[mock_adapter])

        assert len(narrator.backed_up_narrations) == 0
        with narrator.mic_cable_kinked():
            assert len(narrator.backed_up_narrations) == 1
            assert narrator.backed_up_narrations[0] == []
            with narrator.announcing_the_act(_, "act"):
                assert narrator.backed_up_narrations[0][0][0] == "act"
                with narrator.mic_cable_kinked():
                    assert len(narrator.backed_up_narrations) == 2
                    assert narrator.backed_up_narrations[1] == []
                    with narrator.setting_the_scene(_, "scene"):
                        assert narrator.backed_up_narrations[1][0][0] == "scene"
                        with narrator.mic_cable_kinked():
                            assert len(narrator.backed_up_narrations) == 3
                            assert narrator.backed_up_narrations[2] == []
                            with narrator.stating_a_beat(_, "beat"):
                                assert narrator.backed_up_narrations[2][0][0] == "beat"
                                with narrator.mic_cable_kinked():
                                    assert len(narrator.backed_up_narrations) == 4
                                    assert narrator.backed_up_narrations[3] == []
                                assert len(narrator.backed_up_narrations) == 3
                        assert len(narrator.backed_up_narrations) == 2
                assert len(narrator.backed_up_narrations) == 1
        assert len(narrator.backed_up_narrations) == 0

    def test_flush_backup(self) -> None:
        mock_adapter = get_mock_adapter()
        narrator = Narrator(adapters=[mock_adapter])
        with narrator.mic_cable_kinked():
            narrator.announcing_the_act(_, "")
            narrator.setting_the_scene(_, "")
            narrator.stating_a_beat(_, "")
            narrator.whispering_an_aside("")

            narrator.flush_backup()

            assert narrator.backed_up_narrations == [[]]
            mock_adapter.act.assert_called_once()
            mock_adapter.scene.assert_called_once()
            mock_adapter.beat.assert_called_once()
            mock_adapter.act.assert_called_once()

    def test__dummy_entangle(self) -> None:
        narrator = Narrator()

        with narrator._dummy_entangle(lambda: narrator.exit_level) as func:
            assert func() == 2
        assert narrator.exit_level == 1

    def test__entangle_chain(self) -> None:
        mock_adapter = get_mock_adapter()
        narrator = Narrator(adapters=[mock_adapter])
        chain: T_Chain = [
            ("act", KW, [("scene", KW, [("beat", KW, [])])]),
            ("aside", KW, []),
        ]

        narrator._entangle_chain(mock_adapter, chain)

        mock_adapter.act.assert_called_once()
        mock_adapter.scene.assert_called_once()
        mock_adapter.beat.assert_called_once()
        mock_adapter.act.assert_called_once()

    @pytest.mark.parametrize("channel", ["act", "scene", "beat", "aside"])
    def test__entangle_func(self, channel) -> None:
        mock_adapter = get_mock_adapter()
        narrator = Narrator(adapters=[mock_adapter])

        with narrator._entangle_func(channel, None, **KW):
            getattr(mock_adapter, channel).assert_called_once_with(**KW)

    def test_narrate_throws_for_uncallable_func(self) -> None:
        narrator = Narrator()

        with pytest.raises(TypeError):
            narrator.narrate("", func="")

    @pytest.mark.parametrize(
        "channel_func,channel",
        [
            ("announcing_the_act", "act"),
            ("setting_the_scene", "scene"),
            ("stating_a_beat", "beat"),
            ("whispering_an_aside", "aside"),
        ],
    )
    def test_channels(self, channel_func, channel) -> None:
        narrator = Narrator()
        kwargs = dict(KW_G)
        expected_kwargs = ["func", "line", "gravitas"]
        if channel == "aside":
            del kwargs["func"]

        with mock.patch.object(narrator, "narrate", autospec=True) as narrate:
            getattr(narrator, channel_func)(**kwargs)

            narrate.assert_called_once()
            assert narrate.call_args_list[0][0][0] == channel
            assert list(narrate.call_args_list[0][1].keys()) == expected_kwargs

    def test_attach(self) -> None:
        test_adapters = [get_mock_adapter() for _ in range(3)]
        narrator = Narrator(adapters=test_adapters)
        test_path = "lskywalker/documents/father.png"
        test_kwargs = {"no": "that's not true!", "that": "is impossible!"}

        narrator.attaches_a_file(test_path, **test_kwargs)

        for mocked_adapter in test_adapters:
            mocked_adapter.attach.assert_called_once_with(test_path, **test_kwargs)

    def test_off_the_air_goes_back_on_after_error(self) -> None:
        narrator = Narrator(adapters=[get_mock_adapter()])

        try:
            with narrator.off_the_air():
                with narrator.stating_a_beat(lambda: "Hello", "Clarise"):
                    raise ValueError()
        except ValueError:
            pass

        assert narrator.on_air

    def test_mic_cable_kinked_unkinks_cable_after_error(self) -> None:
        narrator = Narrator(adapters=[get_mock_adapter()])

        try:
            with narrator.mic_cable_kinked():
                with narrator.stating_a_beat(lambda: "Hello", "Anthony"):
                    raise ValueError()
        except ValueError:
            pass

        assert not narrator.cable_kinked

    def test_flush_backup_without_kink(self) -> None:
        mock_adapter = get_mock_adapter()
        narrator = Narrator(adapters=[mock_adapter])

        with mock.patch.object(narrator, "clear_backup", autospec=True) as clear_backup:
            narrator.flush_backup()

            clear_backup.assert_not_called()
