from unittest import mock

import pytest
from requests.cookies import RequestsCookieJar

from screenpy import Target
from screenpy.abilities import BrowseTheWeb, MakeAPIRequests
from screenpy.questions import (
    BodyOfTheLastResponse,
    BrowserTitle,
    BrowserURL,
    Cookies,
    Element,
    HeadersOfTheLastResponse,
    List,
    Number,
    Selected,
    StatusCodeOfTheLastResponse,
    Text,
    TextOfTheAlert,
)
from screenpy.resolutions import (
    ContainsTheEntries,
    ContainsTheEntry,
    ContainsTheText,
    ContainTheEntry,
    Empty,
    EqualTo,
    IsEmpty,
    IsEqualTo,
    IsNot,
    IsVisible,
    ReadsExactly,
)


def test_ask_for_list(Tester):
    """List uses .to_find_all() and returns a list"""
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)
    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_find_all.return_value = []

    Tester.should_see_the((List.of(fake_target), IsEmpty()))

    mocked_btw.to_find_all.assert_called_once_with(fake_target)


def test_is_empty_nonempty_list(Tester):
    """IsEmpty complains about a not-empty list"""
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)
    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_find_all.return_value = ["not", "empty"]

    with pytest.raises(AssertionError):
        Tester.should_see_the((List.of(fake_target), IsEmpty()))


def test_ask_for_number(Tester):
    """Number uses .to_find_all() and returns an int"""
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)
    return_value = [1, 2, 3]
    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_find_all.return_value = return_value

    Tester.should_see_the((Number.of(fake_target), IsEqualTo(len(return_value))))

    mocked_btw.to_find_all.assert_called_once_with(fake_target)


def test_is_equal_to_unequal_value(Tester):
    """IsEqual complains if the values are not equal"""
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)
    return_value = [1, 2, 3]
    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_find_all.return_value = return_value

    with pytest.raises(AssertionError):
        Tester.should_see_the(
            (Number.of(fake_target), IsEqualTo(len(return_value) + 3))
        )


@mock.patch("screenpy.questions.selected.SeleniumSelect")
def test_ask_for_selected(mocked_selenium_select, Tester):
    """Selected finds its target and gets the first_selected_option"""
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)
    return_value = "test"
    mocked_selenium_select.return_value.first_selected_option.text = return_value

    Tester.should_see_the(
        (Selected.option_from(fake_target), ReadsExactly(return_value))
    )

    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_find.assert_called_once_with(fake_target)


@mock.patch("screenpy.questions.selected.SeleniumSelect")
def test_reads_exactly_mismatched_string(mocked_selenium_select, Tester):
    """ReadsExactly complains if the strings do not match exactly"""
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)
    mocked_selenium_select.return_value.first_selected_option.text = "sentences"

    with pytest.raises(AssertionError):
        Tester.should_see_the(
            (Selected.option_from(fake_target), ReadsExactly("sandwiches"))
        )


def test_ask_for_text(Tester):
    """Text finds its target and gets its text"""
    text = "spam"
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)
    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_element = mock.Mock()
    mocked_element.text = f"{text} and eggs"
    mocked_btw.to_find.return_value = mocked_element

    Tester.should_see_the((Text.of_the(fake_target), ContainsTheText(text)))

    mocked_btw.to_find.assert_called_once_with(fake_target)


def test_ask_for_text_of_the_alert(Tester):
    """TextOfTheAlert gets the alert's text"""
    text = "spam"
    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_alert = mock.Mock()
    mocked_alert.text = f"{text} and eggs"
    mocked_btw.browser.switch_to.alert = mocked_alert

    Tester.should_see_the((TextOfTheAlert(), ContainsTheText(text)))


def test_contains_the_text_no_it_does_not(Tester):
    """ContainsTheText test fails if the substring does not exist"""
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)
    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_element = mock.Mock()
    mocked_element.text = "spam and eggs"
    mocked_btw.to_find.return_value = mocked_element

    with pytest.raises(AssertionError):
        Tester.should_see_the(
            (Text.of_the(fake_target), ContainsTheText("baked beans"))
        )


