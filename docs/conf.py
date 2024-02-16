# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("./ext"))
sys.path.insert(0, os.path.abspath("../"))

from screenpy.__version__ import __version__, __author__, __copyright__

autodoc_mock_imports = ["hamcrest", "pydantic"]


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "ScreenPy"
copyright = __copyright__
author = __author__
release = __version__


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx_rtd_theme",
    "autodoc_skip_protocols",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = []

autodoc_member_order = "bysource"
add_module_names = False


# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}


# -- Options for Autodoc Pydantic extension ----------------------------------

# Don't show the JSON schema for BaseSettings extensions
autodoc_pydantic_settings_show_json = False
autodoc_pydantic_settings_show_config_member = False
autodoc_pydantic_settings_show_config_summary = False
autodoc_pydantic_settings_member_order = "bysource"
