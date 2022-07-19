import os
import sys
from unittest import mock

import pytest

from screenpy.actions import (
    AttachTheFile,
    Debug,
    Eventually,
    MakeNote,
    Pause,
    See,
    SeeAllOf,
    SeeAnyOf,
)
from screenpy.directions import noted_under
from screenpy.director import Director
from screenpy.exceptions import DeliveryError, UnableToAct, UnableToDirect
from screenpy.protocols import (
    Describable,
    Performable,
)
from screenpy.resolutions import IsEqualTo
from screenpy.resolutions import IsEqualTo, BaseResolution
from tests.conftest import mock_settings
from tests.unittest_protocols import Question, Action


class TestAttachTheFile:
    def test_can_be_instantiated(self):
        atf = AttachTheFile("")

        assert isinstance(atf, AttachTheFile)

    def test_implements_protocol(self):
        atf = AttachTheFile("")
        assert isinstance(atf, Performable)
        assert isinstance(atf, Describable)

    def test_divines_filename(self):
        filename = "thisisonlyatest.png"
        filepath = os.sep.join(["this", "is", "a", "test", filename])
        atf_without_path = AttachTheFile(filename)
        atf_with_path = AttachTheFile(filepath)

        assert atf_without_path.filename == filename
        assert atf_with_path.filename == filename

    @mock.patch("screenpy.actions.attach_the_file.the_narrator")
    def test_perform_attach_the_file_sends_kwargs(self, mocked_narrator, Tester):
        test_path = "souiiie.png"
        test_kwargs = {"color": "Red", "weather": "Tornado"}

        AttachTheFile(test_path, **test_kwargs).perform_as(Tester)

        mocked_narrator.attaches_a_file.assert_called_once_with(
            test_path, **test_kwargs
        )

    def test_describe(self):
        file = "somefile.txt"
        assert AttachTheFile(file).describe() == f"Attach a file named {file}."


class TestDebug:
    def test_can_be_instantiated(self):
        d = Debug()

        assert isinstance(d, Debug)

    def test_implements_protocol(self):
        d = Debug()
        assert isinstance(d, Performable)
        assert isinstance(d, Describable)

    @mock.patch("screenpy.actions.debug.breakpoint")
    def test_calls_breakpoint(self, mocked_breakpoint, Tester):
        Debug().perform_as(Tester)

        mocked_breakpoint.assert_called_once()

    @mock.patch("screenpy.actions.debug.breakpoint")
    @mock.patch("screenpy.actions.debug.pdb")
    def test_falls_back_to_pdb(self, mocked_pdb, mocked_breakpoint, Tester):
        mocked_breakpoint.side_effect = NameError("name 'breakpoint' is not defined")

        Debug().perform_as(Tester)

        mocked_pdb.set_trace.assert_called_once()

    def test_describe(self):
        assert Debug().describe() == "Assume direct control."


class TestEventually:
    def get_mock_action(self, **kwargs):
        mock_action = mock.Mock(spec_set=Action)
        mock_action.perform_as = mock.Mock(**kwargs)
        mock_action.describe.return_value = "An African or a European swallow?"
        return mock_action

    def test_can_be_instantiated(self):
        e1 = Eventually(None)
        e2 = Eventually(None).trying_for_no_longer_than(0).seconds()
        e3 = Eventually(None).trying_for(0).milliseconds()
        e4 = Eventually(None).for_(0).seconds()
        e5 = Eventually(None).waiting_for(0).seconds()
        e6 = Eventually(None).polling(0).seconds()
        e7 = Eventually(None).polling_every(0).milliseconds()
        e8 = Eventually(None).trying_every(0).seconds()

        assert isinstance(e1, Eventually)
        assert isinstance(e2, Eventually)
        assert isinstance(e3, Eventually)
        assert isinstance(e4, Eventually)
        assert isinstance(e5, Eventually)
        assert isinstance(e6, Eventually)
        assert isinstance(e7, Eventually)
        assert isinstance(e8, Eventually)

    def test_implements_protocol(self):
        t = Eventually(None)
        assert isinstance(t, Performable)
        assert isinstance(t, Describable)

    def test_uses_timeframe_builder(self):
        ev = Eventually(None).trying_for(1)

        assert isinstance(ev, Eventually._TimeframeBuilder)

    def test_can_adjust_timeout(self):
        ev = Eventually(None).trying_for(12)

        # is still _TimeframeBuilder, so get the stored Eventually
        assert ev.eventually.timeout == 12

    def test_can_adjust_timeout_seconds(self):
        ev = Eventually(None).trying_for(15).seconds()

        assert ev.timeout == 15

    def test_can_adjust_timeout_milliseconds(self):
        ev = Eventually(None).trying_for(1200).milliseconds()

        assert ev.timeout == 1.2

    def test_can_adjust_polling_frequency(self):
        ev = Eventually(None).polling(1).second()

        assert ev.poll == 1

    @mock_settings(TIMEOUT=100)
    def test_adjusting_settings_timeout(self):
        ev = Eventually(None)

        assert ev.timeout == 100

    def test__timeframebuilder_is_performable(self, Tester):
        MockAction = self.get_mock_action()

        # test passes if no exception is raised
        Eventually(MockAction).for_(1).perform_as(Tester)

    def test_valueerror_when_poll_is_larger_than_timeout(self, Tester):
        MockAction = self.get_mock_action()
        ev = (
            Eventually(MockAction)
            .polling_every(200)
            .milliseconds()
            .for_(100)
            .milliseconds()
        )

        with pytest.raises(ValueError) as actual_exception:
            ev.perform_as(Tester)

        assert "poll must be less than or equal to timeout" in str(actual_exception)

    @mock.patch("screenpy.actions.eventually.time")
    def test_perform_eventually_times_out(self, mocked_time, Tester):
        num_calls = 5
        mocked_time.time = mock.Mock(side_effect=[1] * num_calls + [100])
        MockAction = self.get_mock_action(
            side_effect=ValueError("'Tis but a flesh wound!")
        )

        with pytest.raises(DeliveryError):
            Eventually(MockAction).perform_as(Tester)

        assert mocked_time.time.call_count == num_calls + 1

    @mock.patch("screenpy.actions.eventually.time")
    def test_timeout_mentions_num_executions(self, mocked_time, Tester):
        num_calls = 5
        mocked_time.time = mock.Mock(side_effect=[1] * num_calls + [100])
        MockAction = self.get_mock_action(
            side_effect=ValueError("He's pining for the fjords!")
        )

        with pytest.raises(DeliveryError) as e:
            Eventually(MockAction).perform_as(Tester)

        assert f"{num_calls} times" in str(e)

    @mock.patch("screenpy.actions.eventually.time")
    def test_catches_exceptions(self, mocked_time, Tester):
        mocked_time.time = mock.Mock(side_effect=[1, 1, 100])
        msg = "I got better."
        MockAction = self.get_mock_action(side_effect=ValueError(msg))

        with pytest.raises(DeliveryError) as actual_exception:
            Eventually(MockAction).perform_as(Tester)

        assert msg in str(actual_exception)

    @mock.patch("screenpy.actions.eventually.time")
    def test_mentions_all_errors(self, mocked_time, Tester):
        mocked_time.time = mock.Mock(side_effect=[1, 1, 100])
        exc1 = ValueError("These tracts of land aren't that huge!")
        exc2 = TypeError("This witch does not weigh as much as a duck!")
        MockAction = self.get_mock_action(side_effect=[exc1, exc2])

        with pytest.raises(DeliveryError) as actual_exception:
            Eventually(MockAction).perform_as(Tester)

        assert exc1.__class__.__name__ in str(actual_exception.value)
        assert str(exc1) in str(actual_exception.value)
        assert exc2.__class__.__name__ in str(actual_exception.value)
        assert str(exc2) in str(actual_exception.value)

    def test_describe(self):
        MockAction = self.get_mock_action()
        assert Eventually(MockAction).describe() == f"Eventually an African or a European swallow."


class TestMakeNote:
    def test_can_be_instantiated(self):
        mn1 = MakeNote(None)
        mn2 = MakeNote.of(None)
        mn3 = MakeNote.of_the(None).as_("")

        assert isinstance(mn1, MakeNote)
        assert isinstance(mn2, MakeNote)
        assert isinstance(mn3, MakeNote)

    def test_implements_protocol(self):
        m = MakeNote("")
        assert isinstance(m, Performable)
        assert isinstance(m, Describable)

    def test_key_value_set(self):
        test_question = "Do I feel lucky?"
        test_key = "Well, do you, punk?"

        mn = MakeNote.of_the(test_question).as_(test_key)

        assert mn.question == test_question
        assert mn.key == test_key

    def test_answers_question(self, Tester):
        MockQuestion = mock.Mock(spec_set=Question)

        MakeNote.of_the(MockQuestion).as_("test").perform_as(Tester)

        assert MockQuestion.answered_by.called_once_with(Tester)

    def test_raises_without_key(self, Tester):
        with pytest.raises(UnableToAct):
            MakeNote.of_the(None).perform_as(Tester)

    def test_adds_note_to_director(self, Tester):
        key = "key"
        value = "note"
        MockQuestion = mock.Mock(spec_set=Question)
        MockQuestion.answered_by.return_value = value

        MakeNote.of_the(MockQuestion).as_(key).perform_as(Tester)

        assert Director().looks_up(key) == value

    def test_can_use_value_instead_of_question(self, Tester):
        key = "key"
        test_note = "note"

        MakeNote.of_the(test_note).as_(key).perform_as(Tester)

        assert Director().looks_up(key) == test_note

    def test_using_note_immediately_raises_with_docs(self, Tester):
        MockQuestion = mock.Mock(spec_set=Question)
        key = "spam, spam, spam, spam, baked beans, and spam"

        with pytest.raises(UnableToDirect) as exc:
            Tester.attempts_to(
                MakeNote.of_the(MockQuestion).as_(key),
                noted_under(key),
            )

        assert "screenpy-docs.readthedocs.io" in str(exc.value)

    def test_describe(self):
        assert MakeNote(None).as_("blah").describe() == f"Make a note under blah."
    
    @mock.patch("screenpy.actions.make_note.aside")
    def test_caught_exception_noted(self, mock_aside: mock.Mock, Tester):
        key = "key"
        value = "note"
        MockQuestion = mock.Mock()
        MockQuestion.answered_by.return_value = value
        MockQuestion.caught_exception = ValueError("Failure msg")

        MakeNote.of_the(MockQuestion).as_(key).perform_as(Tester)
        mock_aside.assert_has_calls((
            mock.call(f"Making note of {MockQuestion}..."),
            mock.call(f"Caught Exception: {MockQuestion.caught_exception}"))
        )
        return


class TestPause:
    def test_can_be_instantiated(self):
        p1 = Pause.for_(20)
        p2 = Pause.for_(20).seconds_because("test")
        p3 = Pause.for_(20).milliseconds_because("test")

        assert isinstance(p1, Pause)
        assert isinstance(p2, Pause)
        assert isinstance(p3, Pause)

    def test_implements_protocol(self):
        p = Pause(1)
        assert isinstance(p, Performable)
        assert isinstance(p, Describable)

    def test_seconds(self):
        """Choosing seconds stores the correct time"""
        duration = 20
        pause = Pause.for_(duration).seconds_because("test")

        assert pause.time == duration

    def test_milliseconds(self):
        """Choosing milliseconds stores the correct time"""
        duration = 20
        pause = Pause.for_(duration).milliseconds_because("Test")

        assert pause.time == duration / 1000.0

    def test_units_are_pluralized_correctly(self):
        """Unit is pluralized if more than 1"""
        p1 = Pause.for_(1).second_because("test")
        p2 = Pause.for_(1).milliseconds_because("test")
        p3 = Pause.for_(2).seconds_because("test")
        p4 = Pause.for_(2).milliseconds_because("test")

        assert not p1.unit.endswith("s")
        assert not p2.unit.endswith("s")
        assert p3.unit.endswith("s")
        assert p4.unit.endswith("s")

    def test_reason_is_massaged_correctly(self):
        p1 = Pause.for_(1).second_because("because reasons.")
        p2 = Pause.for_(1).second_because("reasons")
        p3 = Pause.for_(1000).milliseconds_because("because reasons.")
        p4 = Pause.for_(1000).milliseconds_because("reasons")

        assert p1.reason == p2.reason == "because reasons"
        assert p3.reason == p4.reason == "because reasons"

    @mock.patch("screenpy.actions.pause.sleep")
    def test_calls_sleep(self, mocked_sleep, Tester):
        duration = 20

        Pause.for_(duration).seconds_because("").perform_as(Tester)

        mocked_sleep.assert_called_once_with(duration)

    def test_complains_for_missing_reason(self, Tester):
        with pytest.raises(UnableToAct):
            Pause.for_(20).perform_as(Tester)

    def test_describe(self):
        assert Pause(1).second_because("moo").describe() == f"Pause for 1 second because moo."


class TestSee:
    def test_can_be_instantiated(self):
        s1 = See(None, mock.Mock(spec_set=BaseResolution))
        s2 = See.the(None, mock.Mock(spec_set=BaseResolution))

        assert isinstance(s1, See)
        assert isinstance(s2, See)

    def test_implements_protocol(self):
        s = See(None, mock.Mock())
        assert isinstance(s, Performable)
        assert isinstance(s, Describable)

    @mock.patch("screenpy.actions.see.assert_that")
    def test_calls_assert_that_with_answered_question(self, mocked_assert_that, Tester):
        mock_question = mock.Mock(spec=Question)
        mock_question.describe.return_value = "What was your mother?"
        mock_question.caught_exception = ValueError("Failure msg")
        mock_resolution = mock.Mock(spec_set=BaseResolution)
        mock_resolution.get_line.return_value = "A hamster!"

        See.the(mock_question, mock_resolution).perform_as(Tester)

        mock_question.answered_by.assert_called_once_with(Tester)
        mocked_assert_that.assert_called_once_with(
            mock_question.answered_by.return_value, mock_resolution, str(mock_question.caught_exception)
        )

    @mock.patch("screenpy.actions.see.assert_that")
    def test_calls_assert_that_with_value(self, mocked_assert_that, Tester):
        test_value = "Your father smelt of"
        mock_resolution = mock.Mock(spec_set=BaseResolution)
        mock_resolution.get_line.return_value = "Elderberries!"

        See.the(test_value, mock_resolution).perform_as(Tester)

        mocked_assert_that.assert_called_once_with(test_value, mock_resolution, "")

    def test_describe(self):
        mock_question = mock.Mock(spec_set=Question)
        mock_question.describe.return_value = "Can you speak?"
        mock_resolution = mock.Mock(spec_set=BaseResolution)
        mock_resolution.get_line.return_value = "I speak"
        assert See(mock_question, mock_resolution).describe() == f"See if can you speak is I speak."


class TestSeeAllOf:
    def test_can_be_instantiated(self):
        sao1 = SeeAllOf(None, None)
        sao2 = SeeAllOf.the(None, None)

        assert isinstance(sao1, SeeAllOf)
        assert isinstance(sao2, SeeAllOf)

    def test_implements_protocol(self):
        s = SeeAllOf(None, None)
        assert isinstance(s, Performable)
        assert isinstance(s, Describable)

    def test_raises_exception_for_too_few_tests(self):
        with pytest.raises(UnableToAct):
            SeeAllOf(None)

    @mock.patch("screenpy.actions.see_all_of.See")
    def test_calls_see_for_each_test(self, MockedSee, Tester):
        num_tests = 3
        tests = ((mock.Mock(spec_set=Question), mock.Mock(spec_set=BaseResolution)),) * num_tests

        SeeAllOf.the(*tests).perform_as(Tester)

        assert MockedSee.the.call_count == num_tests
        # In 3.7 and earlier, you can't get the .args of a method call from
        # the mocked instance. We can't do the full test there.
        if sys.version_info >= (3, 8):
            for num, test in enumerate(tests):
                assert MockedSee.method_calls[num].args == test

    def test_raises_assertionerror_if_one_fails(self, Tester):
        with pytest.raises(AssertionError):
            SeeAllOf(
                (True, IsEqualTo(True)),
                (True, IsEqualTo(False)),  # <--
                (True, IsEqualTo(True)),
                (True, IsEqualTo(True)),
            ).perform_as(Tester)

    def test_passes_if_all_pass(self, Tester):
        # test passes if no exception is raised
        SeeAllOf(
            (True, IsEqualTo(True)),
            (True, IsEqualTo(True)),
            (True, IsEqualTo(True)),
            (True, IsEqualTo(True)),
        ).perform_as(Tester)

    def test_describe(self):
        tests = ((True, IsEqualTo(True)),
                 (True, IsEqualTo(True)),
                 (True, IsEqualTo(True)),
                 (True, IsEqualTo(True)),)
        assert SeeAllOf(*tests).describe() == f"See if all of 4 tests pass."

class TestSeeAnyOf:
    def test_can_be_instantiated(self):
        sao1 = SeeAnyOf(None, None)
        sao2 = SeeAnyOf.the(None, None)

        assert isinstance(sao1, SeeAnyOf)
        assert isinstance(sao2, SeeAnyOf)

    def test_implements_protocol(self):
        s = SeeAnyOf(None, None)
        assert isinstance(s, Performable)
        assert isinstance(s, Describable)

    def test_raises_exception_for_too_few_tests(self):
        with pytest.raises(UnableToAct):
            SeeAnyOf(None)

    @mock.patch("screenpy.actions.see_any_of.See")
    def test_calls_see_for_each_test(self, MockedSee, Tester):
        num_tests = 3
        tests = ((mock.Mock(spec_set=Question), mock.Mock(spec_set=BaseResolution)),) * num_tests

        SeeAnyOf.the(*tests).perform_as(Tester)

        assert MockedSee.the.call_count == num_tests
        # In 3.7 and earlier, you can't get the .args of a method call from
        # the mocked instance. We can't do the full test there.
        if sys.version_info >= (3, 8):
            for num, test in enumerate(tests):
                assert MockedSee.method_calls[num].args == test

    def test_raises_assertionerror_if_none_pass(self, Tester):
        with pytest.raises(AssertionError) as actual_exception:
            SeeAnyOf(
                (True, IsEqualTo(False)),
                (True, IsEqualTo(False)),
            ).perform_as(Tester)

        assert "did not find any expected answers" in str(actual_exception)

    def test_passes_with_one_pass(self, Tester):
        # test passes if no exception is raised
        SeeAnyOf(
            (True, IsEqualTo(False)),
            (True, IsEqualTo(False)),
            (True, IsEqualTo(True)),  # <--
            (True, IsEqualTo(False)),
        ).perform_as(Tester)

    def test_describe(self):
        tests = ((True, IsEqualTo(True)),
                 (True, IsEqualTo(True)),
                 (True, IsEqualTo(True)),
                 (True, IsEqualTo(True)),)
        assert SeeAnyOf(*tests).describe() == f"See if any of 4 tests pass."
