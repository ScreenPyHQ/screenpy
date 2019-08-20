from screenpy.actions import Open

from ..user_interface.homepage import URL


class Start:
    @staticmethod
    def on_the_homepage():
        return Start(URL)

    def perform_as(self, actor):
        actor.attempts_to(Open.browser_on(self.location))

    def __init__(self, location):
        self.location = location
