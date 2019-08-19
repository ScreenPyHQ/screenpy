.. _quickstart:

Quickstart
==========

If you just want to see it all work, copy/paste the following into a file or your interpreter and call "**Action**!"

.. code-block:: python

    from selenium.webdriver import Firefox

    from screenpy import AnActor, Target, given, when, then
    from screenpy.abilities import BrowseTheWeb
    from screenpy.actions import Click, Open
    from screenpy.questions import Text
    from screenpy.resolutions import ReadsExactly

    # This would normally go in your tasks/start.py
    class Start(object):
        """Test case start points"""
        def perform_as(self, actor):
            actor.attempts_to(Open.browser_on(self.location))
        @staticmethod
        def on_the_screenpy_repo():
            return Start("https://github.com/perrygoy/screenpy")
        def __init__(self, location):
            self.location = location

    # These two would normally go in your user_interface/some_page.py
    THE_AUTHOR_LINK = Target.the("repository author link").located_by("a[rel=author]")
    THE_DISPLAYED_USER_NAME = Target.the("GitHub user's name").located_by("span.vcard-fullname")

    # This would normally go in your questions/user_name.py
    class UserName(object):
        """Questions about the user name"""
        def answered_by(self, the_actor):
            return Text.of(THE_DISPLAYED_USER_NAME).answered_by(the_actor)
        @staticmethod
        def text():
            return UserName()

    perry = AnActor.named("Perry").who_can(BrowseTheWeb.using(Firefox()))

    given(perry).was_able_to(Start.on_the_screenpy_repo())
    when(perry).attempts_to(Click.on(THE_AUTHOR_LINK).then_wait_for(THE_DISPLAYED_USER_NAME))
    then(perry).should_see_the((UserName.text(), ReadsExactly("Perry Goy")),)
    perry.exit_stage_right()
