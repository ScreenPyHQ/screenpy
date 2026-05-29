=========
Narration
=========

Telling the story
of your actors' screenplay
falls to the Narrator.
The Narrator is responsible
for describing the scene,
marking the tests,
and attaching files.

You can fit the Narrator's microphone with adapters
to send the thrilling account
to different reporting tools.
The default Adapter
provided with ScreenPy
logs to ``stdout``.
There may be more Adapters available
in the :ref:`official extensions` section.

Describing Your Tests and Tasks
===============================

ScreenPy uses decorators
to categorize tests
and narrate actions.


``act`` and ``scene``
---------------------

These two decorators
can be used to categorize tests.
Use them in any way
that makes sense for your team,
but :ref:`act <Act>`
is usually meant
for designating suite-level organization,
while :ref:`scene <Scene>`
is meant for smaller groupings.

``beat``
--------

A :ref:`beat` marks and describes
an Action your Actor is performing
or a Question your Actor is asking.
In other words,
it marks a test step.

Performables and Answerables
might reference other
Performables and Answerables
in their execution.

``aside``
---------

:ref:`Asides <aside>` speak a line
directly to the adapters.
Use these to add a quick comment
to the report.

Built-In StdOutAdapter
======================

The default :ref:`StdOutAdapter`
logs its narration
to ``stdout``.
You can see the full output
by following the instructions
for the `ReadTheDocs example <https://github.com/ScreenPyHQ/screenpy_examples/tree/trunk/screenpy/readthedocs>`_
in the `ScreenPy Examples <https://github.com/ScreenPyHQ/screenpy_examples>`_ collection,
but here's just the output
from the ``test_dramatic_moment`` test
in the :ref:`Complete Example`::

    features/test_mood.py::test_dramatic_moment
    ----- live log setup -----
    INFO     screenpy:stdout_adapter.py:42 Cameron arrives on stage!
    INFO     screenpy:stdout_adapter.py:42 Polly gets over their stagefright!
    ----- live log call -----
    INFO     screenpy:stdout_adapter.py:42 Cameron starts recording on Will.
    INFO     screenpy:stdout_adapter.py:42 Cameron skips to scene #35.
    INFO     screenpy:stdout_adapter.py:42 Cameron dollies the active camera left.
    INFO     screenpy:stdout_adapter.py:42 Cameron cuts to a closeup on Will!
    INFO     screenpy:stdout_adapter.py:42     Cameron zooms in.
    INFO     screenpy:stdout_adapter.py:42     Cameron jumps to the camera on Will!
    INFO     screenpy:stdout_adapter.py:42 Cameron executes a dramatic dolly zoom!
    INFO     screenpy:stdout_adapter.py:42     Cameron performs some thrilling camerawork simultaneously!
    INFO     screenpy:stdout_adapter.py:42         Cameron dollies the active camera backward.
    INFO     screenpy:stdout_adapter.py:42         Cameron zooms in.
    INFO     screenpy:stdout_adapter.py:42 Polly sees if audience tension is a palpable tension!.
    INFO     screenpy:stdout_adapter.py:42     ... hoping it's a palpable tension!
    INFO     screenpy:stdout_adapter.py:42         => True
    PASSED
    ----- live log teardown -----
    INFO     screenpy:stdout_adapter.py:42 Cameron stops recording.

The above is what logging looks like
when using ``pytest``
along with the ``--log-cli-level=info`` option.

Using Adapters
==============

To include Adapters
on the Narrator's microphone,
do this::

    from screenpy import StdOutAdapter, the_narrator

    the_narrator.attach_adapter(StdOutAdapter())

Do the above in ``conftest.py``
or a similar setup file
to set the Adapters
for your test suite.
You are able to
add any number of Adapters
in any order.

Creating New Adapters
=====================

For any The :class:`~screenpy.protocols.Adapter` protocol
describes what an adapter looks like.

Each adapter must implement
``act``, ``scene``, ``beat``, and ``aside``.
These methods are **generators**:
they receive a function (and a description line),
do whatever setup they need,
``yield`` the function back
(possibly wrapped),
and then perform teardown
after the ``yield``.

The ``error`` method
is called when an exception occurs
during a beat,
and ``attach`` is called
when a file needs to be included
in the report.

Here is a minimal example —
a ``PlaybillAdapter`` that prints
each narration in the style
of a theatrical playbill:

.. code-block:: python

    from __future__ import annotations

    from collections.abc import Generator
    from functools import wraps
    from pathlib import Path
    from typing import Any, Callable


    class PlaybillAdapter:
        """Print narrations like a playbill program."""

        def act(
            self, func: Callable, line: str, gravitas: str | None = None,
        ) -> Generator:
            """Announce the Act in grand fashion."""

            # Setup: nothing special needed for acts.

            @wraps(func)
            def func_wrapper(*args, **kwargs):
                # Print when the wrapped function is called,
                # so the timing matches the real execution.
                print(f"{'=' * 40}")
                print(f"  ACT: {line.upper()}")
                print(f"{'=' * 40}")
                return func(*args, **kwargs)

            yield func_wrapper

            # Teardown: nothing to clean up.

        def scene(
            self, func: Callable, line: str, gravitas: str | None = None,
        ) -> Generator:
            """Announce the Scene."""

            @wraps(func)
            def func_wrapper(*args, **kwargs):
                print(f"\n--- Scene: {line.title()} ---")
                return func(*args, **kwargs)

            yield func_wrapper

        def beat(
            self, func: Callable, line: str, gravitas: str | None = None,
        ) -> Generator:
            """Print the beat, then yield the original function."""

            def func_context() -> Generator:
                """The context manager for the beat."""
                # Print the beat line when the context is entered.
                print(f"  '{line}")
                yield
                # After the beat's context closes, which prints sub-beats,
                # print the line closer.
                # This will look like:
                #    '{line and any lines from sub-beats},' said the character.
                print(",' said the character.")

            with func_context():
                yield func

        def aside(
            self, func: Callable, line: str, gravitas: str | None = None,
        ) -> Generator:
            """Whisper an aside in parentheses."""

            def func_context() -> Generator:
                """The context manager for the aside."""
                print(f"    ({line})")
                yield

            with func_context():
                yield func

        def error(self, exc: Exception) -> None:
            """React to a mishap on stage (an execution error)."""
            print(f"  !! STAGECRAFT ERROR: {exc}")

        def attach(self, filepath: Path | str, **kwargs: Any) -> None:
            """Mention a "prop" (attached file)."""
            print(f"  [See prop with tag: {filepath}]")

See comments in ``act`` and ``beat``
for explanations of the timing of the narration
between the wrapper style
and the yield style

A few things to note:

* ``act`` and ``scene``
wrap the function
so the announcement is printed
when the function is actually *called*,
not when the decorator runs.
``beat`` and ``aside``
print immediately
because they run inside a ``with`` block
which already has the right timing.

* Every generator method
must ``yield`` exactly once.
Code before the ``yield`` is setup;
code after is teardown.

* The function signatures
must match the protocol exactly,
even if your adapter ignores some of the parameters.

* ``attach`` receives a filepath
(as a string or ``Path``)
and optional keyword arguments.
Pass any adapter-specific arguments as keyword arguments,
so other adapters can ignore them.
