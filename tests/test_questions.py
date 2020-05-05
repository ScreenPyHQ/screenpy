from screenpy.questions import (
    BrowserTitle,
    BrowserURL,
    Element,
    List,
    Number,
    Selected,
    Text,
)


class TestBrowserTitle:
    def test_can_be_instantiated(self):
        """BrowserTitle can be instantiated"""
        b = BrowserTitle()

        assert isinstance(b, BrowserTitle)


class TestBrowserURL:
    def test_can_be_instantiated(self):
        """BrowserURL can be instantiated"""
        b = BrowserURL()

        assert isinstance(b, BrowserURL)


class TestElement:
    def test_can_be_instantiated(self):
        """Element can be instantiated"""
        e = Element(None)

        assert isinstance(e, Element)


class TestList:
    def test_can_be_instantiated(self):
        """List can be instantiated"""
        l1 = List.of(None)
        l2 = List.of_all(None)

        assert isinstance(l1, List)
        assert isinstance(l2, List)


class TestNumber:
    def test_can_be_instantiated(self):
        """Number can be instantiated"""
        n1 = Number.of(None)

        assert isinstance(n1, Number)


class TestSelected:
    def test_can_be_instantiated(self):
        """Selected can be instantiated"""
        s1 = Selected.option_from(None)
        s2 = Selected.option_from_the(None)
        s3 = Selected.options_from(None)
        s4 = Selected.options_from_the(None)

        assert isinstance(s1, Selected)
        assert isinstance(s2, Selected)
        assert isinstance(s3, Selected)
        assert isinstance(s4, Selected)

    def test_options_from_sets_multi(self):
        """Selected.options_from sets multi to True"""
        multi_selected = Selected.options_from(None)

        assert multi_selected.multi


class TestText:
    def test_can_be_instantiated(self):
        """Text can be instantiated"""
        t1 = Text.of(None)
        t2 = Text.of_all(None)

        assert isinstance(t1, Text)
        assert isinstance(t2, Text)

    def test_of_all_sets_multi(self):
        """Text.of_all sets multi to True"""
        multi_text = Text.of_all(None)

        assert multi_text.multi
