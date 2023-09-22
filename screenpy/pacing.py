"""
Provides decorators to group your tests into acts (features) and scenes
(cases), and provide the gravitas (severity) of those groupings. These will
run through all of the Narrator's adapters.
"""
import functools
import inspect
import re
from functools import wraps
from typing import Any, Callable, Optional

from screenpy.narration import Narrator, StdOutAdapter
from screenpy.protocols import Answerable, Resolvable

Function = Callable[..., Any]
the_narrator: Narrator = Narrator(adapters=[StdOutAdapter()])


# credit to https://stackoverflow.com/a/25959545/2532408
def get_class_that_defined_method(meth: Any) -> Optional[type]:
    """attempt to identify what class a method/function came from"""
    if isinstance(meth, functools.partial):
        return get_class_that_defined_method(meth.func)
    if inspect.ismethod(meth) or (
        inspect.isbuiltin(meth)
        and getattr(meth, "__self__", None) is not None
        and getattr(meth.__self__, "__class__", None)
    ):
        for cls in inspect.getmro(meth.__self__.__class__):
            if meth.__name__ in cls.__dict__:
                return cls
        # fallback to __qualname__ parsing
        meth = getattr(meth, "__func__", meth)
    if inspect.isfunction(meth):
        cls2 = getattr(
            inspect.getmodule(meth),
            meth.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0],
            None,
        )
        if isinstance(cls2, type):
            return cls2
    # handle special descriptor objects
    return getattr(meth, "__objclass__", None)


def function_attached_to_protocol(func: Function) -> bool:
    """
    determine if function is attached to one of the protocols that allow for anything
    to return
    """
    cls = get_class_that_defined_method(func)
    return isinstance(cls, (Answerable, Resolvable))


def act(title: str, gravitas: Optional[str] = None) -> Callable[[Function], Function]:
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

    def decorator(func: Function) -> Function:
        with the_narrator.announcing_the_act(func, title, gravitas) as n_func:
            return n_func

    return decorator


def scene(title: str, gravitas: Optional[str] = None) -> Callable[[Function], Function]:
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

    def decorator(func: Function) -> Function:
        with the_narrator.setting_the_scene(func, title, gravitas) as n_func:
            return n_func

    return decorator


def beat(line: str, gravitas: Optional[str] = None) -> Callable[[Function], Function]:
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

    def decorator(func: Function) -> Function:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            action = args[0] if len(args) > 0 else None
            actor = args[1] if len(args) > 1 else ""
            markers = re.findall(r"\{([^\}]+)}", line)
            cues = {mark: getattr(action, mark) for mark in markers}

            completed_line = f"{line.format(actor, **cues)}"
            with the_narrator.stating_a_beat(func, completed_line, gravitas) as n_func:
                retval = n_func(*args, **kwargs)
                if retval is not None or function_attached_to_protocol(n_func):
                    aside(f"=> {retval}")
            return retval

        return wrapper

    return decorator


def aside(line: str, gravitas: Optional[str] = None) -> None:
    """A line spoken in a stage whisper to the audience (log a message).

    Args:
        line: the line spoken during this "beat" (the step description).
        gravitas: the severity for the narration of the line.
    """
    with the_narrator.whispering_an_aside(line, gravitas) as n_func:
        n_func()
