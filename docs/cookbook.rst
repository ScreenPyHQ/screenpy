================
ScreenPy Recipes
================

This collection contains
examples of common ScreenPy use-cases.

Retrieving Initial Answers
==========================

Some tests may need to ensure something has changed.
You are able to retrieve
the answers to Questions
anywhere you may need to.

.. code-block:: python

    empty_todo_list_text = Text.of_the(TODO_LIST).answered_by(Wanda)

    when(Wanda).attempts_to(AddTodoListItem("Wash the fish"))

    then(Wanda).should(
        See.the(Text.of_the(TODO_LIST), DoesNot(ReadExactly(empty_todo_list_text)),
    )

Using MakeNote
--------------

You can also retrieve initial answers
with the :class:`~screenpy.actions.MakeNote` class,
and retrieve the value
with a :ref:`direction <directions>`.

.. code-block:: python

    when(Cameron).attempts_to(
        StartRecording(),
        MakeNote.of_the(Text.of_the(OPENING_LINE))).as_("camera 2 cue"),
        CutToCamera(2).after_line(1),
    )

    then(Dirk).should(
        See.the(JumpCutLine(), ReadsExactly(the_noted("camera 2 cue"))),
    )

.. _makenote gotcha:

Gotchas
^^^^^^^

There is one limitation
to using :class:`~screenpy.actions.MakeNote`:
it is not possible
to make a note and retrieve it
in the same Actions list.

.. code-block:: python

    # CAN NOT do this:
    when(Perry).attempts_to(
        ...
        MakeNote.of_the(Text.of_the(NOTABLE_ITEM)).as_("potent notable"),
        Enter.the_text(noted_under("potent notable")).into_the(INPUT_FIELD),
        ...
    )

    # Workaround:
    when(Perry).attempts_to(
        ...
        MakeNote.of_the(Text.of_the(NOTABLE_ITEM)).as_("potent notable"),
    )
    and_(Perry).attempts_to(
        Enter.the_text(noted_under("potent notable")).into_the(INPUT_FIELD),
        ...
    )

This limitation exists
because the note
isn't written down
until the action is *performed*.
:func:`~screenpy.directions.noted_under` will attempt
to retrieve the note
as the actions list
is being passed in to :func:`~screenpy.actor.Actor.attempts_to`,
which is too quick!

See `issue #51 <https://github.com/perrygoy/screenpy/issues/51>`__
for more details
(and frustration).

The Eventually Class
====================

If you know an Action or Task
will *eventually* complete,
but may need a few tries,
you can use the :class:`~screenpy.actions.Eventually` Action!

This Action takes a performable
and performs it,
repeatedly,
until either it succeeds
or the timeout expires.
Here's what that looks like.

.. code-block:: python

    Marcel.attempts_to(
        Eventually(
            See.the(Text.of_the(CALL_STATUS), ReadsExactly("Completed!"))
        )
    )

The above will repeatedly attempt the assertion
that the Call Status section reads "Completed!"
until either it does,
or 20 seconds (by default) have elapsed.
If the timeout expires,
a ``TimeoutError`` will be raised
from the caught error.

Debugging
=========

The Debug Class
---------------

You can use
the :class:`~screenpy.actions.Debug` Action
to drop a debugger
in a series of Actions.

You will need to go up a few frames
to get to the Actor's :meth:`~screenpy.actor.Actor.attempts_to` method.
From there, you will be able to
step through each Action one at a time.

.. code-block:: python

    given(Perry).was_able_to(
        Click.on_the(LOGIN_LINK),
        Enter.the_text(USERNAME).into_the(USERNAME_FIELD),
        Enter.the_password(PASSWORD).into_the(PASSWORD_FIELD),
        Debug(),  # gives you a debugger here!
        Click.on_the(SIGN_IN_BUTTON),
        Wait(60).seconds_for_the(WELCOME_BANNER),
    )

The Pause Class
---------------

You can also use :class:`~screenpy.actions.Pause`
to stop the test for a few moments,
if you only need to see
what the state of the page is.

.. code-block:: python

    given(Perry).was_able_to(
        Click.on_the(LOGIN_LINK),
        Enter.the_text(USERNAME).into_the(USERNAME_FIELD),
        Enter.the_password(PASSWORD).into_the(PASSWORD_FIELD),
        Pause.for_(60).seconds_because("I need to see something"),  # stops the execution here for 60 seconds.
        Click.on_the(SIGN_IN_BUTTON),
        Wait(60).seconds_for_the(WELCOME_BANNER),
    )


Cleaning Up
===========

