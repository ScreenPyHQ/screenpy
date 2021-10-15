import pytest

from screenpy.speech_tools import get_additive_description


class ThisIsADescribableWithADescribe:
    def perform_as(self):
        pass

    def describe(self):
        return "This is a describable."


class ThisIsADescribable:
    def perform_as(self):
        pass


class DescribableWithQuote:
    def perform_as(self):
        pass

    def describe(self):
        return 'This Describable ends with a "quote".'


class TestGetAdditiveDescription:
    @pytest.mark.parametrize(
        "describable", [ThisIsADescribable(), ThisIsADescribableWithADescribe()]
    )
    def test_get_description(self, describable):
        description = get_additive_description(describable)

        assert description == "this is a describable"

    def test_ending_with_quotes(self):
        description = get_additive_description(DescribableWithQuote())

        assert description == 'this Describable ends with a "quote"'

    def test_describe_value(self):
        description = get_additive_description("this is just a string!")

        assert description == "the str"
