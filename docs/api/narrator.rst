============
Narrator API
============

The Narrator has several useful methods
for reporting on things of note during a test.
You may not need to use most of them directly.

.. autoclass:: screenpy.narration.narrator.Narrator
    :members:

Adapters
========

There is one adapter included in ScreenPy,
which allows the Narrator to reach ``stdout``.

StdOutAdapter
-------------

.. autoclass:: screenpy.narration.adapters.stdout_adapter.StdOutAdapter
    :members:
