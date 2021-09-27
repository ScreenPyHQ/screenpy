import pytest

from screenpy.speech_tools import get_additive_description


class ThisIsAPerformableWithADescribe:
    def perform_as(self):
        pass

    def describe(self):
        return "This is a performable."


class ThisIsAPerformable:
    def perform_as(self):
        pass


@pytest.mark.parametrize(
    "performable", [ThisIsAPerformable(), ThisIsAPerformableWithADescribe()]
)
def test_get_additive_description(performable):
    description = get_additive_description(performable)

    assert description == "this is a performable"
