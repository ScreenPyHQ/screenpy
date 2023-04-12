import logging
import os
import sys
import time
from unittest import mock

import pytest
from pytest_mock import MockerFixture

from screenpy import (
    Actor,
    Answerable,
    AttachTheFile,
    Debug,
    DeliveryError,
    Describable,
    Director,
    Eventually,
    IsEqualTo,
    MakeNote,
    NotAnswerable,
    NotPerformable,
    NotResolvable,
    Pause,
    Performable,
    Resolvable,
    See,
    SeeAllOf,
    SeeAnyOf,
    Silently,
    UnableToAct,
    UnableToDirect,
    beat,
    noted_under,
    settings,
    the_narrator,
)
from screenpy.actions.silently import (
    SilentlyAnswerable,
    SilentlyPerformable,
    SilentlyResolvable,
)
from screenpy.test_utils import mock_settings
from unittest_protocols import ErrorQuestion
from useful_mocks import (
    get_mock_action_class,
    get_mock_question_class,
    get_mock_resolution_class,
)

FakeAction = get_mock_action_class()
FakeQuestion = get_mock_question_class()
FakeResolution = get_mock_resolution_class()


class DoThingThatFails(Performable):
    COUNTER = 0

    def perform_as(self, actor: Actor):
        DoThingThatFails.COUNTER += 1
        raise AssertionError(f"Failure #{DoThingThatFails.COUNTER}")


class TestAttachTheFile:
    def test_can_be_instantiated(self) -> None:
        atf = AttachTheFile("")

        assert isinstance(atf, AttachTheFile)

    def test_implements_protocol(self) -> None:
        atf = AttachTheFile("")

        assert isinstance(atf, Performable)
        assert isinstance(atf, Describable)

    def test_divines_filename(self) -> None:
        filename = "thisisonlyatest.png"
        filepath = os.sep.join(["this", "is", "a", "test", filename])
        atf_without_path = AttachTheFile(filename)
        atf_with_path = AttachTheFile(filepath)

        assert atf_without_path.filename == filename
        assert atf_with_path.filename == filename

    @mock.patch("screenpy.actions.attach_the_file.the_narrator", autospec=True)
    def test_perform_attach_the_file_sends_kwargs(
        self, mocked_narrator, Tester
    ) -> None:
        test_path = "souiiie.png"
        test_kwargs = {"color": "Red", "weather": "Tornado"}

        AttachTheFile(test_path, **test_kwargs).perform_as(Tester)

        mocked_narrator.attaches_a_file.assert_called_once_with(
            test_path, **test_kwargs
        )

    def test_describe(self) -> None:
        file = "somefile.txt"
        assert AttachTheFile(file).describe() == f"Attach a file named {file}."


class TestDebug:
    def test_can_be_instantiated(self) -> None:
        d = Debug()

        assert isinstance(d, Debug)

    def test_implements_protocol(self) -> None:
        d = Debug()

        assert isinstance(d, Performable)
        assert isinstance(d, Describable)

    @mock.patch("screenpy.actions.debug.breakpoint")
    def test_calls_breakpoint(self, mocked_breakpoint, Tester) -> None:
        Debug().perform_as(Tester)

        mocked_breakpoint.assert_called_once()

    @mock.patch("screenpy.actions.debug.breakpoint")
    @mock.patch("screenpy.actions.debug.pdb")
    def test_falls_back_to_pdb(self, mocked_pdb, mocked_breakpoint, Tester) -> None:
        mocked_breakpoint.side_effect = NameError("name 'breakpoint' is not defined")

        Debug().perform_as(Tester)

        mocked_pdb.set_trace.assert_called_once()

    def test_describe(self) -> None:
        assert Debug().describe() == "Assume direct control."


