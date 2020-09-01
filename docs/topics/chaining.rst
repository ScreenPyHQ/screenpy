.. _chaining:

Chaining
========

The |Chain| action is a sort of meta-action
that can group many other actions into a series.
This is useful for those features that require things like
clicking-and-dragging or hovering.

Many of the included :ref:`actions` may be added to a Chain,
but some of the Actions are not ``Chainable``
and will raise an |UnableToAct|.
The Actions which can be chained
correspond to the methods of Selenium's |ActionChains| class.

In order to be ``Chainable``,
an action must implement an ``add_to_chain`` method.
Keep this in mind
when you write custom actions.
See the :ref:`protocols` page for more information.

Adding Actions to a Chain looks like this::

    from screenpy.actions import Chain, Click, Hover

    from ..user_interface.homepage import HAMBURGER_MENU, SIGN_IN_LINK


    Perry.attempts_to(
        Chain(Hover.on_the(HAMBURGER_MENU), Click.on_the(SIGN_IN_LINK))
    )

