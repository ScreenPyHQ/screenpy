.. _resolutions:

===========
Resolutions
===========

Resolutions provide both
the expected value
and the comparison
to the answer
to a Question.
Pairing a Question
and a Resolution
forms the assertion step
to your tests.

There were a couple examples of assertions
in our :ref:`Complete Example`,
both performed by Polly.
One used the built-in ``ReadsExactly``,
while the other used a custom ``IsPalpable`` Resolution.
Let's examine the latter.

Resolutions all inherit
from the ``BaseResolution`` class.
All that is needed
is a "matcher" function,
which can come from
`PyHamcrest <https://github.com/hamcrest/PyHamcrest#pyhamcrest>`__,
or a custom matcher
written by you.

``IsPalpable`` uses the custom matcher
``has_tension_level``.
Here's how those might be assembled::

    # matchers/has_at_least_tension_level.py
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



    # resolutions/is_palpable.py
    from screenpy.resolutions import BaseResolution

    from ..matchers.has_tension_level import has_at_least_tension_level


    class IsPalpable(BaseResolution):
        """Match a tension level that is very, very high!!!

        Examples::

            the_actor.should(See.the(AudienceTension(), IsPalpable()))
        """
        line = "is palpable!"
        matcher_function = has_at_least_tension_level(85)

The End!
========

This is the final step
of the guided example.
If you want to revisit any section,
you can visit the :ref:`example toc` page.
