from unittest import TestCase

from screenpy.abilities.browse_the_web import BrowseTheWeb


class TestBrowseTheWeb(TestCase):
    def test_can_be_instantiated(self):
        """BrowseTheWeb can be instantiated"""
        b = BrowseTheWeb.using(None)

        self.assertIsInstance(b, BrowseTheWeb)
