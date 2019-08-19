.. _abilities:

Abilities
=========

Abilities allow your |Actor| to **do** things. ScreenPy comes with one built in ability, the ability to |BrowseTheWeb|.

Using Abilities
---------------

To give an actor an ability, pass it in using the actor's |Actor.who_can| or |Actor.can| methods::

    from screenpy.abilities import BrowseTheWeb
    from screenpy.actor import Actor, AnActor
    from selenium.webdriver import Firefox

    # Add abilities on instantiation
    Perry = AnActor.named("Perry").who_can(BrowseTheWeb.using(Firefox()))

    # Or add abilities later
    Perry = AnActor.named("Perry")
    Perry.can(BrowseTheWeb.using(Firefox()))

Granting an ability to an actor allows them to perform any :ref:`actions` or ask any :ref:`questions` that require that ability. If an action or a question require an ability that the actor does not have, the actor will raise an |UnableToPerformException|.

Why Do I Have to Pass In Webdriver?
-----------------------------------

Passing in the Webdriver you want to use allows you to set up the driver however it needs to be to test your application. This way, you can easily switch between any Webdriver you need to use, local or remote.

The examples all use Selenium's webdriver, but you are free to use another webdriver that follows a similar API.

Writing New Abilities
---------------------

There may be other abilities your actors need to possess in order to test your application. You are encouraged to write your own! The only prescribed method for an ability is the `forget` method, which will complete any cleanup required. For an example, see the |BrowseTheWeb.forget| method of the BrowseTheWeb ability.

BrowseTheWeb Class
------------------

.. module:: screenpy.abilities.browse_the_web
.. autoclass:: BrowseTheWeb
    :members:

