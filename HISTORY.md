Release History
===============

4.0.0 (2022-02-22)
------------------

2day is 2sday, by the way.

### Breaking Changes

- ScreenPy is now broken up in2 its core (this repository), `screenpy_selenium`, `screenpy_requests`, `screenpy_pyotp`, and `screenpy_adapter_allure`. This will cause some big, big breakages in your suites, and i'm very sorry about it. To help get you back up and running, see the changes at https://screenpy-docs.readthedocs.io/en/latest/deprecations.html#breaking-changes
- Those deprecated methods mentioned above on that same page are also finally removed.

### Documentation

- Yet another rewrite of the documentation! This time it's much more focused, since the documentation is only for the base module.
- The rewrite includes a new Complete Example section, which shows a fictional example of a ScreenPy test file and breaks down each part of it.

### Improvements

- Eventually now also tells you how many times it attempted its performable, which could be useful for debugging in certain situations.

### Bugfixes

- If `See` was given a value to compare against a Resolution, the value is now properly printed to the log instead of just the string "{value}". :facepalm:

3.2.9 (2021-12-23)
------------------

### Improvements

- Added `.of_the_first_of_the` aliases to several Actions and Questions, to allow for clearer readings of tests.
- Added an `aside` of the actual value when `See` is about to compare a pre-baked value instead of asking a Question.
- Fixed `IsNot`'s descriptions, especially when they were describing when the negative (... of the negative).

3.2.8 (2021-11-11)
------------------

### Bugfixes

- Fixes the Narrator skipping narrations if they occurred within a double-kinked cable. In fact, completely rewrote how the Narrator handles multiple cable kinks in a much more understandable way (h/t @bandophahita).


3.2.7 (2021-10-21)
------------------

### Bugfixes

- Another bugfix for the Narrator when reporting errors -- if the user isn't using Allure, an error in the script would cause a `StopIteration` error to be raised aftewards. Pretty annoying when debugging!
- Speaking of errors being raised, if an error were raised while the Narrator's mic cable was kinked or while the Narrator was off the air, the Narrator would *never narrate again* (until the next script ran anyway). That's fixed!

### Improvements

- Fixed up the quick hackjob for narrating errors to put it in a much more elegant spot.

3.2.6 (2021-10-15)
------------------

### Bugfixes

- Kind of critical bugfix for the Narrator's new ability to report errors -- the Narrator now only reports errors if their mic cable is not kinked and they are on air. This was causing some pretty unfortunate interactions with `Eventually`...


3.2.5 (2021-10-14)
------------------

### Bugfixes

- The `clean_up` method that all Actors use to clean up after themselves was mutating the cleanup task list as it was iterating through it. This was not good! Actors have been reminded of proper looping etiquette.

### Improvements

- `Eventually` now raises a `DeliveryError` to bring it in line with `Wait` and all other Actions which raise errors.
- `Eventually` now mentions all of the exceptions it encountered when it raises `DeliveryError`.
- Several Actions have less-awkwardly-worded `beat`s!

3.2.4 (2021-09-30)
------------------

### Bugfixes

- `MakeNote` and `See` both relied on catching an `AttributeError` to figure out if they had been passed a value or a Question. But if the Question itself encountered an `AttributeError` while being answered, a very confusing situation would arise that was very annoying to debug. Now these two Actions use `hasattr` instead!
- The `AllureAdapter` is no longer falsely marking steps which failed as having passed! Bringin' back them reds and yellows.

### New Features

- The `Adapter` protocol now supports an `error` method, which allows adapters to report exceptions in their own way.

3.2.3 (2021-09-27)
------------------

### Bugfixes

- Toned down the aggressive pruning by `get_additive_description`. It was cutting off closing quotes!
- Fixed the incorrect method being called when attaching in the `AllureAdapter`.

### New Features

- Added some nice new Actions for reporting: `AttachTheFile`, `SaveScreenshot`, and `SaveConsoleLog`!

3.2.2 (2021-09-26)
------------------

### New Features

- `Eventually` and `See` now have beats! They try their best to make a natural-sounding English statement about what your Actor is doing, but if you need to tweak the message...
- Performables and Answerables may now have a `describe` function, which `Eventually` and `See` both directly use.
- Narrators can now `attach` files! Calling Narrator's `attach` method will broadcast the filepath to all the adapters plugged into their microphone. Adapters can look for specific keywords, if needed—all other adapters will ignore those keywords.

### Known Issues

- I was not able to figure out how to fix the problem with the Allure reporting, [#74](https://github.com/perrygoy/screenpy/issues/74). :( (_**Edit**: This is Perry from the Future! I figured it out!_)

3.2.1 (2021-08-29)
------------------

### Bugfixes

- Updated `See` and `MakeNote` typehints now that they allow for bare values *and* Questions.

3.2.0 (2021-08-23)
------------------

### Breaking Changes

- The gravitas levels have moved from `screenpy.pacing` to `screenpy.narration.narrator`, and they've also changed terminology. The updated terminology is more generic, describing how serious the gravitas is. The gravitas level is passed along to the adapters to be used or ignored as needed.

### New Features

- Added a `Narrator` class, who handles all the reporting! The Narrator's microphone can be outfitted with different adapters to report to whatever reporting service you want. Included are the new `AllureAdapter` and `StdOutAdapter`, which will maintain existing behavior.
- (h/t @langgaibo) Added an `IsCloseTo` resolution!
- (h/t @bandophahita) Added an `Eventually` action!

### Improvements

- Part of the above `Narrator` addition is that there is now a way for you to manually control logging, either by putting the narrator `off_the_air` or by making their `microphone_cable_kinked`. It was immediately handy for `Eventually`, maybe you'll find it useful, too!
- Better typehints for `Target`!
- Better `beat` for `MakeNote`!
- `See` and `MakeNote` can now both accept values *and* Questions!

### Bugfixes

- XPATH locators which begin with a parenthesis are now correctly recognized as XPATH locators.

3.1.2 (2021-04-13)
------------------

### Improvements

- I'm on a tear, eh?
- Added a more useful test in `screenpy-quickstart` that shows off more actions.
- Adjusted the return type of the `noted_under` direction from `object` to `Any`. I think it could be something more specific, but `Any` is the best i've got for now.

3.1.1 (2021-04-12)
------------------

### Improvements

- Added `.of_all` method to the **Attribute** Question because that is, incidentally, the way i needed to be able to use it. Woops!

3.1.0 (2021-04-11)
------------------

### New Features

- (h/t @langgaibo and @sramdas-dod) Actors can now clean up after themselves! Give 'em a task with `.has_cleanup_task(CleanUpTask())` and they'll do the `CleanUpTask()` task as they exit. Or sooner, if you call `Actor.cleans_up()` yourself! (`CleanUpTask` not included.)
- (h/t @langgaibo) Actors can now take notes and use them... anywhere. The new **MakeNote** Action allows you to save the answer to a Question under a handy key, which can then be recalled later using the `noted_under` direction! Which brings me to...
- The Director! The Director is omnipresent and singular. They are always watching, waiting to take or give a needed note. Ask for one by using a `the_noted(key)` or `noted_under(key)` direction, wherever you need the information they hold. 🔺👁🔺
- Added the **See**, **SeeAllOf**, and **SeeAnyOf** Actions, to relieve Actors of the burden of asserting. Take a look at the new [Deprecations](https://screenpy-docs.readthedocs.io/en/latest/deprecations.html#id3) docs page to learn more.
- Added the **Attribute** Question, to ask about an element's attributes. Like "value", which is the one i'll be asking about.

### Improvements

- (h/t @WandyYing and @bandophahita) SOLIDified Actors a little bit more by deprecating their asserting responsibility. This was part of adding the new **See** etc. Actions mentioned above. Actors now have a `should` method, which is really just an alias for `was_able_to` and `attempts_to`, but is meant to be used with that **See** Action. Or not, it's really up to you.
- Targets can now be used as if they themselves were locator tuples. You can do `target[0]` and pass in `*target`s. It's wild! And cleans up a really gross list comprehension from the **Wait** source code.
- As ever, another huge documentation update. Things should be more consistent now. Maybe. (I'll probably find more things to smooth out as soon as i commit this.) (*Edit*: i did.)

### Deprecations

- Deprecated `Actor.should_see_the` and `Actor.should_see_any_of` in favor of using `Actor.should` with the new **See**, **SeeAllOf**, and **SeeAnyOf** Actions. These methods will be removed in 4.0.0. Instructions for modifying your tests can be found in the [3.1.0 Deprecations documentation](https://screenpy-docs.readthedocs.io/en/latest/deprecations.html#id3)


3.0.4 (2021-03-09)
------------------

### Bug Fixes

- Missed a `from typing import Protocol`, that's fixed now. Woops!

3.0.3 (2021-03-09)
------------------

### Improvements

- (h/t @bandophahita) CLI logging now has indentation levels to help show which statements are encapsulated by Questions, tasks, Actions, etc.!
- Reverted the `Protocol` import from `typing` back to `typing_extensions` for better compatibility. This will be revisited when Python 4 is released, probably.

### New Features

- (h/t @bandophahita) New **IsClickable** Resolution to check if an element is clickable!

3.0.2 (2021-02-28)
------------------

### Improvements

- **Wait** now only puts *one* "..." at the end of its messages. :eye_roll:
- `mypy` will now be looking at the `examples/` directory as well, so it can catch errors like...

### Bugfixes

-  (h/t @bandophahita) Removed the **BaseAction**, **BaseAbility**, and **BaseQuestion** classes, for *sure* this time.
- `mypy` should no longer complain whenever you use any of the **SendMETHODRequest** API request Actions (e.g. **SendGETRequest**, **SendPOSTRequest**, etc.).

3.0.1 (2021-02-18)
------------------

### Improvements

- **Wait** can do custom log messages again, to make the reports look nicer.

### Bug Fixes

- **Element** now catches the correct exception type, now that Target's the one doing the finding.
- **Wait** now formats its custom exception correctly.
- What's a release without some same-day bug fixes, right?

3.0.0 (2021-02-18)
------------------

### Breaking Changes

- **BrowseTheWeb** no longer has `.to_find()` or `.to_wait_for()`. I realized these methods actually break the S in SOLID, and these methods were limiting Actions from really doing what they're supposed to do. See the Improvements section below for the direct benefit of this change!

### Improvements

- **Wait** can now use strategies that don't use a Target, or have multiple arguments. You can now use any of Selenium's URL-monitoring expected conditions or any other custom strategies through `Wait().using(strategy).with_("any", "number", "of", "args")`!
- **AddHeader** can now accept new forms of header-setting arguments, like a dict or just alternating pairs. Now `AddHeader(Cookie="yes=please")` == `AddHeader({"Cookie": "yes=please"})` == `AddHeader("Cookie", "yes=please")`!
- Added **SetHeaders** Action, if you want to set the headers *exactly* (and remove all unmentioned headers).
- **AddHeader**, **SetHeaders**, and **Send\[METHOD\]Request** Actions now all have a way to mark their contents as secret, so they won't be logged. Add a `.which_should_be_kept_secret()` or `.secretly()` to the end and the log won't mention the unmentionables.
- I did another docs overhaul, this time making them read in a way that might please [Hemingway](http://www.hemingwayapp.com/).

### Bug Fixes

- **Click** is now able to be chained without a Target to click. This was preventing clicking at an offset, which annoyed *me* at least.


2.2.0 (2020-11-29)
------------------

### Improvements

- Updated all the dependencies to support Python 3.9! Kind of a boring update.
- Made the reported Actions more consistently worded.

2.1.0 (2020-09-03)
------------------

### Breaking Changes

- Removed `on_top` method from **SwitchToTab**, it wasn't consistent under certain circumstances and that could be misleading.
- Removed the **BaseAction**, **BaseAbility**, and **BaseQuestion** classes in favor of Protocols.

### New Features

- Added API testing support!
  - Added **MakeAPIRequests** Ability.
  - Added **SendGETRequest**, **SendPOSTRequest**, **SendPATCHRequest**, **SendPUTRequest**, **SendOPTIONSRequest**, **SendHEADRequest**, **SendDELETERequest**, and **SendAPIRequest** Actions.
  - Added **AddHeader**/**AddHeaders** Action.
  - Added **Cookies**, **CookiesOnTheWebSession**, **CookiesOnTheAPISession** Questions.
  - Added **StatusCodeOfTheLastResponse** Question.
  - Added **BodyOfTheLastResponse** Question.
  - Added **HeadersOfTheLastResponse** Question.
  - Added **ContainsTheKey**, **ContainsTheValue**, **ContainsTheEntry** Resolutions.
- Added `should_see_any_of` assertion method to Actors, which is similar to `should_see_the` but passes if *at least* one of its tests are true, instead of all of them.
- Added **HasLength** Resolution, for fun.
- Added a "cookbook" section to the docs to give examples of common use-cases.

### Improvements:

- *Huge* docs overhaul, aimed at reducing word count and increasing word value.
- Switched to using Protocols for type hinting instead of base classes.
- **IsVisible** Resolution now has a nicer mismatch message.

### Bugfixes:

- Fixed a timing issue with **has_method_with_return_value** where the return value could change by the time the mismatch message was being written to the log, which made it look like a passing test was failing.
- Fixed `SwitchTo.default()` logging a very metaphysical "{The Actor} switches to the None".
- Fixed **Enter**'s logging when `then_hits` is used to hit a key without a nice text representation (like "Return").
- Fixed a small collection of copy/paste errors in documentation and logged strings.

2.0.1 (2020-05-10)
------------------

### Improvements:

- Added try/except to the **Element** Question so it will return `None` if the element doesn't exist, which enables `IsNot(Visible())` or `IsNot(EqualTo(None))` to test for non-visibility/presence of an element.
- Moved **BrowsingError** to `screenpy.exceptions` too, missed that one!


2.0.0 (2020-05-05)
------------------

### Breaking Changes

- Removed `.then_wait_for` methods from **Enter** and **Click**.
- Removed all `to_switch_to...` methods from **BrowseTheWeb**, preferring to use the browser directly. Also removed `to_visit` and `to_get` from **BrowseTheWeb** for the same reason.
- Changed **UnableToPerformError** and **UnableToActError** to **UnableToPerform** and **UnableToAct**.
- Moved **DeliveryError** and **TargetingError** to `screenpy.exceptions` (though you can still technically import them from `screenpy.actor` and `screenpy.target`).
- Removed several syntactic sugar options that, upon retrospect, aren't really grammatically possible in this module.

### New Features

- Added *so many* new Actions!
  - Added **RefreshPage** Action.
  - Added **GoBack** Action.
  - Added **GoForward** Action.
  - Added **SwitchToTab** Action. (It turns out **SwitchTo** didn't quite switch to all the things you needed to switch to.)
  - Added **Chain** Action, to do chained Actions! Such as these:
    - Added **DoubleClick** Action.
    - Added **RightClick** Action.
    - Added **MoveMouse**/**Hover** Action.
    - Added **HoldDown** Action.
    - Added **Release** Action.
- Enabled several existing Actions to be chained with the new **Chain** Action:
  - **Click**
  - **Enter**
  - **Enter2FAToken**
  - **Pause**
- Added **Element** Question, to test things about a specific element, such as...
- Added **IsVisible** Resolution, to test if an element is visible!
- You can now see the same detailed logs without the Allure report if you wish! All the Action is now logged at INFO level. Try adding `--log-cli-level=INFO` to your `pytest` run, for example!

### Improvements

- Cleaned up a lot of documentation.
- Updated the `screenpy-quickstart` script to better reflect the current state and recommendations.

### Fixes

- Fixed a strange issue that prevented Allure from properly naming the acts and scenes in the Behavior view.

1.0.1 (2020-02-25)
------------------

### Improvements

- "Properly" typed ScreenPy. It could probably be done a little better, though.

1.0.0 (2020-02-17)
------------------

### New Features

- Added IOS and Android browser support! 🎉 (Will add full Appium support later!)
- Added **Pause** Action, for those times you *really* need it.
- Added **Debug** Action, to drop a debugger in the middle of a chain of Actions/tasks.
- Added **SwitchTo** Action, to switch to iframes, back to the default frame, and whatever else you need to switch to.
- Added **AcceptAlert**/**DismissAlert**/**RespondToPrompt** to support any javascript alert Actions you could want.

### Improvements

- Added a bunch of new syntactic sugar and default options.
- Added a new method to Target that will allow you to pass in your own locator tuple, like `Target.located((By.LINK_TEXT, "click me"))`
- Added additional logging to improve debugging experience.
- Added custom exceptions with exception chaining to provide more context when tests break.
- HUGE documentation improvement.
- Typed ScreenPy, and marked ScreenPy as being typed!

### Fixes

- Fixed strange grammar in logged Resolution lines.

### Deprecations

- Deprecated the `then_wait_for` methods on **Click** and **Enter** now that we have a **Wait** Action. These methods will be removed in 2.0.0. Instructions for modifying your tests can be found in the [1.0.0 Deprecations documentation](https://screenpy-docs.readthedocs.io/en/latest/deprecations.html#id2)


0.4.0 (2019-11-04)
------------------

### New Features

- Added the **Wait** Action, which enables the Actor to wait for a Target to be visible, invisible, or contain expected text.
- Added the **Clear** Action, which enables the Actor to clear text from an input field.


0.3.0 (2019-08-18)
------------------

### Improvements

- Added import magic to make importing Actions, Resolutions, Targets, ... everything! easier.
- Added some natural-language-enabling syntactic sugar to Resolutions.
- Added some extra flavor to Actors being created because i can't help myself.


0.2.0 (2019-04-13)
------------------

### New Features

- Added "the-internet" example
- Added **Selected** Question

### Improvements

- Adjusted strategy for multi-Target **Text** Question
- Added more consistency in coding style

### Bugfix

- Fixed issues with **Select** Actions


0.1.4 (2019-03-28)
------------------

### Bugfix

- Fixed a lot of issues with documentation. I _think_ i understand reStructured Text now. Mostly.


0.1.3 (2019-03-09)
------------------

### Bugfix

- Fixed call to old keyword argument. Woops.


0.1.2 (2019-03-09)
------------------

### New Features

- Added more Resolutions.
- Added **List** Question.

### Improvements

- Added more syntactic sugar.
- May have gone overboard with additional theming.

### Documentation

- Added Sphinx documentation!
- Added docstrings and type hints across the board.
- Reorganized method lists to be more consistent.

### Bugfix

- Fixed missing requirements installation in setup.py


0.1.0 (2019-03-08)
------------------

### Timeline

- Upload to personal git repository
- Publish to PyPI
- Too little sleep


0.0.1 (2016-11-23)
------------------

### Timeline

- Conception
- Demo to coworkers

