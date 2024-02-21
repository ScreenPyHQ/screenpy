===========
Actions API
===========

These are the Actions included in ScreenPy.

.. module:: screenpy.actions

AttachTheFile
-------------

**Aliases**: ``AttachAFile``,
``AttachFile``,
``AttachesTheFile``,
``AttachesAFile``,
``AttachesFile``

.. autoclass:: AttachTheFile
    :members:

Debug
-----

.. autoclass:: Debug
    :members:

Either
------

**Aliases**: ``Attempt``,
``AttemptTo``,
``GoFor``,
``Try``
``TryTo``,
``Attempts``,
``AttemptsTo``,
``GoesFor``,
``Tries``,
``TriesTo``

.. autoclass:: Either
    :members:
    :exclude-members: except_, else_, otherwise, alternatively, failing_that

Eventually
----------

.. autoclass:: Eventually
    :members:
    :exclude-members: trying_for_no_longer_than, trying_for, waiting_for, polling_every, trying_every

Log
---

.. autoclass:: Log
    :members:

MakeNote
--------

**Aliases**: ``TakeNote``,
``MakesNote``,
``TakesNote``

.. autoclass:: MakeNote
    :members:
    :exclude-members: of_the

Pause
-----

**Aliases**: ``Sleep``,
``Pauses``,
``Sleeps``

.. autoclass:: Pause
    :members:
    :exclude-members: second_because,

See
---

**Aliases**: ``Assert``,
``Confirm``,
``Observe``,
``Verify``,
``Sees``,
``Asserts``,
``Confirms``,
``Observes``,
``Verifies``


.. autoclass:: See
    :members:

SeeAllOf
--------

**Aliases**: ``AssertAllOf``,
``ConfirmAllOf``,
``ObserveAllOf``,
``VerifyAllOf``,
``SeesAllOf``,
``AssertsAllOf``,
``ConfirmsAllOf``,
``ObservesAllOf``,
``VerifiesAllOf``

.. autoclass:: SeeAllOf
    :members:

SeeAnyOf
--------

**Aliases**: ``AssertAnyOf``,
``ConfirmAnyOf``,
``ObserveAnyOf``,
``VerifyAnyOf``,
``SeesAnyOf``,
``AssertsAnyOf``,
``ConfirmsAnyOf``,
``ObservesAnyOf``,
``VerifiesAnyOf``

.. autoclass:: SeeAnyOf
    :members:


Silently
--------

**Aliases**: ``Quietly``

.. autofunction:: Silently
