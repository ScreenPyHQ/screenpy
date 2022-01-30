from unittest import mock
import sys

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
from screenpy.resolutions import IsEqualTo

from tests.conftest import mock_settings


class TestAttachTheFile:
    def test_can_be_instantiated(self):
        atf = AttachTheFile("")

        assert isinstance(atf, AttachTheFile)

    @mock.patch("screenpy.actions.attach_the_file.the_narrator")
    def test_perform_attach_the_file_sends_kwargs(self, mocked_narrator, Tester):
        test_path = "souiiie.png"
        test_kwargs = {"color": "Red", "weather": "Tornado"}

        AttachTheFile(test_path, **test_kwargs).perform_as(Tester)

        mocked_narrator.attaches_a_file.assert_called_once_with(
            test_path, **test_kwargs
        )


class TestDebug:
    def test_can_be_instantiated(self):
        d = Debug()

        assert isinstance(d, Debug)

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


class TestEventually:

    def get_mock_action(self, **kwargs):
        mock_action = mock.Mock()
        mock_action.perform_as = mock.Mock(**kwargs)
        mock_action.describe.return_value = "An African or a European swallow?"
        return mock_action

    def test_can_be_instantiated(self):
        e1 = Eventually(None)
        e2 = Eventually(None).trying_for(0).seconds()
        e3 = Eventually(None).trying_for(0).milliseconds()
        e4 = Eventually(None).polling(0).seconds()

        assert isinstance(e1, Eventually)
        assert isinstance(e2, Eventually)
        assert isinstance(e3, Eventually)
        assert isinstance(e4, Eventually)

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
            .polling_every(200).milliseconds()
            .for_(100).milliseconds()
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


class TestMakeNote:
    def test_can_be_instantiated(self):
        mn1 = MakeNote(None)
        mn2 = MakeNote.of_the(None)
        mn3 = MakeNote.of_the(None).as_("")

        assert isinstance(mn1, MakeNote)
        assert isinstance(mn2, MakeNote)
        assert isinstance(mn3, MakeNote)

    def test_key_value_set(self):
        test_question = "Do I feel lucky?"
        test_key = "Well, do you, punk?"

        mn = MakeNote.of_the(test_question).as_(test_key)

        assert mn.question == test_question
        assert mn.key == test_key

    def test_answers_question(self, Tester):
        MockQuestion = mock.Mock()

        MakeNote.of_the(MockQuestion).as_("test").perform_as(Tester)

        assert MockQuestion.answered_by.called_once_with(Tester)

    def test_raises_without_key(self, Tester):
        with pytest.raises(UnableToAct):
            MakeNote.of_the(None).perform_as(Tester)

    def test_adds_note_to_director(self, Tester):
        key = "key"
        value = "note"
        MockQuestion = mock.Mock()
        MockQuestion.answered_by.return_value = value

        MakeNote.of_the(MockQuestion).as_(key).perform_as(Tester)

        assert Director().looks_up(key) == value

    def test_can_use_value_instead_of_question(self, Tester):
        key = "key"
        test_note = "note"

        MakeNote.of_the(test_note).as_(key).perform_as(Tester)

        assert Director().looks_up(key) == test_note

    def test_using_note_immediately_raises_with_docs(self, Tester):
        MockQuestion = mock.Mock()
        key = "spam, spam, spam, spam, baked beans, and spam"

        with pytest.raises(UnableToDirect) as exc:
            Tester.attempts_to(
                MakeNote.of_the(MockQuestion).as_(key),
                noted_under(key),
            )

        assert "screenpy-docs.readthedocs.io" in str(exc.value)


class TestPause:
    def test_can_be_instantiated(self):
        p1 = Pause.for_(20)
        p2 = Pause.for_(20).seconds_because("test")
        p3 = Pause.for_(20).milliseconds_because("test")

        assert isinstance(p1, Pause)
        assert isinstance(p2, Pause)
        assert isinstance(p3, Pause)

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


class TestSee:
    def test_can_be_instantiated(self):
        s1 = See(None, mock.Mock())
        s2 = See.the(None, mock.Mock())

        assert isinstance(s1, See)
        assert isinstance(s2, See)

    @mock.patch("screenpy.actions.see.assert_that")
    def test_calls_assert_that_with_answered_question(self, mocked_assert_that, Tester):
        mock_question = mock.Mock()
        mock_question.describe.return_value = "What was your mother?"
        mock_resolution = mock.Mock()
        mock_resolution.describe.return_value = "A hamster!"

        See.the(mock_question, mock_resolution).perform_as(Tester)

        mock_question.answered_by.assert_called_once_with(Tester)
        mocked_assert_that.assert_called_once_with(
            mock_question.answered_by.return_value, mock_resolution
        )

    @mock.patch("screenpy.actions.see.assert_that")
    def test_calls_assert_that_with_value(self, mocked_assert_that, Tester):
        test_value = "Your father smelt of"
        mock_resolution = mock.Mock()
        mock_resolution.describe.return_value = "Elderberries!"

        See.the(test_value, mock_resolution).perform_as(Tester)

        mocked_assert_that.assert_called_once_with(test_value, mock_resolution)


class TestSeeAllOf:
    def test_can_be_instantiated(self):
        sao1 = SeeAllOf(None, None)
        sao2 = SeeAllOf.the(None, None)

        assert isinstance(sao1, SeeAllOf)
        assert isinstance(sao2, SeeAllOf)

    def test_raises_exception_for_too_few_tests(self):
        with pytest.raises(UnableToAct):
            SeeAllOf(None)

    @mock.patch("screenpy.actions.see_all_of.See")
    def test_calls_see_for_each_test(self, MockedSee, Tester):
        num_tests = 3
        tests = ((mock.Mock(), mock.Mock()),) * num_tests

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


class TestSeeAnyOf:
    def test_can_be_instantiated(self):
        sao1 = SeeAnyOf(None, None)
        sao2 = SeeAnyOf.the(None, None)

        assert isinstance(sao1, SeeAnyOf)
        assert isinstance(sao2, SeeAnyOf)

    def test_raises_exception_for_too_few_tests(self):
        with pytest.raises(UnableToAct):
            SeeAnyOf(None)

    @mock.patch("screenpy.actions.see_any_of.See")
    def test_calls_see_for_each_test(self, MockedSee, Tester):
        num_tests = 3
        tests = ((mock.Mock(), mock.Mock()),) * num_tests

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
