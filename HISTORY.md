Release History
===============

2.0.1 (2020-05-06)
------------------

### Improvements:

- Added try/except to Element question so it will return `None` if the element doesn't exist, which enables `IsNot(Visible())` or `IsNot(EqualTo(None))` to test for non-visibility/presence of an element.
- Moved BrowsingError to `screenpy.exceptions` too, missed that one!


2.0.0 (2020-05-05)
------------------

### Breaking Changes

- Removed `.then_wait_for` methods from Enter and Click.
- Removed all `to_switch_to...` methods from BrowseTheWeb, preferring to use the browser directly. Also removed `to_visit` and `to_get` from BrowseTheWeb for the same reason.
- Changed UnableToPerformError and UnableToActError to UnableToPerform and UnableToAct.
- Moved DeliveryError and TargetingError to `screenpy.exceptions` (though you can still technically import them from `screenpy.actor` and `screenpy.target`).
- Removed several syntactic sugar options that, upon retrospect, aren't really grammatically possible in this module.

### New Features

- Added *so many* new actions!
  - Added RefreshPage action.
  - Added GoBack action.
  - Added GoForward action.
  - Added SwitchToTab action. (It turns out SwitchTo didn't quite switch to all the things you needed to switch to.)
  - Added Chain action, to do chained actions! Such as these:
    - Added DoubleClick action.
    - Added RightClick action.
    - Added MoveMouse/Hover action.
    - Added HoldDown action.
    - Added Release action.
- Enabled several existing actions to be chained with the new Chain action:
  - Click
  - Enter
  - Enter2FAToken
  - Pause
- Added Element question, to test things about a specific element, such as...
- Added IsVisible resolution, to test if an element is visible!
- You can now see the same detailed logs without the Allure report if you wish! All the action is now logged at INFO level. Try adding `--log-cli-level=INFO` to your `pytest` run, for example!

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
- Added Pause action, for those times you *really* need it.
- Added Debug action, to drop a debugger in the middle of a chain of actions/tasks.
- Added SwitchTo action, to switch to iframes, back to the default frame, and whatever else you need to switch to.
- Added AcceptAlert/DismissAlert/RespondToPrompt to support any javascript alert actions you could want.

### Improvements

- Added a bunch of new syntactic sugar and default options.
- Added a new method to Target that will allow you to pass in your own locator tuple, like `Target.located((By.LINK_TEXT, "click me"))`
- Added additional logging to improve debugging experience.
- Added custom exceptions with exception chaining to provide more context when tests break.
- HUGE documentation improvement.
- Typed ScreenPy, and marked ScreenPy as being typed!

### Fixes

- Fixed strange grammar in logged resolution lines.

### Deprecations

- Deprecated the "then_wait_for" methods on Click and Enter now that we have a Wait class. These methods will be removed in 2.0.0.


0.4.0 (2019-11-04)
------------------

### New Features

- Added the Wait action, which enables the actor to wait for a target to be visible, invisible, or contain expected text.
- Added the Clear action, which enables the actor to clear text from an input field.


0.3.0 (2019-08-18)
------------------

### Improvements

- Added import magic to make importing actions, resolutions, targets, ... everything! easier.
- Added some natural-language-enabling syntactic sugar to resolutions.
- Added some extra flavor to actors being created because i can't help myself.


0.2.0 (2019-04-13)
------------------

### New Features

- Added "the-internet" example
- Added `Selected` question

### Improvements

- Adjusted strategy for multi-target Text question
- Added more consistency in coding style

### Bugfix

- Fixed issues with Select actions


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
- Added `List` question.

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