class TestEventually:
    def test_can_be_instantiated(self) -> None:
        e1 = Eventually(FakeAction())
        e2 = Eventually(FakeAction()).trying_for_no_longer_than(0).seconds()
        e3 = Eventually(FakeAction()).trying_for(0).milliseconds()
        e4 = Eventually(FakeAction()).for_(0).seconds()
        e5 = Eventually(FakeAction()).waiting_for(0).seconds()
        e6 = Eventually(FakeAction()).polling(0).seconds()
        e7 = Eventually(FakeAction()).polling_every(0).milliseconds()
        e8 = Eventually(FakeAction()).trying_every(0).seconds()

        assert isinstance(e1, Eventually)
        assert isinstance(e2, Eventually)
        assert isinstance(e3, Eventually)
        assert isinstance(e4, Eventually)
        assert isinstance(e5, Eventually)
        assert isinstance(e6, Eventually)
        assert isinstance(e7, Eventually)
        assert isinstance(e8, Eventually)

    def test_implements_protocol(self) -> None:
        t = Eventually(FakeAction())

        assert isinstance(t, Performable)
        assert isinstance(t, Describable)

    def test_uses_timeframe_builder(self) -> None:
        ev = Eventually(FakeAction()).trying_for(1)

        assert isinstance(ev, Eventually._TimeframeBuilder)

    def test_can_adjust_timeout(self) -> None:
        ev = Eventually(FakeAction()).trying_for(12)

        # is still _TimeframeBuilder, so get the stored Eventually
        assert ev.eventually.timeout == 12

    def test_can_adjust_timeout_seconds(self) -> None:
        ev = Eventually(FakeAction()).trying_for(15).seconds()

        assert ev.timeout == 15

    def test_can_adjust_timeout_milliseconds(self) -> None:
        ev = Eventually(FakeAction()).trying_for(1200).milliseconds()

        assert ev.timeout == 1.2

    def test_can_adjust_polling_frequency(self) -> None:
        ev = Eventually(FakeAction()).polling(1).second()

        assert ev.poll == 1

    @mock_settings(TIMEOUT=100)
    def test_adjusting_settings_timeout(self) -> None:
        ev = Eventually(FakeAction())

        assert ev.timeout == 100

    @mock_settings(POLLING=50)
    def test_adjusting_settings_polling(self) -> None:
        ev = Eventually(FakeAction())

        assert ev.poll == 50

    def test_can_adjust_timeout_and_polling(self) -> None:
        ev = Eventually(FakeAction()).trying_for(23).seconds().polling(3).second()
        assert ev.timeout == 23
        assert ev.poll == 3

    def test__timeframebuilder_is_performable(self, Tester) -> None:
        # test passes if no exception is raised
        Eventually(FakeAction()).for_(1).perform_as(Tester)

    def test_valueerror_when_poll_is_larger_than_timeout(self, Tester) -> None:
        ev = (
            Eventually(FakeAction())
            .polling_every(200)
            .milliseconds()
            .for_(100)
            .milliseconds()
        )

        with pytest.raises(ValueError) as actual_exception:
            ev.perform_as(Tester)

        assert "poll must be less than or equal to timeout" in str(actual_exception)

    @mock.patch("screenpy.actions.eventually.time", autospec=True)
    def test_perform_eventually_times_out(self, mocked_time, Tester) -> None:
        num_calls = 5
        mocked_time.time = mock.create_autospec(
            time.time, side_effect=[1] * num_calls + [100]
        )
        mock_action = FakeAction()
        mock_action.perform_as.side_effect = ValueError("'Tis but a flesh wound!")

        with pytest.raises(DeliveryError):
            Eventually(mock_action).perform_as(Tester)

        assert mocked_time.time.call_count == num_calls + 1

    @mock.patch("screenpy.actions.eventually.time", autospec=True)
    def test_timeout_mentions_num_executions(self, mocked_time, Tester) -> None:
        num_calls = 5
        mocked_time.time = mock.create_autospec(
            time.time, side_effect=[1] * num_calls + [100]
        )
        mock_action = FakeAction()
        mock_action.perform_as.side_effect = ValueError("He's pining for the fjords!")

        with pytest.raises(DeliveryError) as e:
            Eventually(mock_action).perform_as(Tester)

        assert f"{num_calls} times" in str(e)

    @mock.patch("screenpy.actions.eventually.time", autospec=True)
    def test_catches_exceptions(self, mocked_time, Tester) -> None:
        mocked_time.time = mock.create_autospec(time.time, side_effect=[1, 1, 100])
        msg = "I got better."
        mock_action = FakeAction()
        mock_action.perform_as.side_effect = ValueError(msg)

        with pytest.raises(DeliveryError) as actual_exception:
            Eventually(mock_action).perform_as(Tester)

        assert msg in str(actual_exception)

    @mock.patch("screenpy.actions.eventually.time", autospec=True)
    def test_mentions_all_errors(self, mocked_time, Tester) -> None:
        mocked_time.time = mock.create_autospec(time.time, side_effect=[1, 1, 100])
        exc1 = ValueError("These tracts of land aren't that huge!")
        exc2 = TypeError("This witch does not weigh as much as a duck!")
        mock_action = FakeAction()
        mock_action.perform_as.side_effect = [exc1, exc2]

        with pytest.raises(DeliveryError) as actual_exception:
            Eventually(mock_action).perform_as(Tester)

        assert exc1.__class__.__name__ in str(actual_exception.value)
        assert str(exc1) in str(actual_exception.value)
        assert exc2.__class__.__name__ in str(actual_exception.value)
        assert str(exc2) in str(actual_exception.value)

    @mock.patch("screenpy.actions.eventually.time", autospec=True)
    def test_mention_all_errors_in_order(self, mocked_time, Tester):
        num_calls = 5
        mocked_time.time = mock.create_autospec(
            time.time, side_effect=[1] * num_calls + [100]
        )

        with pytest.raises(DeliveryError) as actual_exception:
            Eventually(DoThingThatFails()).perform_as(Tester)

        assert str(actual_exception.value) == (
            "Tester tried to Eventually do thing that fails 5 times over 20.0 seconds,"
            " but got:\n"
            "    AssertionError: Failure #1\n"
            "    AssertionError: Failure #2\n"
            "    AssertionError: Failure #3\n"
            "    AssertionError: Failure #4\n"
            "    AssertionError: Failure #5"
        )
        return

    def test_describe(self) -> None:
        mock_action = FakeAction()
        mock_action.describe.return_value = "An African or a European swallow?"
        assert (
            Eventually(mock_action).describe()
            == "Eventually an African or a European swallow."
        )

    def test_describe_none(self) -> None:
        assert (
            Eventually(FakeAction()).describe() == "Eventually something indescribable."
        )


