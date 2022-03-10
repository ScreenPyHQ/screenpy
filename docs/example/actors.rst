======
Actors
======

Actors represent your end users.
They will be granted Abilities,
perform Actions,
ask Questions,
and (hopefully) satisfy Resolutions
during the course
of your tests.

To instantiate an Actor is simple::

    Cameron = AnActor.named("Cameron")
    Polly = AnActor.named("Polly")

The name you give your Actors
will be used
to log the Actions they perform.
(See the :ref:`narrator` page for more details.)
In order to perform
more interesting Actions,
your Actor will need
some Abilities::

    # grant abilities on instantiation
    Cameron = AnActor.named("Cameron").who_can(ControlCameras())

    # or later, if you want
    Polly.can(PollTheAudience())

From our :ref:`Complete Example`,
we granted Cameron
the Ability to ``ControlCameras``
and Polly
the Ability to ``PollTheAudience``.
These Abilities
enabled our Actors
to perform several Actions.

Where to Go from Actors
=======================

* :ref:`abilities`
* :ref:`actions`
* :ref:`actor api`
