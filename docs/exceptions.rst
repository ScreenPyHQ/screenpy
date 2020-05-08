.. _exceptions:

Exceptions
==========

There are several exceptions
thrown about in ScreenPy.
Mostly they are used to provide extra context
when other exceptions are raised.

Base
^^^^
.. autoclass:: screenpy.exceptions.ScreenPyError

Ability Exceptions
^^^^^^^^^^^^^^^^^^
.. autoclass:: screenpy.exceptions.AbilityError
.. autoclass:: screenpy.exceptions.BrowsingError

Action Exceptions
^^^^^^^^^^^^^^^^^
.. autoclass:: screenpy.exceptions.ActionError
.. autoclass:: screenpy.exceptions.DeliveryError
.. autoclass:: screenpy.exceptions.UnableToAct

Actor Exceptions
^^^^^^^^^^^^^^^^
.. autoclass:: screenpy.exceptions.UnableToPerform

Target Exceptions
^^^^^^^^^^^^^^^^^
.. autoclass:: screenpy.exceptions.TargetingError
