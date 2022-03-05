=====
Tasks
=====

Tasks are a grouping of Actions.
They are :class:`~screenpy.protocols.Performable`,
just like Actions,
which means they have
a ``perform_as`` method.
That is the only requirement.

You can create Tasks
for a repeated group of Actions,
like ``LogIn``.
You can also create Tasks
to describe a group of Actions
you only perform once
with a more descriptive name,
like ``ChangeProfilePicture``.

There were two Tasks used
in our :ref:`Complete Example`:
``CutToCloseUp`` and ``DollyZoom``.
Let's look at how ``DollyZoom``
might be implemented::

    from screenpy import Actor
    from screenpy.pacing import beat

    from ..actions import Dolly, Simultaneously, Zoom


    class DollyZoom:
        """Perform a dolly zoom (optionally on a character) to enhance drama.

        Examples::

            the_actor.attempts_to(DollyZoom())

            the_actor.attempts_to(DollyZoom.on("Alfred Hitchcock"))
        """

        @staticmethod
        def on(character: str) -> "DollyZoom":
            """Specify the character to put in frame before dolly zooming."""
            return DollyZoom(character)

        @beat("{} executes a thrilling dolly zoom{detail}!")
        def perform_as(self, the_actor: Actor) -> None:
            """Direct the actor to dolly zoom on their camera."""
            if self.character:
                zoom = Zoom.in_().on(self.character)
            else:
                zoom = Zoom.in_()

            the_actor.attempts_to(
                Simultaneously(
                    Dolly.backwards(),
                    zoom,
                ),
            )

        def __init__(self, character: Optional[str] = None) -> None:
            self.character = character
            self.detail = f" on {character}" if character else ""


As you can see,
this Task simply performs
three other Actions.
``Simultaneously``,
a ``cam_py`` Action
which performs all given Actions at once;
``Dolly``,
which moves the camera
in the direction specified;
and ``Zoom``,
which zooms the camera in or out.

The :func:`~screenpy.pacing.beat` lines
for each action
will be read out
by the Narrator.
The ``DollyZoom`` Task's line
will appear to encapsulate
the other Actions' lines,
something like this:

    Cameron executes a thrilling dolly zoom on Frieda!
        Cameron performs a complicated feat of simultaneous actions:
            Cameron dollies the camera backwards.
            Cameron zooms in on Frieda.

Where to Go from Tasks
======================

* :ref:`narrator`