class TestMakeNote:
    def test_can_be_instantiated(self) -> None:
        mn1 = MakeNote(None)
        mn2 = MakeNote.of(None)
        mn3 = MakeNote.of_the(None).as_("")

        assert isinstance(mn1, MakeNote)
        assert isinstance(mn2, MakeNote)
        assert isinstance(mn3, MakeNote)

    def test_implements_protocol(self) -> None:
        m = MakeNote("")

        assert isinstance(m, Performable)
        assert isinstance(m, Describable)

    def test_key_value_set(self) -> None:
        test_question = "Do I feel lucky?"
        test_key = "Well, do you, punk?"

        mn = MakeNote.of_the(test_question).as_(test_key)

        assert mn.question == test_question
        assert mn.key == test_key

    def test_answers_question(self, Tester) -> None:
        mock_question = FakeQuestion()
        MakeNote.of_the(mock_question).as_("test").perform_as(Tester)
        mock_question.answered_by.assert_called_once_with(Tester)

    def test_raises_without_key(self, Tester) -> None:
        with pytest.raises(UnableToAct):
            MakeNote.of_the(None).perform_as(Tester)

    def test_adds_note_to_director(self, Tester) -> None:
        key = "key"
        value = "note"
        mock_question = FakeQuestion()
        mock_question.answered_by.return_value = value

        MakeNote.of_the(mock_question).as_(key).perform_as(Tester)

        assert Director().looks_up(key) == value

    def test_can_use_value_instead_of_question(self, Tester) -> None:
        key = "key"
        test_note = "note"

        MakeNote.of_the(test_note).as_(key).perform_as(Tester)

        assert Director().looks_up(key) == test_note

    def test_using_note_immediately_raises_with_docs(self, Tester) -> None:
        mock_question = FakeQuestion()
        key = "spam, spam, spam, spam, baked beans, and spam"

        with pytest.raises(UnableToDirect) as exc:
            Tester.attempts_to(
                MakeNote.of_the(mock_question).as_(key),
                noted_under(key),
            )

        assert "screenpy-docs.readthedocs.io" in str(exc.value)

    def test_describe(self) -> None:
        assert MakeNote(None).as_("blah").describe() == "Make a note under blah."

    @mock.patch("screenpy.actions.make_note.aside", autospec=True)
    def test_caught_exception_noted(self, mock_aside: mock.Mock, Tester) -> None:
        key = "key"
        value = "note"
        mock_question = mock.create_autospec(ErrorQuestion, instance=True)
        mock_question.answered_by.return_value = value
        mock_question.caught_exception = ValueError("Failure msg")

        MakeNote.of_the(mock_question).as_(key).perform_as(Tester)
        mock_aside.assert_has_calls(
            (
                mock.call(f"Making note of {mock_question}..."),
                mock.call(f"Caught Exception: {mock_question.caught_exception}"),
            )
        )
        return


