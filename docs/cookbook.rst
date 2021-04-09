.. _cookbook:

ScreenPy Recipes
================

This collection contains
examples of common ScreenPy use-cases.

.. _actor_setup:

Setting Up Actors
-----------------

Set up an actor to browse the web::

    Perry = AnActor.who_can(BrowseTheWeb.using_firefox())

Set up an actor to browse the web with a specific driver::

    options = webdriver.ChromeOptions()
    options.set_headless()
    # ... other setup, maybe
    driver = webdriver.Chrome(options=options)

    Perry = AnActor.who_can(BrowseTheWeb.using(driver))

.. _debugging:

Retrieving Initial Answers
--------------------------

Some tests may need to ensure something has changed.
You are able to retrieve
the answers to questions
anywhere you may need to::

    empty_todo_list_text = Text.of_the(TODO_LIST).answered_by(Perry)

    when(Perry).attempts_to(AddTodoListItem("Wash the fish"))

    then(Perry).should_see_the(
        (Text.of_the(TODO_LIST), DoesNot(ReadExactly(empty_todo_list_text))
    )

Using MakeNote
^^^^^^^^^^^^^^

You can also retrieve initial answers
with the :class:`~screenpy.actions.MakeNote` class,
and retrieve the value
with a |direction|::

    when(Perry).attempts_to(
        Visit(URL),
        MakeNote.of(TheText.of_the(TODO_LIST)).as_("empty todo list"),
        AddTodoListItem("Wash the fish"),
    )

    then(Perry).should_see_the(
        (Text.of_the(TODO_LIST), DoesNot(ReadExactly(the_noted("empty todo list")))
    )


Waiting
-------

Bread-and-butter default wait,
waits 20 seconds for the login modal to appear::

    Perry.attempts_to(Wait.for_the(LOGIN_MODAL))


Wait for a non-default timeout
and a different condition::

    Perry.attempts_to(Wait(42).seconds_for(THE_WELCOME_BANNER).to_disappear())


Using a custom condition,
wait 20 seconds
for the application
to meet the condition::

    class appear_in_greyscale:
        def __init__(self, locator):
            self.locator = locator

        def __call__(self, driver):
            element = driver.find_element(*self.locator)
            return element.value_of_css_property(filter) == "grayscale(100%)"

    Perry.attempts_to(Wait.for_the(PROFILE_ICON).to(appear_in_greyscale))


Using a custom condition
which does not use a Target::

    def url_to_contain_text_and_be_at_least_this_long(text, length):
        def _predicate(driver):
            return text in driver.url and len(driver.url) >= length

        return _predicate

    Perry.attempts_to(
        #   ⇩ note the parentheses here
        Wait().using(
            url_to_contain_text_and_be_at_least_this_long
        ).with_("hello", 20)
    )


Debugging
---------

The Debug Class
^^^^^^^^^^^^^^^

You can use
the |Debug| class
to drop a debugger
in a series of actions.

You will need to go up a few frames
to get to the actor's |Actor.attempts_to| method.
From there, you will be able to
step through each action one at a time.

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
^^^^^^^^^^^^^^^

You can also use |Pause|
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
-----------

Sometimes,
your Actors may need
one or more of their abilities
to do some cleanup.
You can assign cleanup tasks
to your Actor
using their :meth:`~screenpy.actor.Actor.has_cleanup_tasks` method::

    Perry = AnActor.named("Perry").who_can(BrowseTheWeb.using_firefox())
    Perry.has_cleanup_task(CompleteAllTodoItems())

    # ... test code here

    Perry.cleans_up()  # you can call the cleanup method directly
    Perry.exit()  # or it is called here automatically

These tasks can be assigned
at any point
before the Actor exits.
Some opportune moments are
when the Actor is created,
or during a test
or task
which creates things
that need to be cleaned up.

Once the cleanup tasks are performed,
they are removed
from the Actor's cleanup list.
They will only be performed once.
