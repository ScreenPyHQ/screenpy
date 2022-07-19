from typing_extensions import Protocol
from screenpy.protocols import Answerable, Forgettable, Performable


class Describable(Protocol):
    def describe(self) -> str:
        ...

class Question(Answerable, Describable):
    ...

class Action(Performable, Describable):
    ...

class Ability(Forgettable):
    ...


