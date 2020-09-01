.. _exceptions:

Exceptions
==========

There are several exceptions
thrown about in ScreenPy.
Mostly they are used to provide extra context
when other exceptions are raised.

.. module:: screenpy.exceptions

Base
^^^^

.. autoclass:: ScreenPyError

Ability Exceptions
^^^^^^^^^^^^^^^^^^

.. autoclass:: AbilityError
.. autoclass:: BrowsingError

Action Exceptions
^^^^^^^^^^^^^^^^^

.. autoclass:: ActionError
.. autoclass:: DeliveryError
.. autoclass:: UnableToAct

Actor Exceptions
^^^^^^^^^^^^^^^^

.. autoclass:: UnableToPerform

Question Exceptions
^^^^^^^^^^^^^^^^^^^

.. autoclass:: UnableToAnswer

Target Exceptions
^^^^^^^^^^^^^^^^^

.. autoclass:: TargetingError
