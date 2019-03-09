class Number(object):
    """
    Asks how many of a certain element are on the page, viewed by an
    :class:`|Actor|` Actor. This question is meant to be instantiated
    via its static :meth:`|Number|.of` method. A typical invocation might
    look like:

        Number.of(SEARCH_RESULTS)

    It can then be passed along to the :class:`|Actor|` to ask the
    question.
    """

    @staticmethod
    def of(target: "Target") -> "Number":
        """
        Provides the target to count.

        Args:
            target (Target): the :class:`|Target|` describing the element
                to count.

        Returns:
            :class:`|Number|`
        """
        return Number(target=target)

    def viewed_by(self, the_actor: "Actor") -> int:
        """
        Investigates the page as viewed by the supplied :class:`|Actor|`
        and gives its answer.

        Args:
            the_actor (Actor): The :class:`|Actor|` who will answer the
                question.

        Returns:
            int
        """
        return len(self.target.resolve_all_for(the_actor))

    def __init__(self, target: "Target") -> None:
        self.target = target
