.. _narrator:

========
Narrator
========

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
in the :ref:`extensions` section.

Using Adapters
==================

To include Adapters
on the Narrator's microphone,
do this::

    from screenpy.narration.adapters.stdout_adapter import StdOutAdapter
    from screenpy.pacing import the_narrator

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

Narrator
========

.. autoclass:: screenpy.narration.narrator.Narrator
    :members:

Adapters
========

There is one adapter included in ScreenPy,
which allows the Narrator
to reach ``stdout``.

StdOutAdapter
-------------

.. autoclass:: screenpy.narration.adapters.stdout_adapter.StdOutAdapter
    :members:
