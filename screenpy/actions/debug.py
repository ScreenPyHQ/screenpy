"""
An action to launch a debugger either using the debugger set in the
PYTHONBREAKPOINT environment variable (see more information in PEP-553
https://www.python.org/dev/peps/pep-0553/) or falling back to pdb.
"""

import pdb

from screenpy.actor import Actor
from screenpy.pacing import beat


class Debug:
    """Activate a debugger to step through actions.

    In long series of actions, it can be difficult to drop a debugger in
    the right place. This action can be placed anywhere in the chain to
    give you a debugger in the middle of the action chain. This action
    uses Python 3.7+'s breakpoint() call if it can, otherwise it will
    default to pdb.set_trace().

    Examples::

        the_actor.attempts_to(
            Click.on_the(SIGN_IN_BUTTON),
            # ...
            Debug(),
            Wait.for_the(SURPRISE_CONFETTI).to_disappear(),
            # ...
        )
    """

    @beat("{} assumes direct control...")
    def perform_as(self, _: Actor) -> None:
        """Direct the actor to activate a debugger."""

        # Hello! You will probably need to 'return' from this function a
        # few times to reach the action chain you're currently in. It
        # will look like a for-loop inside the actor's `perform` method.
        # Once you are there, you can step through the actions one by one.

        try:
            breakpoint()
        except NameError:
            pdb.set_trace()
