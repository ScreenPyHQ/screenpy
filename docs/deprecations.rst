.. _deprecations:

Deprecations
============

This page documents
the major deprecations
in ScreenPy's life,
and how to adjust your tests
to keep them up to date.

1.0.0 Deprecations
------------------

1.0.0 deprecated
the ``.then_wait_for()`` and ``.then_wait_for_the()`` methods
of both the :class:`~screenpy.actions.Click` and :class:`~screenpy.actions.Enter` Actions
in favor of
the new :class:`~screenpy.actions.Wait` Action.
These deprecated methods are removed
in 2.0.0.

To adjust your tests,
remove the call to ``then_wait_for_the``
or ``then_wait_for``.
Take the Target
that was previously passed in to that method
and give it to :class:`~screenpy.actions.Wait`.
Here's an example::

    # ⇩ before

    Perry.attempts_to(
        # ...
        Click.on_the(LOGIN_LINK).then_wait_for_the(USERNAME_FIELD),
        # ...
    )

    # ⇩ after

    Perry.attempts_to(
        # ...
        Click.on_the(LOGIN_LINK),
        Wait.for_the(USERNAME_FIELD).to_appear(),
        # ...
    )

3.1.0 Deprecations
------------------

3.1.0 deprecated
the ``should_see_the`` and ``should_see_any_of`` methods
of the :class:`~screenpy.actor.Actor` class
in favor of
the new :meth:`~screenpy.actor.Actor.should` method and
the new :class:`~screenpy.actions.See`
and :class:`~screenpy.actions.SeeAnyOf` Actions.
These deprecated methods are removed
in 4.0.0.

To adjust your tests,
change ``should_see_the``
to ``should``,
and place a :class:`~screenpy.actions.See`
before each |Question| and |Resolution| tuple.
You can instead use a single :class:`~screenpy.actions.SeeAllOf`
before the list of tuples,
if it suits you::

    # ⇩ before

    Perry.should_see_the(
        (Text.of_the(WELCOME_BANNER), ReadsExactly("Welcome!")),
        (Element(CONFETTI), IsVisible()),
    )

    # ⇩ after

    Perry.should(
        See.the(Text.of_the(WELCOME_BANNER), ReadsExactly("Welcome!")),
        See.the(Element(CONFETTI), IsVisible()),
    )

    # ... or with SeeAllOf

    Perry.should(
        SeeAllOf.the(
            (Text.of_the(WELCOME_BANNER), ReadsExactly("Welcome!")),
            (Element(CONFETTI), IsVisible()),
        ),
    )

For ``should_see_any_of``,
change to ``should``
and place a :class:`~screenpy.actions.SeeAnyOf` Action
before the list
of |Question| and |Resolution| tuples::

    # ⇩ before

    Perry.should_see_any_of(
        (Number.of(BALLOONS), IsEqualTo(3)),
        (Number.of(BALLOONS), IsEqualTo(4)),
        (Number.of(BALLOONS), IsEqualTo(5)),
    )

    # ⇩ after

    Perry.should(
        SeeAnyOf.the(
            (Number.of(BALLOONS), IsEqualTo(3)),
            (Number.of(BALLOONS), IsEqualTo(4)),
            (Number.of(BALLOONS), IsEqualTo(5)),
        ),
    )
