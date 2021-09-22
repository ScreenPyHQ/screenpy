.. _narrator:

Narrator
========

Telling the story
of your actors' screenplay
falls to the Narrator.

You can fit the Narrator's microphone
with adapters
to send the thrilling account
to different reporting tools.
Currently,
ScreenPy includes adapters for
`Allure <https://docs.qameta.io/allure/>`__
and stdout.

Using Adapters
==================

To include adapters
on the Narrator's microphone,
do this::

    from screenpy.narration.adapters.stdout_adapter import StdOutAdapter
    from screenpy.pacing import the_narrator

    the_narrator.adapters = [StdOutAdapter()]

Do the above in ``conftest.py``
or a similar setup file
to set the adapters
for your test suite.
You are able to
add any number of adapters
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

AllureAdapter
-------------

.. autoclass:: screenpy.narration.adapters.allure_adapter.AllureAdapter
    :members:


StdOutAdapter
-------------

.. autoclass:: screenpy.narration.adapters.stdout_adapter.StdOutAdapter
    :members:
