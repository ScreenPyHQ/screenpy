.. _actors:

Actors
======

Actors are the do-ers in the screenplay.
Actors set the scene,
perform their hearts out,
and then make dramatic assertions
that will either see
a happy ending or a tragic failure.

More seriously,
the actors represent the users of your application,
doing the things you'd expect them to do on it
(or things you might not expect them to do).
Screenplay Pattern focuses entirely
on what your users hope to do on your site,
so your test cases will focus on what the actors do,
which includes using :ref:`abilities`
to perform :ref:`actions`
and ask :ref:`questions`.

Using Actors
------------

To instantiate a new actor,
just give it a name::

    from screenpy.actor import Actor, AnActor


    Perry = AnActor.named("Perry")

Without any abilities,
your actor will be woefully unprepared
to begin their performance.
Actors can be granted abilities like so::

    from selenium.webdriver import Firefox

    from screenpy.abilities import BrowseTheWeb


    Perry.can(BrowseTheWeb.using(Firefox()))

    # For convenience, you can also do the same like this
    Perry = AnActor.named("Perry").who_can(BrowseTheWeb.using_firefox())

Now,
Perry is able to attempt any actions
that require the ability to BrowseTheWeb.
Here's Perry attempting to click a link::

    from screenpy import Target

    from screenpy.actions import Click


    LOGIN_LINK = Target.the('"Log In" link').located_by("//a")
    Perry.attempts_to(Click.the(LOGIN_LINK))

You'll notice we had to make a quick |Target| there.
We'll get to :ref:`targets` later,
they're basically how you direct the actors
where to perform the action.

In the above example,
the action knows what ability it requires,
and it will ask the actor
to use that ability to perform the action.
If the actor does not have that ability,
the actor will raise an |UnableToPerform| exception.

After our actor has performed a few actions,
they are probably ready to ask :ref:`questions`.
Questions and resolutions are how assertions are done in ScreenPy,
like so::

    from screenpy.questions import Text
    from screenpy.resolutions import ReadsExactly


    THE_WELCOME_MESSAGE = Target.the("welcome_message").located_by("span.welcome")
    Perry.should_see_the((Text.of(THE_WELCOME_MESSAGE), ReadsExactly("Welcome!"))

That's the whole flow!
Your actor is now ready to exit::

    Perry.exits_stage_right()

Up Next
-------

The guided tour continues
on the :ref:`abilities` page!

Actor Class
-----------

.. autoclass:: screenpy.actor.Actor
    :members:
