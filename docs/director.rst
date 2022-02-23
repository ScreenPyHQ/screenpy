========
Director
========

Every screenplay has a director,
and ScreenPy is no different.
ScreenPy has exactly one Director
who is in charge of taking notes.

Using the Director
==================

The Director will not be used directly,
usually.
The Director is used
in the :class:`~screenpy.actions.MakeNote` Action,
and may be used in custom Actions
or future Actions as well.
If you do find yourself
needing to talk to the Director,
See :ref:`calling the director` below.

Whenever your Actors make a note,
it is the Director
who keeps track of it.

To look up a note,
use the :func:`~screenpy.directions.noted_under` Direction.
You can use it *anywhere*
(with only one :ref:`limitation <makenote gotcha>`)::

    given(Perry).was_able_to(
        MakeNote.of_the(Text.of_the(GENERATED_KEYCODE)).as_("keycode"),
        GoToLockedGate(),
    )
    when(Perry).attempts_to(
        Enter.the_text(noted_under("keycode")).into_the(KEYCODE_INPUT),  # <- with Actions!
        Wait.for_the(GENERATE_NEW_KEYCODE_BUTTON).to_appear(),
        Click.on_the(GENERATE_NEW_KEYCODE_BUTTON),
    )

    then(Perry).should(
        See.the(
            Text.of_the(GENERATED_KEYCODE),
            DoesNot(ContainTheText(noted_under("keycode")),  # <- with Resolutions!
        ),
    )

As you can see,
the Director never appears in our screenplay,
but is always behind the scenes.

.. _calling the director:

Calling the Director
====================

There is only one Director,
represented by a singleton class.
Thus,
if you need the Director,
all you need to do
is call them,
like ``Director()``.

For example,
this is from the source
of the :class:`~screenpy.actions.MakeNote` Action::

    Director().notes(self.key, value)

Director Class
==============

.. autoclass:: screenpy.director.Director
    :members:

.. _directions:

Included Directions
===================

.. automodule:: screenpy.directions
    :members:
