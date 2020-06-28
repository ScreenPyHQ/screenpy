.. _abilities:

Abilities
=========

Abilities allow your |Actor| to **do** things.
Actors will leverage their abilities
to perform actions
that require those abilities.

Using Abilities
---------------

To grant an Actor an ability,
pass it in using the Actor's |Actor.who_can|
or |Actor.can|
methods::

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
that the actor does not have,
the actor will raise an |UnableToPerform|.

Writing New Abilities
---------------------

There may be other abilities your actors need to possess
in order to test your application.
You are encouraged to write your own!
The only prescribed method for an ability
is the ``forget`` method,
which will complete any cleanup required.
For an example,
see the |BrowseTheWeb.forget| method
of the BrowseTheWeb ability.

Included Abilities
------------------

BrowseTheWeb
^^^^^^^^^^^^

.. autoclass:: screenpy.abilities.browse_the_web.BrowseTheWeb
    :members:

AuthenticateWith2FA
^^^^^^^^^^^^^^^^^^^

.. autoclass:: screenpy.abilities.authenticate_with_2fa.AuthenticateWith2FA
    :members:
