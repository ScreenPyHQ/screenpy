=========
Questions
=========

When you are ready
to make an assertion
in your test,
your Actor can ask a Question.
The answer to this Question
will be compared
against a Resolution.
This pairing forms an assertion in ScreenPy.

Our :ref:`Complete Example` used two Questions:
``AudienceTension`` and ``TopAudienceReaction``.
Let's see how the latter might look::

    # questions/top_audience_reaction.py
    from screenpy import Actor

    from ..abilities import PollTheAudience


    class TopAudienceReaction:
        """Ask about the audience's most popular reaction.

        Examples::

            the_actor.should(See.the(TopAudienceReaction(), Equals(LAUGHING))
        """

        def answered_by(self, the_actor: Actor) -> str:
            """Direct the actor to ask about the audience's top mood."""
            pollster = the_actor.ability_to(PollTheAudience).poll_connection
            return pollster.poll_mood().top_mood


A Question is :class:`~screenpy.protocols.Answerable`,
which is to say
it has an ``answered_by`` method.

Passing a Question
along with a Resolution
into the :class:`~screenpy.actions.See` Action
is how to make assertions in ScreenPy.
The Question provides the actual value
while the Resolution provides the expected value.

Where to Go from Questions
==========================

* :ref:`resolutions`
