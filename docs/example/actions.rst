.. _actions:

=======
Actions
=======

During a test,
your Actors will perform
several Actions.
Actors perform Actions
in order to set up
and perform the test.

In our :ref:`Complete Example`,
Cameron used several Actions.
One of them was ``StartRecording``.
Here is how that Action
might be coded::

    from cam_py import Camera
    from screenpy import Actor
    from screenpy.exceptions import UnableToAct
    from screenpy.pacing import beat

    from ..abilities import ControlCameras


    class StartRecording:
        """Starts recording on one or more cameras.

        Examples::

            the_actor.attempts_to(StartRecording())

            camera = Camera("Character")
            the_actor.attempts_to(StartRecording.on(camera))

            camera1 = Camera("Character1")
            camera2 = Camera("Character2")
            the_actor.attempts_to(StartRecording.on(camera1).and_(camera2))
        """

        def on(self, camera: Camera) -> "StartRecording":
            """Record on an already-created camera."""
            self.cameras.append(camera)
            return self

        and_ = on

        @beat("{} starts recording on {cameras_to_log}.")
        def perform_as(self, the_actor: Actor) -> None:
            """Direct the actor to start recording on their cameras."""
            if not self.cameras:
                raise UnableToAct("No cameras were provided!")

            control_cameras = the_actor.ability_to(ControlCameras)
            for camera in self.cameras:
                campy_session.add_camera(camera)

        @property
        def cameras_to_log(self) -> str:
            """Get a nice list of all the cameras for the logged beat."""
            return ", ".join(self.cameras)

        def __init__(self, script: cam_py.Script) -> None:
            self.script = script
            self.cameras = []


There are a few things to note here.
The first and most important
is that all Actions are :class:`~screenpy.protocols.Performable`.
This means that all Actions
have a ``perform_as`` method.
That method is what
the Actor actually *does*.

The second noteworthy piece
is that :func:`~screenpy.pacing.beat` decoration
above ``perform_as``.
That string is what will be logged
by the Narrator.
The ``{}`` will be replaced
by the name of the Actor
who performs the Action.
Any other words
inside of curly braces
will be fished out
of the Action itself.
In the above example,
``{cameras_to_log}`` was used;
The Narrator will access
the ``cameras_to_log`` property
to fill in that spot.

You may also notice
that the ``on``/``and_`` method
returned the instance of the Action.
This is because
we first give the Actor
the full list of Actions,
*then* they will perform them.

.. note:: I keep performing the same Actions...

    Sometimes,
    we perform several Actions repeatedly.
    Some other times,
    we want to give an higher-level name
    to a group of Actions.
    Tasks are the way
    to group many Actions
    into a repeatable,
    describable routine!

    We'll discuss that further
    in the Tasks section,
    linked below.

Well now we've
performed the Actions,
how do we make an assertion?
What a great Question!

Next
====

* :ref:`tasks`
* :ref:`narrator`
* :ref:`questions`
