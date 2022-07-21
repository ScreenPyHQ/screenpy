from typing_extensions import Protocol
from screenpy.protocols import Answerable, Forgettable, Performable, ErrorKeeper


class Describable(Protocol):
    def describe(self) -> str:
        ...

class Question(Answerable, Describable):
    ...

class ErrorQuestion(Answerable, Describable, ErrorKeeper):
    ...

class Action(Performable, Describable):
    ...

class Ability(Forgettable):
    ...


