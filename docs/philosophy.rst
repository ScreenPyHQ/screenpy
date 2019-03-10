.. include global.rst
.. _philosophy:

Philosophy
==========

As mentioned a few times in this documentation, Screenplay Pattern uses *composition*. That means rather than setting up inheritance trees to pass abilities around, you will build your test suite by passing around a bunch of smaller, more focused objects that have no lineage (or at least very little lineage).

For example, take the following line from the quickstart page::
    perry = Actor.named("Perry").who_can(BrowseTheWeb.using(Firefox()))

:class:`|Actor|` and :class:`|BrowseTheWeb|` are both classes that inherit from `object`, nothing more. We've granted our Actor class an ability here. abilities can be used to perform various actions, without having to create a base class to provide all Actors with that ability. Each Actor will check to see if it has the ability the action requires to perform it, and will raise a :class:`|Actor|.UnableToPerform` exception if it doesn't have the right ability.

All of this was sort of in response to the wildfire popularity of Page Object Model. Page Object Model, by its very definition, violates the SOLID principles of Object Oriented programming, in particular the S (Single Responsibility Principle) and the O (Open/Closed Principle).

Think about the definition of what a Page Object is: it keeps track of the actions the user can do on the page, the locators of the elements on that page, sometimes the URL of the page, sometimes the driver itself, and the workflow between it and your other Page Objects. That is very far from a single responsibility, and if you've used Page Object Model to create large suites, you know how quickly they can balloon out of control if you don't limit your definition of "Page Object".

With Screenplay Pattern, the Page Object is slimmed down to only keep track of locators, maybe also a URL (which you could argue is the biggest locator of all). Admittedly, depending on how you structure your `user_interface` documents, you might need to edit this file in the above scenario. But you could instead create a new file in `user_interface` that is specifically for the login area instead, without violating your organization pattern.

The Open/Closed Principle states that your software should be "open for extension, but closed for modification." Let's say you've got a Homepage object with all your functionality. Now your team has added an Account system, with a login link on the homepage. You'll need to edit your Homepage object not only to add in locators for the new login links and fields, but also new methods and new workflow patterns.

The way to handle this situation with Screenplay Pattern is to create new tasks, create a new `user_interface` file, and write your new features. The old files, which were working before, will (probably) still be working after, since you never had to touch them.
