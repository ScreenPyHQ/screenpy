"""Decorators to mark key moments in your tests.

Provides decorators to group your tests into acts (features) and scenes
(cases), and provide the gravitas (severity) of those groupings; or markers
for moments the Narrator should narrate.
"""

from __future__ import annotations

import re
from functools import wraps
from typing import TYPE_CHECKING, Callable, TypeVar

from screenpy.narration import Narrator, StdOutAdapter
from screenpy.speech_tools import represent_prop

if TYPE_CHECKING:
    from typing_extensions import ParamSpec

    P = ParamSpec("P")
    T = TypeVar("T")

the_narrator: Narrator = Narrator(adapters=[StdOutAdapter()])


def function_should_log_none(func: Callable[P, T]) -> bool:
    """Helper function to decide when to log return values.

    Determine if function wrapped in beat should log that it returns None
    """
    if func.__annotations__ and "return" in func.__annotations__:
        anno = func.__annotations__["return"]
        return anno is not None and anno != "None"

    return False


def act(
    title: str, gravitas: str | None = None
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator to mark an "act".

    Acts are large groupings of tests, like suites or tests for an epic. You
    may have a "Smoke" act, or a "Log In" act, or a "Third" act. Think of acts
    like an Epic ticket.

    Args:
        title: the title of this act (the epic name).
        gravitas: how serious this act is (the severity level).

    Returns:
        The decorated function, which will be narrated when called.
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        with the_narrator.announcing_the_act(func, title, gravitas) as n_func:
            return n_func

    return decorator


def scene(
    title: str, gravitas: str | None = None
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator to mark a "scene".

    Scenes are smaller groupings of tests which can transcend a suite's
    directory grouping. They can be sub-groups of tests of an act, or an
    inter-act group. Think of scenes like a Feature ticket.

    Args:
        title: the title of this scene (the feature).
        gravitas: how serious this scene is (the severity level).

    Returns:
        The decorated function, which will be narrated when called.
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        with the_narrator.setting_the_scene(func, title, gravitas) as n_func:
            return n_func

    return decorator


def beat(
    line: str, gravitas: str | None = None
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator to describe a "beat" (a step in a test).

    A beat's line can contain markers for replacement via str.format(), which
    will be figured out from the properties of a decorated method's class.

    For example, if the beat line is "{} clicks on the {target}", then "{}"
    will be replaced by the Actor's name, and "{target}" will be replaced
    using the Click action's ``target`` property (e.g. ``Click.target``).

    Args:
        line: the line spoken during this "beat" (the step description).
        gravitas: the severity for the narration of the line.

    Returns:
        The decorated function, which will be narrated when called.
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            action = args[0] if len(args) > 0 else None
            actor = args[1] if len(args) > 1 else ""
            markers = re.findall(r"\{([^\}]+)}", line)
            cues = {mark: getattr(action, mark) for mark in markers}

            completed_line = f"{line.format(actor, **cues)}"
            with the_narrator.stating_a_beat(func, completed_line, gravitas) as n_func:
                retval = n_func(*args, **kwargs)
                if retval is not None or function_should_log_none(func):
                    aside(f"=> {represent_prop(retval)}")
            return retval

        return wrapper

    return decorator


def aside(line: str, gravitas: str | None = None) -> None:
    """A line spoken in a stage whisper to the audience (log a message).

    Args:
        line: the line spoken during this "beat" (the step description).
        gravitas: the severity for the narration of the line.
    """
    with the_narrator.whispering_an_aside(line, gravitas) as n_func:
        n_func()
