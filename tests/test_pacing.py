from screenpy.pacing import act, aside, beat, scene


def prop():
    """The candlestick in the hall!"""


class Prop:
    """The wrench in the study!"""

    def __init__(self, weapon: str, room: str, perpetrator: str) -> None:
        self.weapon = weapon
        self.room = room
        self.perpetrator = perpetrator

    @beat("The {weapon} in the {room}!")
    def use(self):
        pass


class TestAct:
    def test_calls_narrators_method(self, mocked_narrator):
        test_act = "Test Act"
        actprop = act(test_act)(prop)

        actprop()

        mocked_narrator.announcing_the_act.assert_called_once()
        announced_act = mocked_narrator.announcing_the_act.call_args_list[0][0][1]
        assert test_act == announced_act


class TestScene:
    def test_calls_narrators_method(self, mocked_narrator):
        test_scene = "Test Scene"
        sceneprop = scene(test_scene)(prop)

        sceneprop()

        mocked_narrator.setting_the_scene.assert_called_once()
        set_scene = mocked_narrator.setting_the_scene.call_args_list[0][0][1]
        assert test_scene == set_scene


class TestBeat:
    def test_interpolations(self, mocked_narrator):
        """(This also tests that the narrator's method was called.)"""
        test_weapon = "rope"
        test_room = "ballroom"
        prop = Prop(test_weapon, test_room, "")

        prop.use()

        mocked_narrator.stating_a_beat.assert_called_once()
        completed_line = mocked_narrator.stating_a_beat.call_args_list[0][0][1]
        assert completed_line == f"The {test_weapon} in the {test_room}!"


class TestAside:
    def test_calls_narrators_method(self, mocked_narrator):
        test_whisper = "<whisper whisper>"

        aside(test_whisper)

        mocked_narrator.whispering_an_aside.assert_called_once()
        completed_line = mocked_narrator.whispering_an_aside.call_args_list[0][0][0]
        assert completed_line == test_whisper
