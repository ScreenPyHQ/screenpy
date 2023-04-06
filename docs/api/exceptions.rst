==========
Exceptions
==========

There are several exceptions
thrown about in ScreenPy.
In general,
they provide extra context
after catching other,
less descriptive exceptions.

.. module:: screenpy.exceptions

Base
----

.. autoclass:: ScreenPyError
.. autoclass:: ResolutionError
.. autoclass:: QuestionError

Ability Exceptions
------------------

.. autoclass:: AbilityError

Action Exceptions
-----------------

.. autoclass:: ActionError
.. autoclass:: DeliveryError
.. autoclass:: NotPerformable
.. autoclass:: UnableToAct

Actor Exceptions
----------------

.. autoclass:: UnableToPerform

Director Exceptions
-------------------

.. autoclass:: UnableToDirect

Narrator Exceptions
-------------------

.. autoclass:: UnableToNarrate


Question Exceptions
-------------------

.. autoclass:: NotAnswerable
.. autoclass:: UnableToAnswer

Resolution Exceptions
---------------------

.. autoclass:: NotResolvable
.. autoclass:: UnableToFormResolution
