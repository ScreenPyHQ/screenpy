from unittest import mock

import pytest

from screenpy.narration.narrator import NORMAL, Narrator, _chainify
from screenpy.protocols import Adapter

def _():
    """Dummy function for simple chaining tests."""
    pass


KW: dict = {"func": _, "line": ""}
KW_G = {**KW, "gravitas": NORMAL}


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
    def test_flat_narration(self, test_narrations, expected):
        actual = _chainify(test_narrations)

        assert actual == expected


class TestNarrator:
    def test_add_new_adapter(self):
        narrator = Narrator()
        test_adapter = mock.create_autospec(Adapter, instance=True)
        narrator.attach_adapter(test_adapter)
        assert test_adapter in narrator.adapters

    def test_off_air(self):
        MockAdapter = mock.create_autospec(Adapter, instance=True)
        narrator = Narrator(adapters=[MockAdapter])

        with narrator.off_the_air():
            narrator.announcing_the_act(_, "")
            narrator.setting_the_scene(_, "")
            narrator.stating_a_beat(_, "")
            narrator.whispering_an_aside("")

        assert narrator.backed_up_narrations == []
        MockAdapter.act.assert_not_called()
        MockAdapter.scene.assert_not_called()
        MockAdapter.beat.assert_not_called()
        MockAdapter.act.assert_not_called()

    def test_mic_cable_kinked(self):
        MockAdapter = mock.create_autospec(Adapter, instance=True)
        narrator = Narrator(adapters=[MockAdapter])

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
            MockAdapter.act.assert_not_called()
            MockAdapter.scene.assert_not_called()
            MockAdapter.beat.assert_not_called()
            MockAdapter.act.assert_not_called()

        # exiting the context flushes the backed-up narrations
        assert narrator.backed_up_narrations == []
        MockAdapter.act.assert_called_once()
        MockAdapter.scene.assert_called_once()
        MockAdapter.beat.assert_called_once()
        MockAdapter.act.assert_called_once()

    def test_deep_kink(self):
        MockAdapter = mock.create_autospec(Adapter, instance=True)
        narrator = Narrator(adapters=[MockAdapter])
        with narrator.mic_cable_kinked():
            with narrator.announcing_the_act(_, ""):
                with narrator.mic_cable_kinked():
                    with narrator.stating_a_beat(_, ""):
                        assert len(narrator.backed_up_narrations) == 2
                        assert narrator.backed_up_narrations[-1][0][0] == "beat"

    def test_clear_backup(self):
        MockAdapter = mock.create_autospec(Adapter, instance=True)
        narrator = Narrator(adapters=[MockAdapter])
        with narrator.mic_cable_kinked():
            narrator.announcing_the_act(_, "")
            narrator.setting_the_scene(_, "")
            narrator.stating_a_beat(_, "")
            narrator.whispering_an_aside("")

            narrator.clear_backup()

            assert narrator.backed_up_narrations == [[]]

        assert narrator.backed_up_narrations == []
        MockAdapter.act.assert_not_called()
        MockAdapter.scene.assert_not_called()
        MockAdapter.beat.assert_not_called()
        MockAdapter.act.assert_not_called()

    def test_clear_backup_deep_kink(self):
        MockAdapter = mock.create_autospec(Adapter, instance=True)
        narrator = Narrator(adapters=[MockAdapter])
        with narrator.mic_cable_kinked():
            with narrator.announcing_the_act(_, ""):
                with narrator.mic_cable_kinked():
                    with narrator.stating_a_beat(_, ""):
                        narrator.clear_backup()
                    assert len(narrator.backed_up_narrations) == 2
                    assert narrator.backed_up_narrations[0][0][0] == "act"
                    assert narrator.backed_up_narrations[1] == []

        MockAdapter.act.assert_called_once()

    def test__increase_exit_level(self):
        MockAdapter = mock.create_autospec(Adapter, instance=True)
        narrator = Narrator(adapters=[MockAdapter])

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

    def test_multi_kink(self):
        MockAdapter = mock.create_autospec(Adapter, instance=True)
        narrator = Narrator(adapters=[MockAdapter])

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

    def test_flush_backup(self):
        MockAdapter = mock.create_autospec(Adapter, instance=True)
        narrator = Narrator(adapters=[MockAdapter])
        with narrator.mic_cable_kinked():
            narrator.announcing_the_act(_, "")
            narrator.setting_the_scene(_, "")
            narrator.stating_a_beat(_, "")
            narrator.whispering_an_aside("")

            narrator.flush_backup()

            assert narrator.backed_up_narrations == [[]]
            MockAdapter.act.assert_called_once()
            MockAdapter.scene.assert_called_once()
            MockAdapter.beat.assert_called_once()
            MockAdapter.act.assert_called_once()

    def test__dummy_entangle(self):
        narrator = Narrator()

        with narrator._dummy_entangle(lambda: narrator.exit_level) as func:

            assert func() == 2
        assert narrator.exit_level == 1

    def test__entangle_chain(self):
        MockAdapter = mock.create_autospec(Adapter, instance=True)
        narrator = Narrator(adapters=[MockAdapter])
        chain = [("act", KW, [("scene", KW, [("beat", KW, [])])]), ("aside", KW, [])]

        narrator._entangle_chain(MockAdapter, chain)

        MockAdapter.act.assert_called_once()
        MockAdapter.scene.assert_called_once()
        MockAdapter.beat.assert_called_once()
        MockAdapter.act.assert_called_once()

    @pytest.mark.parametrize("channel", ["act", "scene", "beat", "aside"])
    def test__entangle_func(self, channel):
        MockAdapter = mock.create_autospec(Adapter, instance=True)
        narrator = Narrator(adapters=[MockAdapter])

        with narrator._entangle_func(channel, **KW):
            getattr(MockAdapter, channel).assert_called_once_with(**KW)

    def test_narrate_throws_for_uncallable_func(self):
        narrator = Narrator()

        with pytest.raises(TypeError):
            narrator.narrate("", func="")

    @pytest.mark.parametrize(
        "channel_func,channel,kwds",
        [
            ("announcing_the_act", "act", ["func", "line", "gravitas"]),
            ("setting_the_scene", "scene", ["func", "line", "gravitas"]),
            ("stating_a_beat", "beat", ["func", "line"]),
            ("whispering_an_aside", "aside", ["func", "line"]),
        ],
    )
    def test_channels(self, channel_func, channel, kwds):
        narrator = Narrator()
        narrator.narrate = mock.create_autospec(narrator.narrate)
        kwargs = KW_G if "gravitas" in kwds else KW
        if channel == "aside":
            del kwargs["func"]

        getattr(narrator, channel_func)(**kwargs)

        narrator.narrate.assert_called_once()
        assert narrator.narrate.call_args_list[0][0][0] == channel
        assert list(narrator.narrate.call_args_list[0][1].keys()) == kwds

    def test_attach(self):
        test_adapters = [mock.create_autospec(Adapter, instance=True) for _ in range(3)]
        narrator = Narrator(adapters=test_adapters)
        test_path = "lskywalker/documents/father.png"
        test_kwargs = {"no": "that's not true!", "that": "is impossible!"}

        narrator.attaches_a_file(test_path, **test_kwargs)

        for mocked_adapter in test_adapters:
            mocked_adapter.attach.assert_called_once_with(test_path, **test_kwargs)

    def test_off_the_air_goes_back_on_after_error(self):
        narrator = Narrator(adapters=[mock.create_autospec(Adapter, instance=True)])

        try:
            with narrator.off_the_air():
                with narrator.stating_a_beat(lambda: "Hello", "Clarise"):
                    raise ValueError()
        except ValueError:
            pass

        assert narrator.on_air

    def test_mic_cable_kinked_unkinks_cable_after_error(self):
        narrator = Narrator(adapters=[mock.create_autospec(Adapter, instance=True)])

        try:
            with narrator.mic_cable_kinked():
                with narrator.stating_a_beat(lambda: "Hello", "Anthony"):
                    raise ValueError()
        except ValueError:
            pass

        assert not narrator.cable_kinked

    def test_flush_backup_without_kink(self):
        MockAdapter = mock.create_autospec(Adapter, instance=True)
        narrator = Narrator(adapters=[MockAdapter])
        narrator.clear_backup = mock.create_autospec(narrator.clear_backup)
        narrator.flush_backup()
        narrator.clear_backup.assert_not_called()
