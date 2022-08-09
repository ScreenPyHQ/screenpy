from typing_extensions import Protocol

from screenpy.protocols import (
    Answerable,
    Describable,
    ErrorKeeper,
    Forgettable,
    Performable,
)


class Question(Answerable, Describable, Protocol):
    ...


class ErrorQuestion(Answerable, Describable, ErrorKeeper, Protocol):
    ...


class Action(Performable, Describable, Protocol):
    ...


class Ability(Forgettable, Protocol):
    ...
