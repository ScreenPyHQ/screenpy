from typing import List as ListType


class List(object):
    """
    Asks for a list of elements, viewed by an |Actor|. This question is
    meant to be instantiated using its static |List.of| or |List.of_all|
    methods. Typical invocations might look like:

        List.of(SEARCH_RESULTS)
        List.of_all(IMAGES)

    It can then be passed along to the |Actor| to ask the question.
    """

    @staticmethod
    def of(target: "Target") -> "List":
        """
        Provides the target to list.

        Args:
            target (Target): the |Target| describing the elements to list
                out.

        Returns:
            |List|
        """
        return List(target)

    @staticmethod
    def of_all(target):
        """Syntactic sugar for |List.of|."""
        return List(target)

    def viewed_by(self, the_actor: "Actor") -> ListType["WebElement"]:
        """
        Investigates the page as viewed by the supplied |Actor| and gives
        their answer.

        Args:
            the_actor (Actor): The |Actor| who will answer the question.

        Returns:
            list(|WebElement|)
        """
        return self.target.all_found_by(the_actor)

    def __init__(self, target: "Target") -> None:
        self.target = target
