from selenium.webdriver.common.by import By

from .abilities.browse_the_web import BrowseTheWeb


class Target(object):
    """
    A class to contain information about an element.
    """

    def resolve_for(self, the_actor):
        return the_actor.uses_ability_to(BrowseTheWeb).find(self.get_locator())

    def resolve_all_for(self, the_actor):
        return the_actor.uses_ability_to(BrowseTheWeb).find_all(self.get_locator())

    def get_locator(self):
        if self.locator.startswith("/"):
            return (By.XPATH, self.locator)
        else:
            return (By.CSS_SELECTOR, self.locator)

    def __repr__(self):
        return self.target_name

    def __str__(self):
        return self.target_name

    @staticmethod
    def the(desc):
        return Target(desc)

    def located_by(self, locator):
        self.locator = locator
        return self

    def __init__(self, desc):
        self.target_name = desc
        self.locator = ""
