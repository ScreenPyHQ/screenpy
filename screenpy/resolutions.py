from hamcrest import *
from hamcrest.core.matcher import Matcher

from .pacing import beat, MINOR


class Resolution(Matcher):
    @beat("... hoping {motivation}", severity=MINOR)
    def matches(self, actual):
        return self.matcher.matches(actual)

    def describe_to(self, description):
        return self.matcher.describe_to(description)

    def describe_mismatch(self, item, mismatch_description):
        return self.matcher.describe_mismatch(item, mismatch_description)

    @property
    def motivation(self):
        return self


class ReadsExactly(Resolution):
    line = "to read '{},' exactly"

    def __init__(self, substring):
        self.substring = substring
        self.matcher = has_string(substring)

    def __repr__(self):
        return self.line.format(self.substring)


class ContainsTheText(Resolution):
    line = "to have '{}'"

    def __init__(self, substring):
        self.substring = substring
        self.matcher = contains_string(substring)

    def __repr__(self):
        return self.line.format(self.substring)


class IsEqualTo(Resolution):
    line = "to find {}"

    def __init__(self, obj):
        self.obj = obj
        self.matcher = equal_to(obj)

    def __repr__(self):
        return self.line.format(self.obj)


class IsNot(Resolution):
    line = "not {}"

    def __init__(self, resolution):
        self.resolution = resolution
        self.matcher = is_not(resolution)

    def __repr__(self):
        return self.line.format(self.resolution)


# Natural-language-enabling syntactic sugar
ReadExactly = ReadsExactly
ContainTheText = ContainsTheText
DoesNot = IsNot
