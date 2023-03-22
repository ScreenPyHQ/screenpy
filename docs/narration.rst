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

Like the :ref:`Director`,
there is only one Narrator.

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

Calling the Narrator
====================

There is only one Narrator,
represented by a singleton class.
Thus,
if you need the Narrator,
all you need to do is call them,
like ``Narrator()``.

For example,
this is how to kink the cable
on the Narrator's microphone
(which defers logging until you leave the context)::

    with Narrator().mic_cable_kinked():
       ...

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

    from screenpy.narration.adapters.stdout_adapter import StdOutAdapter
    from screenpy.narration import Narrator

    Narrator().attach_adapter(StdOutAdapter())

Do the above in ``conftest.py``
or a similar setup file
to set the Adapters
for your test suite.
You are able to
add any number of Adapters
in any order.

Creating New Adapters
=====================

The :class:`~screenpy.protocols.Adapter` protocol
describes what an adapter looks like.

The function signatures
must remain completely intact.
The new adapter's methods
must also ``yield`` back a function
for ``act``,
``scene``,
``beat``,
and ``aside``.
Most likely this will be
the function passed to it
in the first place,
having been modified in some way.

The ``attach`` function
allows the narrator
to attach a file.
Each adapter will handle this differently.
The signature only has one required argument:
the filepath.
This argument is a string,
and may or may not be a filepath,
depending on what reporting tool
the new adapter supports.
Pass any other required arguments
as keyword arguments,
so the other adapters
can ignore them.
