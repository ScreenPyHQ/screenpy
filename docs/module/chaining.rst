.. _chaining:

Chaining
========

The |Chain| action
is a sort of meta-action
that can group many other actions
into a series.
This is useful
for those features
that require things
like clicking-and-dragging
or hovering.

Many of the included :ref:`actions`
may be added to a Chain,
but some of the Actions
are not chainable
and will raise an |UnableToAct|.
The Actions
which can be chained
correspond to the methods
of Selenium's |ActionChains| class.

Adding Actions
to a Chain
looks like this:

.. code-block:: python

    from screenpy.actions import Chain, Click, Hover

    from ..user_interface.homepage import HAMBURGER_MENU, SIGN_IN_LINK


    Perry.attempts_to(
        Chain(Hover.on_the(HAMBURGER_MENU), Click.on_the(SIGN_IN_LINK))
    )

If you write a custom Action
which should be able
to be added to a Chain,
you must define
an `add_to_chain(self, the_actor, the_chain)` method
on your custom Action.
This method takes in
the actor who will perform the chain
along with an instantiated ActionChains object
and adds your action
to the chain
using the |ActionChains| API.
