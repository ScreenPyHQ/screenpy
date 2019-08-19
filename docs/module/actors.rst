.. _actors:

Actors
======

Actors are the do-ers in the screenplay. Actors set the scene, perform their hearts out, and then make dramatic assertions that will either see a happy ending or a tragic failure.

More seriously, the actors represent the users of your application, doing the things you'd expect them to do on it (or things you might not expect them to do). Screenplay Pattern focuses entirely on what your users hope to do on your site, so your test cases will focus on what the actors do, which includes gaining :ref:`abilities`, performing :ref:`actions`, and asking :ref:`questions`.

Using Actors
------------

To instantiate a new actor, just give it a name::

    from screenpy.actor import Actor, AnActor

    Perry = AnActor.named("Perry")

Without any abilities, your actor will be woefully unprepared to begin their performance. To give your actor an ability, you can do something like::

    from selenium.webdriver import Firefox
    from screenpy.abilities import BrowseTheWeb

    Perry.can(BrowseTheWeb.using(Firefox()))

    # For convenience, you can also do the same like this
    Perry = AnActor.named("Perry").who_can(BrowseTheWeb.using(Firefox()))

Now, Perry is able to attempt any actions that require the ability to BrowseTheWeb. Attempting actions looks like this::

    from screenpy import Target
    from screenpy.actions import Click

    EXAMPLE_LINK = Target.the("example link").located_by("//a")
    Perry.attempts_to(Click.the(EXAMPLE_LINK))

You'll notice we had to make a quick Target there. We'll get to :ref:`targets` later, but a quick summary is that they're how you tell the actors where to perform the action.

In the above example, the action knows what ability it requires, and it will ask the actor to find its matching ability to perform the action. If it does not have that ability, the actor will raise an |UnableToPerformException|.

Now that our actor has performed an action, they are ready to perform a test. Tests are performed with :ref:`questions`, like so::

    from screenpy.questions import Text
    from screenpy.resolutions import ReadsExactly

    THE_WELCOME_MESSAGE = Target.the("welcome_message").located_by("span.welcome")
    Perry.should_see_the((Text.of(THE_WELCOME_MESSAGE), ReadsExactly("Welcome!"))

That's the whole flow! Your actor is now ready to exit::

    Perry.exits_stage_right()

In summary, actors:
 - Are created by naming them using the |Actor.named| class method.
 - Are granted :ref:`abilities` using the |Actor.who_can| or |Actor.can| class methods.
 - Perform :ref:`actions` using their granted :ref:`abilities`.
 - Ask :ref:`questions` about the state of the application under test.
 - Exit gracefully, with a flourish.

Actor Class
-----------

.. module:: screenpy.actor
.. autoclass:: Actor
    :members:
