from typing import Protocol, runtime_checkable

from screenpy.protocols import (
    Answerable,
    Describable,
    ErrorKeeper,
    Forgettable,
    Performable,
    Resolvable,
)


@runtime_checkable
class Question(Answerable, Describable, Protocol): ...


@runtime_checkable
class ErrorQuestion(Answerable, Describable, ErrorKeeper, Protocol): ...


@runtime_checkable
class Action(Performable, Describable, Protocol): ...


@runtime_checkable
class Ability(Forgettable, Protocol): ...


@runtime_checkable
class Resolution(Resolvable, Describable, Protocol): ...
