from typing import List as ListType


class List(object):
    """
    Asks for a list of elements, viewed by an :class:`|Actor|`. This
    question is meant to be instantiated using its static
    :meth:`|List|.of` or :meth:`|List|.of_all` methods. Typical
    invocations might look like:

        List.of(SEARCH_RESULTS)
        List.of_all(IMAGES)

    It can then be passed along to the :class:`|Actor|` to ask the
    question.
    """

    @staticmethod
    def of(target: "Target") -> "List":
        """
        Provides the target to list.

        Args:
            target (Target): the :class:`|Target|` describing the elements
                to list out.

        Returns:
            :class:`|List|`
        """
        return List(target)

    @staticmethod
    def of_all(target):
        """Syntactic sugar for :meth:`|List|.of`."""
        return List(target)

    def viewed_by(self, the_actor: "Actor") -> ListType["WebElement"]:
        """
        Investigates the page as viewed by the supplied :class:`|Actor|`
        and gives its answer.

        Args:
            the_actor (Actor): The :class:`|Actor|` who will answer the
                question.

        Returns:
            list(|WebElement|)
        """
        return self.target.resolve_all_for(the_actor)

    def __init__(self, target: "Target") -> None:
        self.target = target