def test_is_not_negates(Tester):
    """IsNot negates the resolution it is passed"""
    fake_xpath = "//xpath"
    fake_target = Target.the("fake").located_by(fake_xpath)
    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.to_find_all.return_value = [1, 2, 3]

    Tester.should_see_the((List.of(fake_target), IsNot(Empty())))


def test_browser_title(Tester):
    """BrowserTitle asks for the browser's title"""
    fake_title = "ScreenPy's Totally Awesome Webpage!"
    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.browser.title = fake_title

    Tester.should_see_the((BrowserTitle(), ReadsExactly(fake_title)))


def test_browser_url(Tester):
    """BrowserURL asks for the browser's current_url"""
    fake_url = "http://www.screenpy.com"
    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_btw.browser.current_url = fake_url

    Tester.should_see_the((BrowserURL(), ReadsExactly(fake_url)))


def test_ask_for_element(Tester):
    """Element asks for, duh, an element"""
    fake_target = Target.the("fake").located_by("//html")
    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_element = mock.Mock()
    mocked_btw.to_find.return_value = mocked_element

    Tester.should_see_the((Element(fake_target), IsNot(EqualTo(None))))

    mocked_btw.to_find.assert_called_once_with(fake_target)


def test_visible_element(Tester):
    """IsVisible matches a visible element"""
    fake_target = Target.the("fake").located_by("//html")
    mocked_btw = Tester.ability_to(BrowseTheWeb)
    mocked_element = mock.Mock()
    mocked_element.is_displayed.return_value = True
    mocked_btw.to_find.return_value = mocked_element

    Tester.should_see_the((Element(fake_target), IsVisible()))


def test_body_of_the_last_response(APITester):
    """BodyOfTheLastResponse and ContainsTheEntry tests the JSON body"""
    test_json = {"play": "Hamlet"}
    fake_response = mock.Mock()
    fake_response.json.return_value = test_json
    mocked_mar = APITester.ability_to(MakeAPIRequests)
    mocked_mar.responses = [fake_response]

    APITester.should_see_the((BodyOfTheLastResponse(), ContainsTheEntry(**test_json)))


def test_contains_the_entries_multiple(APITester):
    """ContainsTheEntries can test multiple key/value pairs"""
    test_json = {"play": "Hamlet", "intermission": "1hr"}
    fake_response = mock.Mock()
    fake_response.json.return_value = test_json
    mocked_mar = APITester.ability_to(MakeAPIRequests)
    mocked_mar.responses = [fake_response]

    APITester.should_see_the(
        (BodyOfTheLastResponse(), ContainsTheEntries(**test_json))
    )


def test_cookies_api_dict(APITester):
    """Cookies returns a dict for actors who can MakeAPIRequests"""
    test_name = "cookie_type"
    test_value = "madeleine"
    test_cookie = {test_name: test_value}
    test_jar = RequestsCookieJar()
    test_jar.set(test_name, test_value)
    APITester.ability_to(MakeAPIRequests).session.cookies = test_jar

    APITester.should_see_the((Cookies(), ContainTheEntry(**test_cookie)))


def test_cookies_web_dict(Tester):
    """Cookies returns a dict for actors who can BrowseTheWeb"""
    test_name = "cookie_type"
    test_value = "madeleine"
    test_cookie = {test_name: test_value}
    Tester.ability_to(BrowseTheWeb).browser.get_cookies.return_value = [
        {"name": test_name, "value": test_value}
    ]

    Tester.should_see_the((Cookies(), ContainTheEntry(**test_cookie)))


def test_headers_returns_a_dict(APITester):
    """HeadersOfTheLastResponse returns a dict"""
    test_headers = {"Content-Type": "application/json"}
    mock_response = mock.Mock()
    mock_response.headers = test_headers
    APITester.ability_to(MakeAPIRequests).responses = [mock_response]

    APITester.should_see_the(
        (HeadersOfTheLastResponse(), ContainTheEntry(**test_headers))
    )


def test_status_code_of_the_last_response(APITester):
    test_status_code = 1337
    mock_response = mock.Mock()
    mock_response.status_code = test_status_code
    APITester.ability_to(MakeAPIRequests).responses = [mock_response]

    APITester.should_see_the(
        (StatusCodeOfTheLastResponse(), IsEqualTo(test_status_code))
    )
