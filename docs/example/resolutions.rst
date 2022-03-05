===========
Resolutions
===========

Resolutions provide both
the expected value
and the comparison method
to the answer to a Question.
Pairing a Question
and a Resolution
forms the assertion step
to your tests.

There were a couple examples of assertions
in our :ref:`Complete Example`,
both performed by Polly.
One used the built-in :class:`~screenpy.resolutions.Equals` Resolution,
while the other used a custom ``IsPalpable`` Resolution.
Let's examine the latter.

Resolutions all inherit
from the :class:`~screenpy.resolutions.BaseResolution` class.
All that is needed
is a ``line`` and a "matcher" function.

The ``line`` appears in the log.
Write the line such that
it describes the expected value
while completing the sentence,
"Hoping it's...".
You can use ``{expectation}`` here
to reference the expected value.

The "matcher" function
can come from `PyHamcrest <https://github.com/hamcrest/PyHamcrest#pyhamcrest>`__,
or it can be a custom matcher
written by you.

Anyway,
``IsPalpable`` uses the custom matcher
``has_at_least_tension_level``.
Here's how those might be assembled::

    # resolutions/matchers/has_at_least_tension_level.py
    from hamcrest import BaseMatcher


    class HasAtLeastTensionLevel(BaseMatcher):
        """Assert that a tension object has at least a specific tension level."""

        def _matches(self, item: Any) -> bool:
            """Whether the assertion passes."""
            return self.tension_level <= item.tension

        def __init__(self, tension_level: int) -> None:
            self.tension_level = tension_level


    def has_at_least_tension_level(tension_level: int) -> HasAtLeastTensionLevel:
        return HasAtLeastTensionLevel(tension_level)

.. code-block:: python

    # resolutions/is_palpable.py
    from screenpy.resolutions import BaseResolution

    from ..matchers.has_tension_level import has_at_least_tension_level


    class IsPalpable(BaseResolution):
        """Match a tension level that is very, very high!!!

        Examples::

            the_actor.should(See.the(AudienceTension(), IsPalpable()))
        """
        line = "a palpable tension!"
        matcher_function = has_at_least_tension_level(85)

That's really all there is
to creating a Resolution!

The End!
========

This is the final step
of the guided example.
If you want to revisit any section,
you can visit the :ref:`guided example` page.
