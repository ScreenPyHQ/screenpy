"""Debug a performance.

Launch a debugger either using pdb or the debugger set in the PYTHONBREAKPOINT
environment variable.
(See more information in PEP-553 https://www.python.org/dev/peps/pep-0553/)
"""

import pdb  # noqa: T100

from screenpy.actor import Actor
from screenpy.pacing import beat

# pylint: disable=forgotten-debug-statement
# haha, thanks pylint.


class Debug:
    """Activate a debugger to step through Actions.

    In long series of Actions, it can be difficult to drop a debugger in
    the right place. This Action can be placed anywhere in the list to
    give you a debugger in the middle of the Action list. This Action
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

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return "Assume direct control."

    @beat("{} assumes direct control...")
    def perform_as(self, _: Actor) -> None:
        """Direct the Actor to activate a debugger."""
        try:
            # Hello! To get to the perform loop and step through the remaining
            # Actions, you will need to go "up" about 3 times.
            breakpoint()  # noqa: T100
        except NameError:
            pdb.set_trace()  # noqa: T100
