.. _chaining:

Chaining
========

The |Chain| Action is a sort of meta-Action
that can group many other Actions into a series.
This is useful for testing features which include things like
clicking-and-dragging or hovering.

You are able to chain
many of the included :ref:`actions`,
but some are not :class:`~screenpy.protocols.Chainable`.
These will cause your Actor
to raise an |UnableToAct| exception.
Chainable Actions
correspond to the methods
of Selenium's |ActionChains| class.

To be Chainable,
an Action must implement
an ``add_to_chain`` method.
Keep this in mind
when you write custom Actions.
See the :ref:`protocols` page for more information.

Adding Actions to a Chain looks like this::

    from screenpy.actions import Chain, Click, Hover

    from ..user_interface.homepage import HAMBURGER_MENU, SIGN_IN_LINK


    Perry.attempts_to(
        Chain(
            Hover.on_the(HAMBURGER_MENU),
            Click.on_the(SIGN_IN_LINK),
        )
    )

