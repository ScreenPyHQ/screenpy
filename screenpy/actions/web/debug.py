"""
An action to launch a debugger either using the debugger set in the
PYTHONBREAKPOINT environment variable (see more information in PEP-553
https://www.python.org/dev/peps/pep-0553/) or falling back to pdb. An
actor can perform this action like so:

    the_actor.attempts_to(Debug())
"""


import pdb

from screenpy.actor import Actor
from screenpy.pacing import beat


class Debug:
    """
    In long chains of actions, it can be difficult to drop a debugger in
    the right place. This action can be placed anywhere in the chain to
    give you a debugger in the middle of the action chain. This action
    uses Python 3.7+'s breakpoint() call if it can, otherwise it will
    default to pdb.set_trace().

    A Debug action is expected to be instantiated in the standard way. A
    typical instantiation will always look like:

        Debug()

    It can then be passed along to the |Actor| to perform the action.
    """

    @beat("{} assumes direct control...")
    def perform_as(self, _: Actor) -> None:
        """Activate a debugger."""
        try:
            breakpoint()
        except NameError:
            pdb.set_trace()

        # Hello! You will probably need to 'return' from this function a
        # few times to reach the action chain you're currently in. It
        # will look like a for-loop inside the actor's `perform` method.
        # Once you are there, you can step through the actions one by one.
