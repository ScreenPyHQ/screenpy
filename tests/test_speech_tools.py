from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

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


class TestRepresentProp:
    def test_str(self) -> None:
        val = "hello\nworld!"

        assert represent_prop(val) == "'hello\\nworld!'"

    def test_int(self) -> None:
        val = 1234

        assert represent_prop(val) == "<1234>"
