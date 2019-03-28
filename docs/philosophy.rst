.. _philosophy:

Philosophy
==========

As mentioned a few times in this documentation, Screenplay Pattern uses *composition*. That means rather than setting up inheritance trees to pass abilities around, you will build your test suite by passing around a bunch of smaller, more focused objects that have no lineage (or at least very little lineage).

For example, take the following line from the quickstart page::

    perry = AnActor.named("Perry").who_can(BrowseTheWeb.using(Firefox()))

|Actor| and |BrowseTheWeb| are both classes that inherit from `object`, nothing more. We've granted our Actor class an ability here. abilities can be used to perform various actions, without having to create a base class to provide all Actors with that ability.

On top of that, the structure of the line makes it reach almost exactly like English with just a few extra punctuation sprinkled in. That provides a truly valuable level of readability both for code maintainers and for QA engineers, managers, BAs, and anyone else in your team who wants to know what these tests are doing.

Relation to Page Object Model
-----------------------------

In the later days of Selenium's incipience, when folks really started using the library, the committers at Selenium were being bombarded by bug reports complaining about flaky tests and inconsistent runs. The test writers were seeing their scripts fail intermittently and believed it was because Selenium was a faulty library.

After (presumably panicked) investigation, those Selenium folks were absolutely certain that the problem wasn't with Selenium—at least not most of them—but with the way these test writers were writing their test scripts. Some of the people tasked with doing Automated QA had never programmed before, so they were falling into every pitfall imaginable: magic strings, DRY, YAGNI, the whole lot.

So, Simon Stewart wrote an article detailing Page Object Model, a beginner-friendly introduction to a more maintainable test suite. Very quickly there were articles, videos, and webinars encouraging everyone to ensure they were using Page Object Model to architect their test suites, because switching to a strict adherence to that model fixed all the flaky test issues for many test writers.

Screenplay Pattern's inception was in response to the wildfire popularity of Page Object Model. Page Object Model, by its very definition, violates the SOLID principles of Object Oriented programming, in particular the S (Single Responsibility Principle) and the O (Open/Closed Principle).

Comparison Between POM and SPP
------------------------------

Think about the definition of what a Page Object is. It keeps track of::

* The actions the user can do on the page
* The locators of the elements on that page
* Sometimes the URL of the page
* Sometimes the driver itself
* The workflow between it and your other Page Objects.

That is very far from a single responsibility, and if you've used Page Object Model to create large suites, you know how quickly they can balloon out of control if you don't limit your definition of "Page Object".

With Screenplay Pattern, the Page Object is slimmed down to only keep track of locators, maybe also a URL (which you could argue is the biggest locator of all). Admittedly, depending on how you structure your `user_interface` documents, you might need to edit this file in the above scenario.

The Open/Closed Principle states that your software should be "open for extension, but closed for modification." Let's say you've got a Homepage object with all your functionality. Now your team has added an Account system, with a login link on the homepage. You'll need to edit your Homepage object not only to add in locators for the new login links and fields, but also new methods and new workflow patterns.

The way to handle this situation with Screenplay Pattern is to create new tasks, create a new `user_interface` file, and write your new features. The old files, which were working before, will (probably) still be working after, since you never had to touch them.

If you're coming from experience with Page Object Model, you're probably used to seeing relatively few, beefy files. The files of Screenplay Pattern will feel downright *barren* at first, yet crowded at the same time. Compared to Page Object Model, Screenplay Pattern has an infestation of .py files that are all barely a couple dozen of lines long in some cases. This is normal! The files are more focused, and thus easier to digest and organize.
