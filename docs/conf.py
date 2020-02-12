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
.. .. Actors
.. |Actor| replace:: :class:`~screenpy.actor.Actor`
.. |Actor.named| replace:: :meth:`~screenpy.actor.Actor.named`
.. |Actor.who_can| replace:: :meth:`~screenpy.actor.Actor.who_can`
.. |Actor.can| replace:: :meth:`~screenpy.actor.Actor.can`
.. |Actor.ability_to| replace:: :meth:`~screenpy.actor.Actor.ability_to`
.. |Actor.attempts_to| replace:: :meth:`~screenpy.actor.Actor.attempts_to`
.. |Actor.should_see_that| replace:: :meth:`~screenpy.actor.Actor.should_see_that`
.. |Actor.should_see_the| replace:: :meth:`~screenpy.actor.Actor.should_see_the`
.. |Actor.exit| replace:: :meth:`~screenpy.actor.Actor.exit`
.. |UnableToPerformException| replace:: :class:`~screenpy.actor.UnableToPerformException`

.. .. Targets
.. |Target| replace:: :class:`~screenpy.target.Target`
.. |Target.the| replace:: :meth:`~screenpy.target.Target.the`
.. |Target.located_by| replace:: :meth:`~screenpy.target.Target.located_by`

.. .. Abilities
.. |BrowseTheWeb| replace:: :class:`~screenpy.abilities.browse_the_web.BrowseTheWeb`
.. |BrowseTheWeb.using| replace:: :meth:`~screenpy.abilities.browse_the_web.BrowseTheWeb.using`
.. |BrowseTheWeb.to_find| replace:: :meth:`~screenpy.abilities.browse_the_web.BrowseTheWeb.to_find`
.. |BrowseTheWeb.to_find_all| replace:: :meth:`~screenpy.abilities.browse_the_web.BrowseTheWeb.to_find_all`
.. |BrowseTheWeb.to_wait_for| replace:: :meth:`~screenpy.abilities.browse_the_web.BrowseTheWeb.to_wait_for`
.. |BrowseTheWeb.forget| replace:: :meth:`~screenpy.abilities.browse_the_web.BrowseTheWeb.forget`
.. |BrowseTheWeb.wait_for| replace:: :meth:`~screenpy.abilities.browse_the_web.BrowseTheWeb.wait_for`

.. .. Actions
.. |Action| replace:: :ref:`actions`
.. |Clear| replace:: :class:`~screenpy.actions.clear.Clear`
.. |Clear.the_text_from| replace:: :meth:`~screenpy.actions.clear.Clear.the_text_from`
.. |Clear.the_text_from_the| replace:: :meth:`~screenpy.actions.clear.Clear.the_text_from_the`
.. |Click| replace:: :class:`~screenpy.actions.click.Click`
.. |Click.on| replace:: :meth:`~screenpy.actions.click.Click.on`
.. |Click.on_the| replace:: :meth:`~screenpy.actions.click.Click.on_the`
.. |Click.then_wait_for| replace:: :meth:`~screenpy.actions.click.Click.then_wait_for`
.. |Click.perform_as| replace:: :meth:`~screenpy.actions.click.Click.perform_as`
.. |Debug| replace:: :class:`~screenpy.actions.debug.Debug`
.. |Enter| replace:: :class:`~screenpy.actions.enter.Enter`
.. |Enter.the_text| replace:: :meth:`~screenpy.actions.enter.Enter.the_text`
.. |Enter.into| replace:: :meth:`~screenpy.actions.enter.Enter.into`
.. |Enter.then_hit| replace:: :meth:`~screenpy.actions.enter.Enter.then_hit`
.. |Enter.then_wait_for| replace:: :meth:`~screenpy.actions.enter.Enter.then_wait_for`
.. |Open| replace:: :class:`~screenpy.actions.open.Open`
.. |Open.browser_on| replace:: :meth:`~screenpy.actions.open.Open.browser_on`
.. |Pause| replace:: :class:`~screenpy.actions.pause.Pause`
.. |Pause.for_| replace:: :meth:`~screenpy.actions.pause.Pause.for_`
.. |Select| replace:: :class:`~screenpy.actions.select.Select`
.. |Select.the_option_named| replace:: :meth:`~screenpy.actions.select.Select.the_option_named`
.. |Select.the_option_at_index| replace:: :meth:`~screenpy.actions.select.Select.the_option_at_index`
.. |Select.the_option_with_value| replace:: :meth:`~screenpy.actions.select.Select.the_option_with_value`
.. |SelectByText| replace:: :class:`~screenpy.actions.select.SelectByText`
.. |SelectByText.from_the| replace:: :meth:`~screenpy.actions.select.SelectByText.from_the`
.. |SelectByIndex| replace:: :class:`~screenpy.actions.select.SelectByIndex`
.. |SelectByIndex.from_the| replace:: :meth:`~screenpy.actions.select.SelectByIndex.from_the`
.. |SelectByValue| replace:: :class:`~screenpy.actions.select.SelectByValue`
.. |SelectByValue.from_the| replace:: :meth:`~screenpy.actions.select.SelectByValue.from_the`
.. |Wait| replace:: :class:`~screenpy.actions.wait.Wait`
.. |Wait.for_| replace:: :meth:`~screenpy.actions.wait.Wait.for_`
.. |Wait.for_the| replace:: :meth:`~screenpy.actions.wait.Wait.for_the`
.. |wait.to_appear| replace:: :meth:`~screenpy.actions.wait.Wait.to_appear`

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
.. |Text.asked_by| replace:: :meth:`~screenpy.questions.text.Text.asked_by`
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
.. |WebDriver| replace:: `WebDriver <https://seleniumhq.github.io/selenium/docs/api/py/api.html>`__
.. |WebElement| replace:: `WebElement <https://seleniumhq.github.io/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webelement.html#module-selenium.webdriver.remote.webelement>`__
.. |Keys| replace:: `Keys <https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html#module-selenium.webdriver.common.keys>`__
.. |By| replace:: `By <https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.by.html>`__

.. .. PyHamcrest
.. |PyHamcrest| replace:: `PyHamcrest <https://pyhamcrest.readthedocs.io/en/latest/>`__

.. .. Allure
.. |Allure| replace:: `Allure <https://docs.qameta.io/allure/>`__

.. .. Pytst
.. |Pytest| replace:: `Pytest <https://docs.pytest.org/en/latest/>`__
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