class TestPause:
    def test_can_be_instantiated(self) -> None:
        p1 = Pause.for_(20)
        p2 = Pause.for_(20).seconds_because("test")
        p3 = Pause.for_(20).milliseconds_because("test")

        assert isinstance(p1, Pause)
        assert isinstance(p2, Pause)
        assert isinstance(p3, Pause)

    def test_implements_protocol(self) -> None:
        p = Pause(1)

        assert isinstance(p, Performable)
        assert isinstance(p, Describable)

    def test_seconds(self) -> None:
        """Choosing seconds stores the correct time"""
        duration = 20
        pause = Pause.for_(duration).seconds_because("test")

        assert pause.time == duration

    def test_milliseconds(self) -> None:
        """Choosing milliseconds stores the correct time"""
        duration = 20
        pause = Pause.for_(duration).milliseconds_because("Test")

        assert pause.time == duration / 1000.0

    def test_units_are_pluralized_correctly(self) -> None:
        """Unit is pluralized if more than 1"""
        p1 = Pause.for_(1).second_because("test")
        p2 = Pause.for_(1).milliseconds_because("test")
        p3 = Pause.for_(2).seconds_because("test")
        p4 = Pause.for_(2).milliseconds_because("test")

        assert not p1.unit.endswith("s")
        assert not p2.unit.endswith("s")
        assert p3.unit.endswith("s")
        assert p4.unit.endswith("s")

    def test_reason_is_massaged_correctly(self) -> None:
        p1 = Pause.for_(1).second_because("because reasons.")
        p2 = Pause.for_(1).second_because("reasons")
        p3 = Pause.for_(1000).milliseconds_because("because reasons.")
        p4 = Pause.for_(1000).milliseconds_because("reasons")

        assert p1.reason == p2.reason == "because reasons"
        assert p3.reason == p4.reason == "because reasons"

    @mock.patch("screenpy.actions.pause.sleep", autospec=True)
    def test_calls_sleep(self, mocked_sleep, Tester) -> None:
        duration = 20

        Pause.for_(duration).seconds_because("").perform_as(Tester)

        mocked_sleep.assert_called_once_with(duration)

    def test_complains_for_missing_reason(self, Tester) -> None:
        with pytest.raises(UnableToAct):
            Pause.for_(20).perform_as(Tester)

    def test_describe(self) -> None:
        assert (
            Pause(1).second_because("moo").describe()
            == "Pause for 1 second because moo."
        )


class TestSee:
    def test_can_be_instantiated(self) -> None:
        s1 = See(None, FakeResolution())
        s2 = See.the(None, FakeResolution())

        assert isinstance(s1, See)
        assert isinstance(s2, See)

    def test_implements_protocol(self) -> None:
        s = See(None, FakeResolution())

        assert isinstance(s, Performable)
        assert isinstance(s, Describable)

    @mock.patch("screenpy.actions.see.assert_that")
    def test_calls_assert_that_with_answered_question(
        self, mocked_assert_that, Tester
    ) -> None:
        mock_question = FakeQuestion()
        mock_question.describe.return_value = "What was your mother?"
        mock_question.caught_exception = ValueError("Failure msg")
        mock_resolution = FakeResolution()
        mock_resolution.describe.return_value = "A hamster!"

        See.the(mock_question, mock_resolution).perform_as(Tester)

        mock_question.answered_by.assert_called_once_with(Tester)
        mocked_assert_that.assert_called_once_with(
            mock_question.answered_by.return_value,
            mock_resolution,
            str(mock_question.caught_exception),
        )

    @mock.patch("screenpy.actions.see.assert_that")
    def test_calls_assert_that_with_value(self, mocked_assert_that, Tester) -> None:
        test_value = "Your father smelt of"
        mock_resolution = FakeResolution()
        mock_resolution.describe.return_value = "Elderberries!"

        See.the(test_value, mock_resolution).perform_as(Tester)

        mocked_assert_that.assert_called_once_with(test_value, mock_resolution, "")

    def test_describe(self) -> None:
        mock_question = FakeQuestion()
        mock_question.describe.return_value = "Can you speak?"
        mock_resolution = FakeResolution()
        mock_resolution.describe.return_value = "Only this sentence."

        assert (
            See(mock_question, mock_resolution).describe()
            == "See if can you speak is only this sentence."
        )


class TestSeeAllOf:
    def test_can_be_instantiated(self) -> None:
        sao1 = SeeAllOf(("FakeQuestion()", FakeResolution()))
        sao2 = SeeAllOf.the((FakeQuestion(), FakeResolution()))

        assert isinstance(sao1, SeeAllOf)
        assert isinstance(sao2, SeeAllOf)

    def test_implements_protocol(self) -> None:
        s = SeeAllOf((FakeQuestion(), FakeResolution()))

        assert isinstance(s, Performable)
        assert isinstance(s, Describable)

    def test_raises_exception(self) -> None:
        with pytest.raises(TypeError):
            SeeAllOf(FakeQuestion())  # type: ignore

        with pytest.raises(UnableToAct):
            SeeAllOf((FakeQuestion(),))  # type: ignore

        with pytest.raises(UnableToAct):
            SeeAllOf((FakeQuestion(), FakeResolution(), 1))  # type: ignore

    @mock.patch("screenpy.actions.see_all_of.See")
    def test_calls_see_for_each_test(self, MockedSee, Tester) -> None:
        num_tests = 3
        tests = ((FakeQuestion(), FakeResolution()),) * num_tests

        SeeAllOf.the(*tests).perform_as(Tester)

        assert MockedSee.the.call_count == num_tests
        # In 3.7 and earlier, you can't get the .args of a method call from
        # the mocked instance. We can't do the full test there.
        if sys.version_info >= (3, 8):
            for num, test in enumerate(tests):
                assert MockedSee.method_calls[num].args == test

    def test_raises_assertionerror_if_one_fails(self, Tester) -> None:
        with pytest.raises(AssertionError):
            SeeAllOf(
                (FakeQuestion(), IsEqualTo(True)),
                (FakeQuestion(), IsEqualTo(False)),  # <--
                (FakeQuestion(), IsEqualTo(True)),
                (FakeQuestion(), IsEqualTo(True)),
            ).perform_as(Tester)

    def test_passes_if_all_pass(self, Tester) -> None:
        # test passes if no exception is raised
        SeeAllOf(
            (FakeQuestion(), IsEqualTo(True)),
            (FakeQuestion(), IsEqualTo(True)),
            (FakeQuestion(), IsEqualTo(True)),
            (FakeQuestion(), IsEqualTo(True)),
        ).perform_as(Tester)

    def test_describe(self) -> None:
        test = (FakeQuestion(), IsEqualTo(True))
        tests = (
            (FakeQuestion(), IsEqualTo(True)),
            (FakeQuestion(), IsEqualTo(True)),
            (FakeQuestion(), IsEqualTo(True)),
            (FakeQuestion(), IsEqualTo(True)),
        )

        assert SeeAllOf().describe() == "See if no tests pass 🤔."
        assert SeeAllOf(test).describe() == "See if 1 test passes."
        assert SeeAllOf(*tests).describe() == f"See if all of {len(tests)} tests pass."


class TestSeeAnyOf:
    def test_can_be_instantiated(self) -> None:
        sao1 = SeeAnyOf((FakeQuestion(), FakeResolution()))
        sao2 = SeeAnyOf.the((FakeQuestion(), FakeResolution()))

        assert isinstance(sao1, SeeAnyOf)
        assert isinstance(sao2, SeeAnyOf)

    def test_implements_protocol(self) -> None:
        s = SeeAnyOf((FakeQuestion(), FakeResolution()))

        assert isinstance(s, Performable)
        assert isinstance(s, Describable)

    def test_raises_exception(self) -> None:
        with pytest.raises(TypeError):
            SeeAnyOf(FakeQuestion())  # type: ignore

        with pytest.raises(UnableToAct):
            SeeAnyOf((FakeQuestion(),))  # type: ignore

        with pytest.raises(UnableToAct):
            SeeAnyOf((FakeQuestion(), FakeResolution(), 1))  # type: ignore

    @mock.patch("screenpy.actions.see_any_of.See")
    def test_calls_see_for_each_test(self, MockedSee, Tester) -> None:
        num_tests = 3
        tests = ((FakeQuestion(), FakeResolution()),) * num_tests

        SeeAnyOf.the(*tests).perform_as(Tester)

        assert MockedSee.the.call_count == num_tests
        # In 3.7 and earlier, you can't get the .args of a method call from
        # the mocked instance. We can't do the full test there.
        if sys.version_info >= (3, 8):
            for num, test in enumerate(tests):
                assert MockedSee.method_calls[num].args == test

    def test_raises_assertionerror_if_none_pass(self, Tester) -> None:
        with pytest.raises(AssertionError) as actual_exception:
            SeeAnyOf(
                (FakeQuestion(), IsEqualTo(False)),
                (FakeQuestion(), IsEqualTo(False)),
            ).perform_as(Tester)

        assert "did not find any expected answers" in str(actual_exception)

    def test_passes_with_one_pass(self, Tester) -> None:
        # test passes if no exception is raised
        SeeAnyOf(
            (FakeQuestion(), IsEqualTo(False)),
            (FakeQuestion(), IsEqualTo(False)),
            (FakeQuestion(), IsEqualTo(True)),  # <--
            (FakeQuestion(), IsEqualTo(False)),
        ).perform_as(Tester)

    def test_describe(self) -> None:
        test = (FakeQuestion(), IsEqualTo(True))
        tests = (
            (FakeQuestion(), IsEqualTo(True)),
            (FakeQuestion(), IsEqualTo(True)),
            (FakeQuestion(), IsEqualTo(True)),
            (FakeQuestion(), IsEqualTo(True)),
        )

        assert SeeAnyOf().describe() == "See if no tests pass 🤔."
        assert SeeAnyOf(test).describe() == "See if 1 test passes."
        assert SeeAnyOf(*tests).describe() == f"See if any of {len(tests)} tests pass."


class SimpleQuestion(Answerable):
    @beat("{} examines SimpleQuestion")
    def answered_by(self, actor: Actor) -> bool:
        return True

    def describe(self) -> str:
        return "SimpleQuestion"


class TestSilently:
    def test_function_returns_properly(self) -> None:
        q1 = Silently(FakeQuestion())
        q2 = Silently(FakeAction())
        q3 = Silently(FakeResolution())

        assert isinstance(q1, SilentlyAnswerable)
        assert isinstance(q2, SilentlyPerformable)
        assert isinstance(q3, SilentlyResolvable)

    def test_can_be_instantiated(self) -> None:
        q1 = SilentlyAnswerable(FakeQuestion())
        q2 = SilentlyPerformable(FakeAction())
        q3 = SilentlyResolvable(FakeResolution())

        assert isinstance(q1, SilentlyAnswerable)
        assert isinstance(q2, SilentlyPerformable)
        assert isinstance(q3, SilentlyResolvable)

    def test_implements_protocol(self) -> None:
        q1 = SilentlyAnswerable(FakeQuestion())
        q2 = SilentlyPerformable(FakeAction())
        q3 = SilentlyResolvable(FakeResolution())

        assert isinstance(q1, Answerable)
        assert isinstance(q2, Performable)
        assert isinstance(q3, Resolvable)

    def test_not_performable(self) -> None:
        with pytest.raises(NotPerformable) as exc:
            SilentlyPerformable(None)  # type: ignore

        assert str(exc.value) == (
            "SilentlyPerformable only works with Performable. "
            "Use `Silently` instead."
        )

    def test_not_answerable(self) -> None:
        with pytest.raises(NotAnswerable) as exc:
            SilentlyAnswerable(None)  # type: ignore

        assert str(exc.value) == (
            "SilentlyAnswerable only works with Answerable. " "Use `Silently` instead."
        )

    def test_not_resolvable(self) -> None:
        with pytest.raises(NotResolvable) as exc:
            SilentlyResolvable(None)  # type: ignore

        assert str(exc.value) == (
            "SilentlyResolvable only works with Resolvable. " "Use `Silently` instead."
        )

    def test_passthru_attribute(self) -> None:
        a = FakeAction()
        a.describe.return_value = "Happy Thoughts"

        assert Silently(a).describe() == "Happy Thoughts"

    def test_passthru_attribute_missing(self) -> None:
        a = FakeAction()
        q = Silently(a)
        with pytest.raises(AttributeError):
            q.not_a_real_attribute_of_silent_performables()

    def test_answerable_answers(self, Tester) -> None:
        question = FakeQuestion()
        Silently(question).answered_by(Tester)

        question.answered_by.assert_called_once_with(Tester)

    def test_performable_performs(self, Tester) -> None:
        action = FakeAction()
        Silently(action).perform_as(Tester)

        action.perform_as.assert_called_once_with(Tester)

    def test_resolvable_resolves(self) -> None:
        resolution = FakeResolution()
        Silently(resolution).resolve()

        resolution.resolve.assert_called_once_with()

    def test_silently_does_not_log(self, Tester, caplog) -> None:
        """
        Confirm that when Silently is used, all beat messages inside it are not logged.
        """
        caplog.set_level(logging.INFO)

        Tester.will(Action3())

        assert [r.msg for r in caplog.records] == ["Tester tries to Action3"]