Sometimes,
your Actors may need one or more of their Abilities
to do some cleanup.
You can assign cleanup tasks to your Actor
using their :meth:`~screenpy.actor.Actor.has_ordered_cleanup_tasks`
or :meth:`~screenpy.actor.Actor.has_independent_cleanup_tasks` method.

.. code-block:: python

    Perry = AnActor.named("Perry").who_can(BrowseTheWeb.using_firefox())
    Perry.has_ordered_cleanup_tasks(CompleteAllTodoItems())

    # ... test code here

    Perry.cleans_up()  # you can call the cleanup method directly
    Perry.exit()  # or it is called here automatically

These tasks can be assigned at any point
before the Actor exits.
Some opportune moments are
when the Actor is created,
or during a test or task
which creates things that need to be cleaned up.

Once the cleanup tasks are performed,
they are removed from the Actor's cleanup list.
They will only be performed once.


Using Silently
==============

    "Talk less. Smile more." -- Aaron Burr in Hamilton

Sometimes you only need logging when things go wrong.
:func:`~screenpy.actions.Silently` gives you the capability
to only log the important things when things go right.
Everything inside of ``Silently`` is prevented from logging.

Example: The following Action:

.. code-block:: python

    class PerformChatty(Performable):
        @beat("{} tries to PerformChatty")
        def perform_as(self, actor: Actor):
            actor.will(PerformA())

    # used inside a test
    def test_1(marcel):
        marcel.will(PerformChatty())

Would generate this log::

    Marcel tries to PerformChatty
        Marcel tries to PerformA
            Marcel tries to PerformB
                Marcel tries to PerformPass
                    Marcel sees if simpleQuestion is equal to True.
                        Marcel examines SimpleQuestion
                            => True
                        ... hoping it's equal to True.
                            => <True>

But what if we didn't need to know 
all the steps being taken in ``PerformChatty`` 
unless they were to fail?
Wrapping ``PerformA`` in ``Silently``...

.. code-block:: python

    class PerformChatty(Performable):
        @beat("{} tries to PerformChatty")
        def perform_as(self, actor: Actor):
            actor.will(Silently(PerformA()))

...will only generate this log::

    Marcel tries to PerformChatty

Unless of course something bad happens 
inside of ``PerformA`` in which case 
the normal logging will take place::

    Marcel tries to PerformChatty
        Marcel tries to PerformA
            Marcel tries to PerformB
                Marcel tries to PerformPass
                    Marcel sees if simpleQuestion is equal to True.
                        Marcel examines SimpleQuestion
                            => True
                        ... hoping it's equal to False.
                            => <False>
                        ***ERROR***

    AssertionError:
    Expected: <True>
         but: was <False>


Using Either
===========

Sometimes you may need to use a try/except control flow in your test, 
for one reason or another. 
Luckily, your Actor can perform 
this flow with the :class:`~screenpy.actions.Either` Action!

.. code-block:: python

    the_actor.will(Either(DoAction()).or_(DoDifferentAction())

The Actor will attempt to perform the first action (or set of actions).  
If successful, the Actor moves on. 
But if an ``AssertionError`` is raised 
the Actor will begin performing 
the second action (or set of actions) 
passed into :meth:`~screenpy.actions.Either.or_`.
Note the Actor only catches ``AssertionError`` here 
allowing for other exceptions to still be raised.

Other exceptions can be caught when specified.

.. code-block:: python
    
    the_actor.will(
        Either(DoAction())
        .or_(DoDifferentAction())
        .ignoring(ValueError, AssertionError)
    )

:class:`~screenpy.actions.Either` allows users to pass in multiple actions. 
This is similar Actor performing multiple actions in one call.

.. code-block:: python

    the_actor.will(
        Either(
            DoAction1(),
            DoAction2(),
            DoAction3(),
        ).or_(
            DoDifferentAction1(),
            DoDifferentAction2(),
            DoDifferentAction3(),
        )
    )

:class:`~screenpy.actions.Either` has the ability to ignore other exceptions.
Y


.. note::
   :class:`~screenpy.actions.Either` will not describe any cleanup for the Actor
   after it experiences a failure in the first routine; the Actor will proceed directly
   to the second routine. Keep this in mind while defining the two branches of Actions.

To help illustrate this further here is a real-world example 
using `screenpy_selenium <https://screenpy-selenium-docs.readthedocs.io/en/latest/>`__

.. code-block:: python

    the_actor.will(
       Either(
           See(BrowserURL(), ReadsExactly(URL)),
           CheckIfAuthenticated(),
       ).or_(
           ClearCache()
           Open.their_browser_on(URL())
           Eventually(Enter(username).into(USERNAME_FIELD)),
           Enter.the_secret(password).into(PASSWORD_FIELD),
           Click.on(SIGN_IN_BUTTON)
       )
    )

