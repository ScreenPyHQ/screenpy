.. _abilities:

=========
Abilities
=========

Abilities enable your Actors
to use libraries,
connect with resources,
or... well, anything!
Your Actors can then perform Actions
or ask Questions
using their Abilities.

In our :ref:`Complete Example`,
we granted Cameron the Ability
to ``ControlCameras``.
This Ability
uses a made-up library,
``cam_py``,
to control cameras.
This fictional Ability
might look like this::

    import cam_py

    class ControlCameras:
        """Enable an Actor to control cameras through cam_py.

        Examples::

            the_actor.can(ControlCameras())
        """

        def __init__(self) -> None:
            self.campy_session = cam_py.RecordingSession()
            self.cameras = []

        def forget(self) -> None:
            for camera in self.cameras:
                camera.stop()
            self.campy_session.terminate()

It is surprisingly lightweight!
Abilities should be
a sort of wallet
holding sessions,
instantiated macguffins,
and the like.

The only required method
for an Ability
is ``forget``.
This method handles
cleaning up
any dangling loose ends.

Actions and Questions
may both use an Actor's Abilities.

Next
====

* :ref:`actions`
* :ref:`questions`
