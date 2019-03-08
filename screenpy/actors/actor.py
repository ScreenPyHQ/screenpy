from random import choice

from hamcrest import assert_that

from ..pacing import aside, TRIVIAL


ENTRANCE_LINES = [
    "makes their debut!",
    "is ready for their close-up!",
    "enters, stage right!",
    "hears their cue!",
    "arrives on stage!",
]


class UnableToPerformException(Exception):
    pass


class Actor(object):
    """
    Represents an actor, holding their name and abilities.
    """

    @staticmethod
    def named(name):
        aside("{} {}".format(name, choice(ENTRANCE_LINES)), severity=TRIVIAL)
        return Actor(name)

    def can(self, *abilities):
        self.abilities.extend(abilities)
        return self

    def who_can(self, *abilities):
        return self.can(*abilities)

    def ability_to(self, ability):
        for a in self.abilities:
            if isinstance(a, ability):
                return a
        else:
            raise UnableToPerformException(
                "{} cannot perform the ability {}".format(self, ability)
            )

    def uses_ability_to(self, ability):
        return self.ability_to(ability)

    def was_able_to(self, *tasks):
        return self.attempts_to(*tasks)

    def attempts_to(self, *tasks):
        for task in tasks:
            self.perform(task)

    def perform(self, task):
        task.perform_as(self)

    def should_see_that(self, *tests):
        for question, test in tests:
            assert_that(question.answered_by(self), test)

    def exit(self):
        for ability in self.abilities:
            ability.forget()
            self.abilities.remove(ability)

    def exit_stage_right(self):
        aside("{} bows and exits, stage right.".format(self), severity=TRIVIAL)
        self.exit()

    def exit_stage_left(self):
        aside("{} bows and exits, stage left.".format(self), severity=TRIVIAL)
        self.exit()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __init__(self, name):
        self.name = name
        self.abilities = []
