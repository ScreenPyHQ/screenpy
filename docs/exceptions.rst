.. _exceptions:

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
