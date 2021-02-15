.. _actors:

Actors
======


Actors are the do-ers in the screenplay.
Actors set the scene,
perform their hearts out,
and then make dramatic assertions.

Taking my tongue out of my cheek,
actors represent the users of your application.
Screenplay Pattern places the focus
on what your users want to do,
so actors are the drivers of your test cases.

Using Actors
------------

To instantiate a new actor,
give it a name::

    from screenpy.actor import Actor, AnActor


    Perry = AnActor.named("Perry")

Without any abilities,
your actor will be woefully unprepared
to begin their performance.
Grant abilities to your actors like so::

    from selenium.webdriver import Firefox

    from screenpy.abilities import BrowseTheWeb


    Perry.can(BrowseTheWeb.using(Firefox()))

    # For convenience, you can also do the same during instantiation
    Perry = AnActor.named("Perry").who_can(BrowseTheWeb.using_firefox())

Now,
Perry is able to attempt any actions
which need the ability to |BrowseTheWeb|.
Here's Perry attempting to click a link::

    from screenpy import Target

    from screenpy.actions import Click


    LOGIN_LINK = Target.the('"Log In" link').located_by("//a")
    Perry.attempts_to(Click.the(LOGIN_LINK))

You'll notice we had to make a quick ``LOGIN_LINK`` |Target| there.
We'll get to :ref:`targets` later;
they're how you direct the actors
where to perform the action.

All actions know what ability they need,
and the actor must use that ability
to perform them.
If the actor is lacking,
they will raise an |UnableToPerform| exception.

After our actor has set the stage,
they are ready to ask :ref:`questions`.
Questions and resolutions
are how to make assertions in ScreenPy,
like so::

    from screenpy.questions import Text
    from screenpy.resolutions import ReadsExactly


    THE_WELCOME_MESSAGE = Target.the("welcome_message").located_by("span.welcome")
    Perry.should_see_the((Text.of(THE_WELCOME_MESSAGE), ReadsExactly("Welcome!"))

That's the whole flow!
Our Actor has successfully performed their screenplay.
Perry is now ready to exit::

    Perry.exits_stage_right()

Up Next
-------

The guided tour continues
on the :ref:`abilities` page!

Actor Class
-----------

.. autoclass:: screenpy.actor.Actor
    :members:
