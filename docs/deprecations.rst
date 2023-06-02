============
Deprecations
============

This page documents
the major deprecations
in ScreenPy's life,
and how to adjust your tests
to keep them up to date.

4.2.0 Deprecations
==================

BaseResolution Deprecation
--------------------------

:class:`~screenpy.resolutions.base_resolution.BaseResolution` is now deprecated.

For a long time,
``BaseResolution`` was an odd duck.
All the other pieces of ScreenPy are some sort of -able:
Performable.
Answerable.
Describable.
Resolutions,
though,
were some strange inheritance.

Not anymore!
Now Resolutions are :class:`~screenpy.protocols.Resolvable`!
This hopefully makes them easier to understand.

Please update your custom Resolutions by making them Resolvable.
Here is an example of :class:`~screenpy.resolutions.IsEqualTo`
before and after this change.

Before::

    from typing import TypeVar

    from hamcrest import equal_to
    from hamcrest.core.core.isequal import IsEqual

    from .base_resolution import BaseResolution

    T = TypeVar("T")


    class IsEqualTo(BaseResolution):
        """Match on an equal object.

        Examples::
            the_actor.should(
                See.the(Number.of(ADVERTISEMENT_BANNERS), IsEqualTo(0))
            )
        """

        matcher: IsEqual
        line = "equal to {expectation}"
        matcher_function = equal_to

        def __init__(self, obj: T) -> None:
            super().__init__(obj)

After::

    from typing import Any

    from hamcrest import equal_to
    from hamcrest.core.matcher import Matcher

    from screenpy.pacing import beat


    class IsEqualTo:
        """Match on an equal object.

        Examples::

            the_actor.should(
                See.the(Number.of(ADVERTISEMENT_BANNERS), IsEqualTo(0))
            )
        """

        def describe(self) -> str:
            """Describe the Resolution's expectation."""
            return f"Equal to {self.expected}."

        @beat("... hoping it's equal to {expected}.")
        def resolve(self) -> Matcher[Any]:
            """Produce the Matcher to make the assertion."""
            return equal_to(self.expected)

        def __init__(self, obj: Any) -> None:
            self.expected = obj

Actor.has_cleanup_tasks Removed
-------------------------------

This method was deprecated in 4.0.1,
and is removed as of 4.2.0.
(Sorry for not mentioning it here yet!)

If you used this method,
you can use :meth:`~screenpy.actor.Actor.has_ordered_cleanup_tasks` instead
as a drop-in replacement,
or :meth:`~screenpy.actor.Actor.has_independent_cleanup_tasks`
if the tasks can be executed
without ensuring they are successful.

4.0.0 Breaking Changes
======================

Hoo boy.
This was the big one.
This version split ScreenPy
into one "core" module
and several extension modules.
The extensions were divided
based on :ref:`Abilities`.

This change was necessary
because ScreenPy is growing.
As ScreenPy supports more and more tools,
collisions are starting to happen,
and the package is getting bigger.
Plus,
this approach makes it clear
how extensible ScreenPy is,
and how to go about extending it!

Upgrading to this version
will see you first install ScreenPy
slightly differently.
To get the same features,
your install will change like this:

``pip install screenpy``

⇩ to

``pip install screenpy[selenium,requests,allure]``

Then,
your ``import`` statements
will also need to be updated::

    # ⇩ before

    from screenpy.abilities import BrowseTheWeb, MakeAPIRequests
    from screenpy.actions import Click, See, SendGETRequest
    from screenpy.questions import BodyOfTheLastResponse, Text

    # ⇩ after

    from screenpy_requests.abilities import MakeAPIRequests
    from screenpy_selenium.abilities import BrowseTheWeb
    from screenpy.actions import See
    from screenpy_requests.actions import SendGETRequest
    from screenpy_selenium.actions import Click
    from screenpy_requests.questions import BodyOfTheLastResponse
    from screenpy_selenium.questions import Text

Finally,
you'll need to add
the new ``AllureAdapter``
to the :ref:`Narrator <narrator api>`
somewhere near the beginning of the tests.
In ``pytest``,
you can do this
in the feature-level ``conftest.py`` file::

    from screenpy.pacing import the_narrator
    from screenpy_adapter_allure import AllureAdapter

    the_narrator.attach_adapter(AllureAdapter())

3.1.0 Deprecations
==================

3.1.0 deprecated
the ``should_see_the`` and ``should_see_any_of`` methods
of the :class:`~screenpy.actor.Actor` class
in favor of
the new :meth:`~screenpy.actor.Actor.should` method and
the new :class:`~screenpy.actions.See`,
:class:`~screenpy.actions.SeeAllOf`,
and :class:`~screenpy.actions.SeeAnyOf` Actions.
These deprecated methods are removed
in 4.0.0.

To adjust your tests,
change ``should_see_the``
to ``should``,
and place a :class:`~screenpy.actions.See`
before each Question and Resolution tuple.
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
of Question and Resolution tuples::

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

1.0.0 Deprecations
==================

1.0.0 deprecated
the ``.then_wait_for()`` and ``.then_wait_for_the()`` methods
of both the Click and Enter Actions
in favor of
the new Wait Action.
These deprecated methods are removed
in 2.0.0.

To adjust your tests,
remove the call to ``then_wait_for_the``
or ``then_wait_for``.
Take the Target
that was previously passed in to that method
and give it to Wait.
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
