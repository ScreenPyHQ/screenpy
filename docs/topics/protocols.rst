.. _protocols:

Protocols
=========

ScreenPy uses Protocols
to enable "structure subclassing."
This means
a Question is only a Question
if it is ``Answerable``,
for example.

Note that :ref:`resolutions`
are the exception
to this subclassing strategy.
They use traditional inheritance
to take advantage of |PyHamcrest|'s matchers.

The following Protocols describe
Actions,
Abilities,
and Questions
through the methods they need.

.. module:: screenpy.protocols

Abilities
---------

.. autoclass:: Forgettable
    :members:

Actions
-------

.. autoclass:: Performable
    :members:

.. autoclass:: Chainable
    :members:

Questions
---------

.. autoclass:: Answerable
    :members:

