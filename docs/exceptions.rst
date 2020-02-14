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
.. autoclass:: screenpy.abilities.browse_the_web.BrowsingError

Action Exceptions
^^^^^^^^^^^^^^^^^
.. autoclass:: screenpy.exceptions.ActionError
.. autoclass:: screenpy.exceptions.DeliveryError
.. autoclass:: screenpy.exceptions.UnableToActError

Actor Exceptions
^^^^^^^^^^^^^^^^
.. autoclass:: screenpy.actor.UnableToPerformError

Target Exceptions
^^^^^^^^^^^^^^^^^
.. autoclass:: screenpy.target.TargetingError
