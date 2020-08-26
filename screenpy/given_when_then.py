"""
Given, When, and Then are Gherkin-style directives. The general idea is:

* given/given_that is for test setup or "arrange" steps.
* when is for test actions or the "act" steps.
* then is for test assertions or the "assert" steps.
* and_ can be used for continuations of any of the above.

All of these are identity functions, only used to provide a little extra
context to your tests. An example test flow might be:

    given(Perry).was_able_to(Start.on_the_homepage())
    and_(Perry).was_able_to(LoginSuccessfully.using(USERNAME, PASSWORD))
    when(Perry).attempts_to(Click.on_the(LOGOUT_BUTTON))
    then(Perry).should_see_the(
        (Text.of_the(BANNER_MESSAGE), ReadsExactly("Goodbye!"))
    )

[The Gherkin reference](https://docs.cucumber.io/gherkin/reference/) can
explain more.
"""


from .actor import Actor


def given(the_actor: Actor) -> Actor:
    """Typically used to designate "arrange" steps."""
    return the_actor


def given_that(the_actor: Actor) -> Actor:
    """Typically used to designate "arrange" steps."""
    return the_actor


def when(the_actor: Actor) -> Actor:
    """Typically used to designate the "act" steps."""
    return the_actor


def then(the_actor: Actor) -> Actor:
    """Typically used to designate the "assert" steps."""
    return the_actor


def and_(the_actor: Actor) -> Actor:
    """Can be used in place of given, when, or then as a continuation."""
    return the_actor