class Action1(Performable):
    @beat("{} tries to Action1")
    def perform_as(self, actor: Actor) -> None:
        actor.will(Silently(Action2()))


class Action2(Performable):
    @beat("{} tries to Action2")
    def perform_as(self, actor: Actor) -> None:
        settings.UNABRIDGED_NARRATION = True
        actor.will(Silently(See(SimpleQuestion(), IsEqualTo(True))))


class Action3(Performable):
    @beat("{} tries to Action3")
    def perform_as(self, actor: Actor) -> None:
        actor.will(Silently(Action4()))


class Action4(Performable):
    @beat("{} tries to Action4")
    def perform_as(self, actor: Actor) -> None:
        actor.will(Silently(See(SimpleQuestion(), IsEqualTo(True))))


class TestSilentlyUnabridged:
    @pytest.fixture(autouse=True)
    def setup(self):
        settings.UNABRIDGED_NARRATION = False
        yield
        settings.UNABRIDGED_NARRATION = False

    def test_kinking(self, Tester: Actor, mocker: MockerFixture) -> None:
        mock_clear = mocker.spy(the_narrator, "clear_backup")
        mock_flush = mocker.spy(the_narrator, "flush_backup")
        mock_kink = mocker.spy(the_narrator, "mic_cable_kinked")

        Tester.will(Silently(FakeAction()))

        assert mock_kink.call_count == 1
        assert mock_clear.call_count == 2
        assert mock_flush.call_count == 1

    def test_skip_creation(self) -> None:
        settings.UNABRIDGED_NARRATION = True
        fake_action = FakeAction()

        q = Silently(fake_action)

        assert q is fake_action

    def test_unabridge_from_function(
        self, Tester: Actor, mocker: MockerFixture
    ) -> None:
        settings.UNABRIDGED_NARRATION = True
        mock_clear = mocker.spy(the_narrator, "clear_backup")
        mock_flush = mocker.spy(the_narrator, "flush_backup")
        mock_kink = mocker.spy(the_narrator, "mic_cable_kinked")

        Silently(FakeAction()).perform_as(Tester)

        assert mock_kink.call_count == 0
        assert mock_clear.call_count == 0
        assert mock_flush.call_count == 0

    def test_unabridged_from_class(self, Tester: Actor, mocker: MockerFixture) -> None:
        settings.UNABRIDGED_NARRATION = True
        mock_clear = mocker.spy(the_narrator, "clear_backup")
        mock_flush = mocker.spy(the_narrator, "flush_backup")
        mock_kink = mocker.spy(the_narrator, "mic_cable_kinked")

        Tester.will(SilentlyPerformable(FakeAction()))

        assert mock_kink.call_count == 1
        assert mock_clear.call_count == 1
        assert mock_flush.call_count == 1

    def test_unabridged_set_inside_silently(self, Tester, caplog) -> None:
        """
        Confirm when unabridged flag is set, DEEP INSIDE actions which are
        wrapped in Silently, that logging will occur normally.
        """
        caplog.set_level(logging.INFO)

        Tester.will(Silently(Action1()))

        assert [r.msg for r in caplog.records] == [
            "Tester tries to Action1",
            "    Tester tries to Action2",
            "        Tester sees if simpleQuestion is equal to True.",
            "            Tester examines SimpleQuestion",
            "                => True",
            "            ... hoping it's equal to True.",
            "                => <True>",
        ]

    def test_unabridged_set_outside_silently(self, Tester, caplog) -> None:
        """
        Confirm when unabridged flag is set, logging will occur normally.
        """
        caplog.set_level(logging.INFO)
        settings.UNABRIDGED_NARRATION = True

        Tester.will(Silently(Action2()))

        assert [r.msg for r in caplog.records] == [
            "Tester tries to Action2",
            "    Tester sees if simpleQuestion is equal to True.",
            "        Tester examines SimpleQuestion",
            "            => True",
            "        ... hoping it's equal to True.",
            "            => <True>",
        ]
