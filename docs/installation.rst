Installation
============

To install ScreenPy,
run the following command
in a `virtual environment <https://docs.python.org/3/library/venv.html>`_:

``pip install screenpy``

Official Extensions
-------------------

There are several extensions to ScreenPy
which are officially recognized.
To install them,
use `pip's extras feature <https://www.python.org/dev/peps/pep-0508/#extras>`__.
You can install multiple options
by separating with commas:

``pip install "screenpy[selenium,requests,allure]"``

Selenium
++++++++

`ScreenpPy Selenium <https://screenpy-selenium-docs.readthedocs.io/en/latest/>`__
adds the Ability to ``BrowseTheWeb``
using `Selenium <https://www.selenium.dev/>`__.
It provides Actors
with several Actions,
Questions,
and Resolutions
to support testing web applications.

``pip install "screenpy[selenium]"``

Requests
++++++++

`ScreenPy Requests <https://screenpy-requests-docs.readthedocs.io/en/latest/>`__
adds the Ability to ``MakeAPIRequests``
using `Requests <https://docs.python-requests.org/en/latest/>`__.
It provides Actors
with several Actions and Questions
to support API testing.

``pip install "screenpy[requests]"``

Playwright
++++++++++

`ScreenPy Playwright <https://screenpy-playwright-docs.readthedocs.io/en/latest/>`__
adds the Ability to ``BrowseTheWebSynchronously``
using `Playwright <https://playwright.dev/>`__.
It provides Actors
with several Actions,
Questions,
and Resolutions
to support using Microsoft's webdriver.

``pip install "screenpy[playwright]"``

Appium
++++++

`ScreenPy Appium <https://screenpy-appium-docs.readthedocs.io/en/latest/>`__
adds the Abilities to ``UseAMobileDevice``,
``UseAnAndroidDevice``,
and ``UseAnIOSDevice``
using `Appium <https://appium.io/>`__.
It provides Actors
with several Actions,
Questions,
and Resolutions
to support mobile testing.

``pip install "screenpy[appium]"``

PyOTP
+++++

`ScreenPy PyOTP <https://screenpy-pyotp-docs.readthedocs.io/en/latest/>`__
adds the Ability to ``AuthenticateWith2FA``
using `PyOTP <https://github.com/pyauth/pyotp>`__.
It uh,
doesn't provide anything else...
currently.
But Actors can use their Ability
to get their 2FA token!
(It's also used by ``screenpy_selenium`` above.)

``pip install "screenpy[pyotp]"``

Allure
++++++

`ScreenPy Adapter: Allure <https://screenpy-adapter-allure-docs.readthedocs.io/en/latest/>`__
adds an Adapter for the :ref:`Narrator <narrator api>`
which enables logging through
`Allure <https://docs.qameta.io/allure-report/>`__.

``pip install "screenpy[allure]"``
