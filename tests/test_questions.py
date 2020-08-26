from json.decoder import JSONDecodeError
from unittest import mock

import pytest

from screenpy import AnActor, Target
from screenpy.abilities import MakeAPIRequests
from screenpy.abilities.browse_the_web import BrowsingError
from screenpy.exceptions import UnableToAnswer
from screenpy.questions import (
    BodyOfTheLastResponse,
    BrowserTitle,
    BrowserURL,
    Cookies,
    CookiesOnTheAPISession,
    CookiesOnTheWebSession,
    Element,
    HeadersOfTheLastResponse,
    List,
    Number,
    Selected,
    StatusCodeOfTheLastResponse,
    Text,
)


class TestBodyOfTheLastResponse:
    def test_can_be_instantiated(self):
        botlr = BodyOfTheLastResponse()

        assert isinstance(botlr, BodyOfTheLastResponse)

    def test_raises_error_if_no_responses(self, APITester):
        botlr = BodyOfTheLastResponse()
        APITester.ability_to(MakeAPIRequests).responses = []

        with pytest.raises(UnableToAnswer):
            botlr.answered_by(APITester)

    def test_handles_non_json(self, APITester):
        """Non-JSON bodies are returned as text."""
        botlr = BodyOfTheLastResponse()
        test_body = "And stop calling me Shirley."
        mock_response = mock.Mock()
        mock_response.json.side_effect = JSONDecodeError(
            "Surely, it's not JSON", test_body, 1
        )
        mock_response.text = test_body
        APITester.ability_to(MakeAPIRequests).responses = [mock_response]

        answer = botlr.answered_by(APITester)

        assert answer == test_body


class TestBrowserTitle:
    def test_can_be_instantiated(self):
        b = BrowserTitle()

        assert isinstance(b, BrowserTitle)


class TestBrowserURL:
    def test_can_be_instantiated(self):
        b = BrowserURL()

        assert isinstance(b, BrowserURL)


class TestCookies:
    def test_can_be_instantiated(self):
        c = Cookies()

        assert isinstance(c, Cookies)

    @mock.patch("screenpy.questions.cookies.CookiesOnTheWebSession")
    def test_calls_web_session(self, mock_CookiesOnTheWebSession, Tester):
        """Cookies calls CookiesOnTheWebSession for BrowseTheWeb"""
        Cookies().answered_by(Tester)

        mock_CookiesOnTheWebSession.return_value.answered_by.assert_called_once_with(
            Tester
        )

    @mock.patch("screenpy.questions.cookies.CookiesOnTheAPISession")
    def test_calls_api_session(self, mock_CookiesOnTheAPISession, APITester):
        """Cookies calls CookiesOnTheAPISession for MakeAPIRequests"""
        Cookies().answered_by(APITester)

        mock_CookiesOnTheAPISession.return_value.answered_by.assert_called_once_with(
            APITester
        )

    def test_raises_exception_if_missing_abilities(self):
        with pytest.raises(UnableToAnswer):
            Cookies().answered_by(AnActor.named("Bob"))


class TestCookiesOnTheAPISession:
    def test_can_be_instantiated(self):
        c = CookiesOnTheAPISession()

        assert isinstance(c, CookiesOnTheAPISession)


class TestCookiesOnTheWebSession:
    def test_can_be_instantiated(self):
        c = CookiesOnTheWebSession()

        assert isinstance(c, CookiesOnTheWebSession)


class TestElement:
    def test_can_be_instantiated(self):
        e = Element(None)

        assert isinstance(e, Element)

    def test_question_returns_none_if_no_element_found(self, Tester):
        mock_target = mock.Mock(spec=Target)
        mock_target.found_by.side_effect = BrowsingError()

        element = Element(mock_target).answered_by(Tester)

        assert element is None


class TestStatusCodeOfTheLastResponse:
    def test_can_be_instantiated(self):
        scotlr = StatusCodeOfTheLastResponse()

        assert isinstance(scotlr, StatusCodeOfTheLastResponse)

    def test_raises_error_if_no_responses(self, APITester):
        scotlr = StatusCodeOfTheLastResponse()
        APITester.ability_to(MakeAPIRequests).responses = []

        with pytest.raises(UnableToAnswer):
            scotlr.answered_by(APITester)


class TestList:
    def test_can_be_instantiated(self):
        l1 = List.of(None)
        l2 = List.of_all(None)

        assert isinstance(l1, List)
        assert isinstance(l2, List)


class TestNumber:
    def test_can_be_instantiated(self):
        n1 = Number.of(None)

        assert isinstance(n1, Number)


class TestSelected:
    def test_can_be_instantiated(self):
        s1 = Selected.option_from(None)
        s2 = Selected.option_from_the(None)
        s3 = Selected.options_from(None)
        s4 = Selected.options_from_the(None)

        assert isinstance(s1, Selected)
        assert isinstance(s2, Selected)
        assert isinstance(s3, Selected)
        assert isinstance(s4, Selected)

    def test_options_from_sets_multi(self):
        multi_selected = Selected.options_from(None)

        assert multi_selected.multi


class TestHeadersOfTheLastResponse:
    def test_can_be_instantiated(self):
        hotlr = HeadersOfTheLastResponse()

        assert isinstance(hotlr, HeadersOfTheLastResponse)

    def test_raises_error_if_no_responses(self, APITester):
        hotlr = HeadersOfTheLastResponse()
        APITester.ability_to(MakeAPIRequests).responses = []

        with pytest.raises(UnableToAnswer):
            hotlr.answered_by(APITester)


class TestText:
    def test_can_be_instantiated(self):
        t1 = Text.of(None)
        t2 = Text.of_all(None)

        assert isinstance(t1, Text)
        assert isinstance(t2, Text)

    def test_of_all_sets_multi(self):
        multi_text = Text.of_all(None)

        assert multi_text.multi
