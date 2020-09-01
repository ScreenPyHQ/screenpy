.. _cookbook:

ScreenPy Recipes
================

This collection contains
some examples of common use-cases
you may run into while using ScreenPy.

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
outside of the ``should_see`` assertion step::

    empty_todo_list_text = Text.of_the(TODO_LIST).answered_by(Perry)

    when(Perry).attempts_to(AddTodoListItem("Wash the fish"))

    then(Perry).should_see_the(
        (Text.of_the(TODO_LIST), DoesNot(ReadExactly(empty_todo_list_text))
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
wait 20 seconds for that condition to be met::

    class appear_in_greyscale:
        def __init__(self, locator):
            self.locator = locator

        def __call__(self, driver):
            element = driver.find_element(*self.locator)
            return element.value_of_css_property(filter) == "grayscale(100%)"

    Perry.attempts_to(Wait.for_the(PROFILE_ICON).to(appear_in_greyscale))

Debugging
---------

The Debug Class
^^^^^^^^^^^^^^^

The |Debug| class can be used
to drop a debugger in a series of actions.

You will need to go up a few frames
to get to the actor's |Actor.attempts_to| method,
but then you will be able to
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

|Pause| can also be used
to stop the test for a few moments,
if you just need to see
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
