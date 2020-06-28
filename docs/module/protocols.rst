.. _protocols:

Protocols
=========

ScreenPy uses Protocols
to enable "structure subclassing,"
which is to say that
a Question is only a Question
if it is Answerable,
for example.

Note that :ref:`resolutions`
are the exception
to this subclassing strategy,
as they use traditional inheritance
to take advantage of |PyHamcrest|'s matchers.

The following Protocols
describe Actions,
Abilities,
and Questions
through the methods
they are required to implement.

Abilities
---------

.. autoclass:: screenpy.protocols.Forgettable
    :members:

Actions
-------

.. autoclass:: screenpy.protocols.Performable
    :members:

.. autoclass:: screenpy.protocols.Chainable
    :members:

Questions
---------

.. autoclass:: screenpy.protocols.Answerable
    :members:

