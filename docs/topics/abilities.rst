.. _abilities:

Abilities
=========

Abilities allow your |Actor| to **do** things.
Actors will leverage their abilities
to perform their role in your test scripts.

Granting Abilities
------------------

To grant an Actor an ability,
pass it in using the Actor's
|Actor.who_can| or |Actor.can| methods::

    from screenpy import Actor, AnActor
    from screenpy.abilities import BrowseTheWeb


    # Add abilities on instantiation
    Perry = AnActor.named("Perry").who_can(BrowseTheWeb.using_firefox())

    # Or add abilities later
    Perry = AnActor.named("Perry")
    Perry.can(BrowseTheWeb.using_safari())

Granting an ability to an actor
allows them to perform any :ref:`actions`
or ask any :ref:`questions`
that require that ability.
If an action or a question require an ability
which the actor does not have,
the actor will raise an |UnableToPerform| exception.

Writing New Abilities
---------------------

There may be other abilities your actors need to possess
in order to test your application.
You are encouraged to write your own!
Abilities must be ``Forgettable``,
which means they must have a ``forget`` method
which cleans up after them.
See the :ref:`protocols` page for more information.

Up Next
-------

The guided tour continues
on the :ref:`targets` page!

Included Abilities
------------------

These are the abilities included in ScreenPy.

.. module:: screenpy.abilities

AuthenticateWith2FA
^^^^^^^^^^^^^^^^^^^

.. autoclass:: AuthenticateWith2FA
    :members:

BrowseTheWeb
^^^^^^^^^^^^

.. autoclass:: BrowseTheWeb
    :members:

MakeAPIRequests
^^^^^^^^^^^^^^^

.. autoclass:: MakeAPIRequests
    :members:
