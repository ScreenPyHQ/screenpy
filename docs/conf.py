# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../"))
sys.path.insert(0, os.path.abspath("../env/lib/python3.7/site-packages/"))

autodoc_mock_imports = ["hamcrest", "allure"]

# -- Project information -----------------------------------------------------

project = "ScreenPy"
copyright = "2019, Perry Goy"
author = "Perry Goy"

# The short X.Y version
version = ""
# The full version, including alpha/beta/rc tags
release = "0.2.0"


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx.ext.ifconfig",
    "sphinx.ext.napoleon",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

rst_prolog = """.. Internal references
.. .. Exceptions
.. |DeliveryError| replace:: :class:`~screenpy.exceptions.DeliveryError`
.. |UnableToAct| replace:: :class:`~screenpy.exceptions.UnableToAct`
.. |UnableToPerform| replace:: :class:`~screenpy.actor.UnableToPerform`

.. .. Actors
.. |Actor| replace:: :class:`~screenpy.actor.Actor`
.. |Actor.named| replace:: :meth:`~screenpy.actor.Actor.named`
.. |Actor.who_can| replace:: :meth:`~screenpy.actor.Actor.who_can`
.. |Actor.can| replace:: :meth:`~screenpy.actor.Actor.can`
.. |Actor.uses_ability_to| replace:: :meth:`~screenpy.actor.Actor.uses_ability_to`
.. |Actor.attempts_to| replace:: :meth:`~screenpy.actor.Actor.attempts_to`
.. |Actor.should_see_that| replace:: :meth:`~screenpy.actor.Actor.should_see_that`
.. |Actor.should_see_the| replace:: :meth:`~screenpy.actor.Actor.should_see_the`
.. |Actor.exit| replace:: :meth:`~screenpy.actor.Actor.exit`

.. .. Targets
.. |Target| replace:: :class:`~screenpy.target.Target`
.. |Target.the| replace:: :meth:`~screenpy.target.Target.the`
.. |Target.located_by| replace:: :meth:`~screenpy.target.Target.located_by`

.. .. Abilities
.. |AuthenticateWith2FA| replace:: :class:`~screenpy.abilities.authenticate_with_2fa.AuthenticateWith2FA`
.. |AuthenticateWith2FA.using| replace:: :meth:`~screenpy.abilities.authenticate_with_2fa.AuthenticateWith2FA.using`
.. |AuthenticateWith2FA.using_secret| replace:: :meth:`~screenpy.abilities.authenticate_with_2fa.AuthenticateWith2FA.using_secret`
.. |BrowseTheWeb| replace:: :class:`~screenpy.abilities.browse_the_web.BrowseTheWeb`
.. |BrowseTheWeb.using| replace:: :meth:`~screenpy.abilities.browse_the_web.BrowseTheWeb.using`
.. |BrowseTheWeb.to_find| replace:: :meth:`~screenpy.abilities.browse_the_web.BrowseTheWeb.to_find`
.. |BrowseTheWeb.to_find_all| replace:: :meth:`~screenpy.abilities.browse_the_web.BrowseTheWeb.to_find_all`
.. |BrowseTheWeb.to_get| replace:: :meth:`~screenpy.abilities.browse_the_web.BrowseTheWeb.to_get`
.. |BrowseTheWeb.to_wait_for| replace:: :meth:`~screenpy.abilities.browse_the_web.BrowseTheWeb.to_wait_for`
.. |BrowseTheWeb.forget| replace:: :meth:`~screenpy.abilities.browse_the_web.BrowseTheWeb.forget`
.. |BrowseTheWeb.wait_for| replace:: :meth:`~screenpy.abilities.browse_the_web.BrowseTheWeb.wait_for`
.. |MakeAPIRequests| replace:: :class:`~screenpy.abilities.make_api_requests.MakeAPIRequests`

.. .. Actions
.. |Action| replace:: :ref:`actions`
.. |AcceptAlert| replace:: :class:`~screenpy.actions.web.accept_alert.AcceptAlert`
.. |Chain| replace:: :class:`~screenpy.actions.web.chain.Chain`
.. |Clear| replace:: :class:`~screenpy.actions.web.clear.Clear`
.. |Clear.the_text_from| replace:: :meth:`~screenpy.actions.web.clear.Clear.the_text_from`
.. |Clear.the_text_from_the| replace:: :meth:`~screenpy.actions.web.clear.Clear.the_text_from_the`
.. |Click| replace:: :class:`~screenpy.actions.web.click.Click`
.. |Click.on| replace:: :meth:`~screenpy.actions.web.click.Click.on`
.. |Click.on_the| replace:: :meth:`~screenpy.actions.web.click.Click.on_the`
.. |Click.then_wait_for| replace:: :meth:`~screenpy.actions.web.click.Click.then_wait_for`
.. |Click.then_wait_for_the| replace:: :meth:`~screenpy.actions.web.click.Click.then_wait_for_the`
.. |Click.perform_as| replace:: :meth:`~screenpy.actions.web.click.Click.perform_as`
.. |Debug| replace:: :class:`~screenpy.actions.web.debug.Debug`
.. |DismissAlert| replace:: :class:`~screenpy.actions.web.dismiss_alert.DismissAlert`
.. |DoubleClick| replace:: :class:`~screenpy.actions.web.double_click.DoubleClick`
.. |DoubleClick.on| replace:: :meth:`~screenpy.actions.web.double_click.DoubleClick.on`
.. |DoubleClick.on_the| replace:: :meth:`~screenpy.actions.web.double_click.DoubleClick.on_the`
.. |Enter| replace:: :class:`~screenpy.actions.web.enter.Enter`
.. |Enter.the_text| replace:: :meth:`~screenpy.actions.web.enter.Enter.the_text`
.. |Enter.the_secret| replace:: :meth:`~screenpy.actions.web.enter.Enter.the_secret`
.. |Enter.into| replace:: :meth:`~screenpy.actions.web.enter.Enter.into`
.. |Enter.then_hit| replace:: :meth:`~screenpy.actions.web.enter.Enter.then_hit`
.. |Enter.then_wait_for| replace:: :meth:`~screenpy.actions.web.enter.Enter.then_wait_for`
.. |Enter2FAToken| replace:: :class:`~screenpy.actions.web.enter_2fa_token.Enter2FAToken`
.. |Enter2FAToken.into| replace:: :meth:`~screenpy.actions.web.enter_2fa_token.Enter2FAToken.into`
.. |Enter2FAToken.into_the| replace:: :meth:`~screenpy.actions.web.enter_2fa_token.Enter2FAToken.into_the`
.. |HoldDown| replace:: :class:`~screenpy.actions.web.hold_down.HoldDown`
.. |HoldDown.on_the| replace:: :meth:`~screenpy.actions.web.hold_down.HoldDown.on_the`
.. |MoveMouse| replace:: :class:`~screenpy.actions.web.move_mouse.MoveMouse`
.. |Open| replace:: :class:`~screenpy.actions.web.open.Open`
.. |Open.browser_on| replace:: :meth:`~screenpy.actions.web.open.Open.browser_on`
.. |Pause| replace:: :class:`~screenpy.actions.web.pause.Pause`
.. |Pause.for_| replace:: :meth:`~screenpy.actions.web.pause.Pause.for_`
.. |Release| replace:: :class:`~screenpy.actions.web.release.Release`
.. |RespondToThePrompt| replace:: :class:`~screenpy.actions.web.respond_to_the_text.RespondToTheText`
.. |RespondToThePrompt.with_| replace:: :meth:`~screenpy.actions.web.respond_to_the_text.RespondToTheText.with_`
.. |RightClick| replace:: :class:`~screenpy.actions.web.right_click.RightClick`
.. |RightClick.on| replace:: :meth:`~screenpy.actions.web.right_click.RightClick.on`
.. |RightClick.on_the| replace:: :meth:`~screenpy.actions.web.right_click.RightClick.on_the`
.. |Select| replace:: :class:`~screenpy.actions.web.select.Select`
.. |Select.the_option_named| replace:: :meth:`~screenpy.actions.web.select.Select.the_option_named`
.. |Select.the_option_at_index| replace:: :meth:`~screenpy.actions.web.select.Select.the_option_at_index`
.. |Select.the_option_with_value| replace:: :meth:`~screenpy.actions.web.select.Select.the_option_with_value`
.. |SelectByText| replace:: :class:`~screenpy.actions.web.select.SelectByText`
.. |SelectByText.from_the| replace:: :meth:`~screenpy.actions.web.select.SelectByText.from_the`
.. |SelectByIndex| replace:: :class:`~screenpy.actions.web.select.SelectByIndex`
.. |SelectByIndex.from_the| replace:: :meth:`~screenpy.actions.web.select.SelectByIndex.from_the`
.. |SelectByValue| replace:: :class:`~screenpy.actions.web.select.SelectByValue`
.. |SelectByValue.from_the| replace:: :meth:`~screenpy.actions.web.select.SelectByValue.from_the`
.. |SendAPIRequest| replace:: :class:`~screenpy.actions.api.send_api_request.SendAPIRequest`
.. |SwitchTo| replace:: :class:`~screenpy.actions.web.switch_to.SwitchTo`
.. |SwitchTo.the| replace:: :meth:`~screenpy.actions.web.switch_to.SwitchTo.the`
.. |SwitchTo.default| replace:: :meth:`~screenpy.actions.web.switch_to.SwitchTo.default`
.. |SwitchToTab| replace:: :class:`~screenpy.actions.web.switch_to_tab.SwitchToTab`
.. |SwitchToTab.on_top| replace:: :meth:`~screenpy.actions.web.switch_to_tab.SwitchToTab.on_top`
.. |Wait| replace:: :class:`~screenpy.actions.web.wait.Wait`
.. |Wait.for_| replace:: :meth:`~screenpy.actions.web.wait.Wait.for_`
.. |Wait.seconds_for| replace:: :meth:`~screenpy.actions.web.wait.Wait.seconds_for`
.. |Wait.for_the| replace:: :meth:`~screenpy.actions.web.wait.Wait.for_the`
.. |wait.to_appear| replace:: :meth:`~screenpy.actions.web.wait.Wait.to_appear`

.. .. Questions
.. |Question| replace:: :ref:`questions`
.. |List| replace:: :class:`~screenpy.questions.list.List`
.. |List.of| replace:: :meth:`~screenpy.questions.list.List.of`
.. |List.of_all| replace:: :meth:`~screenpy.questions.list.List.of_all`
.. |Number| replace:: :class:`~screenpy.questions.number.Number`
.. |Number.of| replace:: :meth:`~screenpy.questions.number.Number.of`
.. |Text| replace:: :class:`~screenpy.questions.text.Text`
.. |Text.of| replace:: :meth:`~screenpy.questions.text.Text.of`
.. |Text.of_all| replace:: :meth:`~screenpy.questions.text.Text.of_all`
.. |Text.answered_by| replace:: :meth:`~screenpy.questions.text.Text.answered_by`
.. |Selected| replace:: :class:`~screenpy.questions.selected.Selected`
.. |Selected.option_from| replace:: :class:`~screenpy.questions.selected.Selected.option_from`
.. |Selected.options_from| replace:: :class:`~screenpy.questions.selected.Selected.option_from`
.. |Selected.answered_by| replace:: :class:`~screenpy.questions.selected.Selected.answered_by`

.. .. Resolutions
.. |Resolution| replace:: :ref:`resolutions`
.. |BaseResolution| replace:: :class:`~screenpy.resolutions.base_resolution.BaseResolution`
.. |ReadsExactly| replace:: :class:`~screenpy.resolutions.reads_exactly.ReadsExactly`

.. External references
.. .. Selenium
.. |Selenium| replace:: `Selenium <https://selenium-python.readthedocs.io/>`__
.. |ActionChains| replace:: `ActionChains <https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains>`__
.. |WebDriver| replace:: `WebDriver <https://seleniumhq.github.io/selenium/docs/api/py/api.html>`__
.. |WebElement| replace:: `WebElement <https://seleniumhq.github.io/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webelement.html#module-selenium.webdriver.remote.webelement>`__
.. |Alert| replace:: `Alert <https://selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.alert.html?highlight=alert#selenium.webdriver.common.alert.Alert>`__
.. |Keys| replace:: `Keys <https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html#module-selenium.webdriver.common.keys>`__
.. |By| replace:: `By <https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.by.html>`__

.. .. PyHamcrest
.. |PyHamcrest| replace:: `PyHamcrest <https://pyhamcrest.readthedocs.io/en/latest/>`__

.. .. Allure
.. |Allure| replace:: `Allure <https://docs.qameta.io/allure/>`__

.. .. Pytest
.. |pytest| replace:: `pytest <https://docs.pytest.org/en/latest/>`__

.. .. PyOTP
.. |PyOTP| replace:: `PyOTP <https://pyotp.readthedocs.io/en/latest/>`__

.. .. Requests
.. |requests| replace:: `requests <https://requests.readthedocs.io/en/master/>`__
.. |request| replace:: `Session.request <https://requests.readthedocs.io/en/master/api/#requests.Session.request>`__
"""

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "default"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

# Other HTML settings
autodoc_member_order = "bysource"
autodoc_typehints = "none"
add_module_names = False


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "ScreenPydoc"


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "ScreenPy.tex", "ScreenPy Documentation", "Perry Goy", "manual"),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "screenpy", "ScreenPy Documentation", [author], 1)]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "ScreenPy",
        "ScreenPy Documentation",
        author,
        "ScreenPy",
        "One line description of project.",
        "Miscellaneous",
    ),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ["search.html"]


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
}
