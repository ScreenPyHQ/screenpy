from __future__ import annotations

from typing import TYPE_CHECKING
from unittest import mock

import pytest
from hamcrest import equal_to, instance_of

from screenpy import Silently
from screenpy.configuration import ScreenPySettings
from screenpy.speech_tools import get_additive_description, represent_prop

if TYPE_CHECKING:
    from screenpy import Describable


class ThisIsADescribableWithADescribe:
    def perform_as(self) -> None:
        pass

    def describe(self) -> str:
        return "This is a describable."


class ThisIsADescribable:
    def perform_as(self) -> None:
        pass


class DescribableWithQuote:
    def perform_as(self) -> None:
        pass

    def describe(self) -> str:
        return 'This Describable ends with a "quote".'


class Indescribable:
    def describe(self) -> None:
        "Intentionally returning None."


class TestGetAdditiveDescription:
    settings_path = "screenpy.actions.silently.settings"

    @pytest.mark.parametrize(
        "describable", [ThisIsADescribable(), ThisIsADescribableWithADescribe()]
    )
    def test_get_description(self, describable: Describable) -> None:
        description = get_additive_description(describable)

        assert description == "this is a describable"

    def test_ending_with_quotes(self) -> None:
        description = get_additive_description(DescribableWithQuote())

        assert description == 'this Describable ends with a "quote"'

    def test_describe_value(self) -> None:
        description = get_additive_description("this is just a string!")

        assert description == "the str"

    def test_indescribable(self) -> None:
        description = get_additive_description(Indescribable())

        assert description == "something indescribable"

    def test_silent(self) -> None:
        mock_settings = ScreenPySettings(UNABRIDGED_NARRATION=False)
        with mock.patch(self.settings_path, mock_settings):
            val = get_additive_description(Silently(ThisIsADescribable()))

        assert val == ""

    def test_not_silent(self) -> None:
        mock_settings = ScreenPySettings(UNABRIDGED_NARRATION=True)
        with mock.patch(self.settings_path, mock_settings):
            val = get_additive_description(Silently(ThisIsADescribable()))

        assert val == "this is a describable"


class FancyObj:
    def __str__(self) -> str:
        return "<FancyObj>"


class TestRepresentProp:
    def test_str(self) -> None:
        val = "hello\nworld!"

        assert represent_prop(val) == "'hello\\nworld!'"

    def test_int(self) -> None:
        val = 1234

        assert represent_prop(val) == "<1234>"

    def test_mock(self) -> None:
        val = mock.Mock()

        assert represent_prop(val) is val

    def test_gtlt_object(self) -> None:
        val = FancyObj()

        assert represent_prop(val) == "<FancyObj>"

    def test_hamcrest_equal_to(self) -> None:
        val = equal_to(1)

        assert represent_prop(val) == "<1>"

    def test_hamcrest_instance_of(self) -> None:
        val = instance_of(int)

        assert represent_prop(val) == "an instance of int"
