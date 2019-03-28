"""
Given, When, and Then are Gherkin-style directives. The general idea is:

* `given`/`given_that` is for test setup steps.
* `when` is for test actions.
* `then` is for test assertions.
* `and_` can be used for continuations of any of the above.

All of these are identity functions, only used to provide a little extra
context to your tests. An example screenplay flow might be:

    given(perry).was_able_to(Start.on_the_homepage())
    and(perry).was_able_to(LoginSuccessfully.using(USERNAME, PASSWORD))
    when(perry).attempts_to(Click.on_the(LOGOUT_BUTTON))
    then(perry).should_see_the((Text.of(WELCOME_MESSAGE), ReadsExactly("Hello!")))

[The Gherkin reference](https://docs.cucumber.io/gherkin/reference/) can explain more.
"""


def given(the_actor: "Actor") -> "Actor":
    return the_actor


def given_that(the_actor: "Actor") -> "Actor":
    return the_actor


def when(the_actor: "Actor") -> "Actor":
    return the_actor


def then(the_actor: "Actor") -> "Actor":
    return the_actor


def and_(the_actor: "Actor") -> "Actor":
    return the_actor
