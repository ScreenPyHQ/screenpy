from screenpy.actions import Open

from ..user_interface.github_home_page import url


class Start:
    def perform_as(self, actor):
        actor.attempts_to(Open.browser_on(self.location))

    @staticmethod
    def on_the_homepage():
        return Start(url)

    def __init__(self, location):
        self.location = location
