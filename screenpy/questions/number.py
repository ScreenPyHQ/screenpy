class Number(object):
    """
    Asks how many of a certain element are on the page, viewed by an
    |Actor|. This question is meant to be instantiated via its static
    |Number.of| method. A typical invocation might look like:

        Number.of(SEARCH_RESULTS)

    It can then be passed along to the |Actor| to ask the question.
    """

    @staticmethod
    def of(target: "Target") -> "Number":
        """
        Provides the target to count.

        Args:
            target (Target): the |Target| describing the element to count.

        Returns:
            |Number|
        """
        return Number(target=target)

    def viewed_by(self, the_actor: "Actor") -> int:
        """
        Investigates the page as viewed by the supplied |Actor| and gives
        their answer.

        Args:
            the_actor (Actor): The |Actor| who will answer the question.

        Returns:
            int
        """
        return len(self.target.all_found_by(the_actor))

    def __init__(self, target: "Target") -> None:
        self.target = target
